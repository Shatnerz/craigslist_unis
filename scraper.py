from __future__ import print_function

from craigslist import CraigslistForSale

from slackclient import SlackClient
import settings
from util import post_listing_to_slack

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import sessionmaker
from dateutil.parser import parse


engine = create_engine('sqlite:///listings.db', echo=False)
Base = declarative_base()


class Listing(Base):
    """A table to store data on craigslist listings."""

    __tablename__ = 'listings'

    id = Column(Integer, primary_key=True)
    link = Column(String, unique=True)
    created = Column(DateTime)
    geotag = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    name = Column(String)
    price = Column(Float)
    location = Column(String)
    cl_id = Column(Integer, unique=True)

    def __init__(self, listing):
        """Initialize a listing object.

        Args:
            listing (dict): A dictionary describing a craigslist listing.
        """
        lat, lon = None, None
        if listing["geotag"] is not None:
            lat, lon = listing["geotag"]
        else:
            pass

        # Try parsing the price
        price = 0
        try:
            price = float(listing["price"].replace("$", ""))
        except Exception:
            pass

        # Explicitly set the column values (except id which auto-increments)
        self.link = listing["url"]
        self.created = parse(listing["datetime"])
        # self.geotag = listing["geotag"]
        self.lat = lat
        self.lon = lon
        self.name = listing["name"]
        self.price = price
        self.location = listing["where"]
        self.cl_id = listing["id"]


Base.metadata.create_all(engine)
Session = sessionmaker(engine)
session = Session()


def scrape():
    """Scrapes craigslist and finds the latest listings."""
    filters = {'query': settings.QUERY}
    cl = CraigslistForSale(site=settings.CRAIGSLIST_SITE, filters=filters)

    results = []
    gen = cl.get_results(sort_by='newest', geotagged=True, limit=20)
    while True:
        try:
            result = next(gen)
        except StopIteration:
            break
        except Exception:
            continue

        listing = session.query(Listing).filter_by(cl_id=result["id"]).first()

        # Don't store the listing if it already exists.
        if listing is not None:
            continue

        # Create the listing object
        listing = Listing(result)

        # Save the listing so we don't grab it again
        session.add(listing)
        session.commit()

        results.append(result)

    return results


def run_scraper():
    """Runs the craigslist scraper and posts data to slack."""

    # Create a slack client.
    sc = SlackClient(settings.SLACK_TOKEN)

    # Get all the results from craigslist.
    results = scrape()

    for result in results[::-1]:  # post the oldest first
        post_listing_to_slack(result, sc)

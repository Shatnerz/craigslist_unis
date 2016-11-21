"""Utility functions"""

import math
import requests
from bs4 import BeautifulSoup

import settings


def coord_distance(lat1, lon1, lat2, lon2):
    """
    Finds the distance between two pairs of latitude and longitude.

    See:
        http://www.codecodex.com/wiki/Calculate_distance_between_two_points_on_a_globe#Python

    Args:
        lat1: Point 1 latitude.
        lon1: Point 1 longitude.
        lat2: Point two latitude.
        lon2: Point two longitude.
    Return:
        Kilometer distance.
    """
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + \
        math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    km = 6367 * c
    return km


def post_listing_to_slack(listing, sc):
    """Post the listing to slack.

    Args:
        listing (dict): A record of the listing.
        sc: A slack client.
    """
    # Form msg text
    desc = "Name: {}\n".format(listing['name']) + \
           "Price: {}\n".format(listing['price'])
    if listing['where']:
        desc += "Where: {}\n".format(listing['where'])
    desc += "URL: {}".format(listing['url'])

    # Configure attachments if there are images
    attachments = []
    if listing['has_image']:
        print(listing['url'])
        img_urls = get_img_urls(listing['url'])
        img = img_urls[0]  # Just use the first image
        attachments = [{"title": listing['name'],
                        "image_url": img}]

    sc.api_call(
        "chat.postMessage", channel=settings.SLACK_CHANNEL, text=desc,
        attachments=attachments, username=settings.BOTNAME,
        icon_emoji=':robot_face:'
    )


def get_img_urls(url):
    """Extract the image urls from the HTML of a craigslist post."""
    out = []

    content = requests.get(url).content
    soup = BeautifulSoup(content, 'html.parser')
    for link in soup.find_all('a'):
        if link.get('data-imgid'):
            out.append(link.get('href'))

    if not out:  # maybe there is only one image
        for link in soup.find_all('img'):
            out.append(link.get('src'))
    return out

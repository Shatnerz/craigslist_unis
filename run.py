"""Run the craigslist scraper and slackbot."""

import sys
import time
import traceback

from scraper import run_scraper
import settings

import logging


logging.basicConfig(filename="scraper.log", level=logging.INFO)


if __name__ == '__main__':
    while True:
        print("{}: Starting scrape cycle".format(time.ctime()))
        try:
            run_scraper()
        except KeyboardInterrupt:
            print("Exiting...")
            logging.info("Exiting...")
            sys.exit(1)
        except Exception as exc:
            print("Error with scraping:", sys.exc_info()[0])
            logging.error("Error with scraping:", sys.exc_info()[0])
            traceback.print_exc()
        else:
            print("{}: Successfully finished scraping".format(time.ctime()))
            logging.info(
                "{}: Successfully finished scraping".format(time.ctime()))
        time.sleep(settings.SLEEP_INTERVAL)

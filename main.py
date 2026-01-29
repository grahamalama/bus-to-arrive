import argparse
import json

import requests
from pydantic import BaseModel


class Coordinates(BaseModel):
    latitude: float
    longitude: float


def get_current_location() -> Coordinates:
    url = "https://geolocation-db.com/json"
    try:
        response = requests.get(url)
        return Coordinates.model_validate_json(response.content.decode())
    except requests.exceptions.RequestException as e:
        print(f"Error fetching geolocation: {e}")
        return None


def fetch_closest_stop(locaiton: Coordinates):
    pass


def fetch_next_busses(stop):
    pass


def main():
    parser = argparse.ArgumentParser(
        prog="bts",
        description="View the next busses to arrive on your route",
    )
    parser.add_argument("route", help="bus route you're traveling on")
    parser.add_argument(
        "-s", "--start", help="Lat/Lon of where you're starting your journey from"
    )
    args = parser.parse_args()

    if args.start is None:
        # location = get_current_location()
        location = get_current_location()
    location = args.start

    stop = fetch_closest_stop(location)
    busses = fetch_next_busses(stop)


if __name__ == "__main__":
    print(get_current_location())
    main()

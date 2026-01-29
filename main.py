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


#  {'lng': '-75.16122', 'lat': '39.931609', 'stopid': '16608', 'stopname': 'Passyunk Av & 10th St'}


def fetch_route_stops(route: int):
    stops = requests.get(f"https://www3.septa.org/api/Stops/index.php?req1={route}")


def fetch_closest_stop(route, location):
    stops = fetch_route_stops(route)
    # TODO: compare location with stop lat/lons to find closest


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

    stop = fetch_closest_stop(args.route, location)
    busses = fetch_next_busses(stop)


if __name__ == "__main__":
    print(get_current_location())
    main()

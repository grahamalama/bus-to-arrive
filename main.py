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
    stops = requests.get(
        f"https://www3.septa.org/api/Stops/index.php?req1={route}"
    ).json()
    out = []
    for stop in stops:
        stop["lat"] = float(stop["lat"])
        stop["lng"] = float(stop["lng"])
        out.append(stop)
    return out



def distance(lat_1, lng_1, lat_2, lng_2) -> float:
    return abs(lat_2 - lat_1) + abs(lng_2 - lng_1)


def fetch_closest_stop(route, location):
    stops = fetch_route_stops(route)
    stops = sorted(stops, key=lambda stop: distance(
        lat_1=location.latitude,
        lng_1=location.longitude,
        lat_2=stop['lat'],
        lng_2=stop['lng']
    ))
    return stops[0]


def fetch_next_busses(stop_id: str, route: str):
    url = f"https://www3.septa.org/api/BusSchedules/index.php?stop_id={stop_id}"
    try:
        response = requests.get(url)
        route_busses = response.json()[route]
        route_busses = sorted(route_busses, key=lambda b: b["date"])
        return route_busses
    except requests.exceptions.RequestException as e:
        print(f"Error fetching next buses: {e}")
        return None
  


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

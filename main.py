import requests
import json
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


def main():
    print("Hello from bus-to-arrive!")


if __name__ == "__main__":
    print(get_current_location())
    main()

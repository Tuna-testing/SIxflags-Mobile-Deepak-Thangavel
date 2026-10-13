from get_api.api_park_helper import ParkHelper
from api_end_points import EndPoint
# Assuming EndPoint class is imported from endpoints.py
# from endpoints import EndPoint


class GetParkNameAndID:

    def __init__(self, env="prod"):
        self.env = env
        self.parks = {}
        self._fetch_and_store_parks()

    def _fetch_and_store_parks(self):
        """Fetch all parks from API and store in dictionary."""
        url = EndPoint.get_url("ALL_PARKS",self.env)
        helper = ParkHelper(url)
        data = helper.data

        # Store as {parkName: parkId}
        self.parks = {
            pname.lower(): str(pid)
            for park in data if isinstance(park, dict)
            for pname, pid in [(park.get("parkName"), park.get("parkId"))]
            if pname and pid
        }

    def get_park_id(self, park_name: str) -> str | None:
        return self.parks.get(park_name.lower())

    def get_park_name(self, park_id: str) -> str | None:
        for name, pid in self.parks.items():
            if pid == park_id:
                return name
        return None

    def display_all_parks(self):
        """Print all parks with their IDs."""
        for name, pid in self.parks.items():
            print(f"{name} : {pid}")

    def get_all_parks(self) -> dict:
        return self.parks

    # -------------------------
    # Example usage
    # -------------------------


if __name__ == "__main__":
    manager = GetParkNameAndID(env="uat")
    manager.display_all_parks()

    # Get park ID by name
    park_name = "cedar point"
    print("Park ID for the", park_name, ":", manager.get_park_id(park_name))

    # Get park name by ID
    park_id = "1"
    print("Park with ID", park_id, ":", manager.get_park_name(park_id))

    PARK_MAPPING = {
        "six flags america": 909,
        "canada's wonderland": 40,
        "california’s great america": 35,
        "carowinds": 30,
        "castaway bay": 203,
        "cedar point sports center": 204,
        "cedar point": 1,
        "six flags darien lake": 945,
        "six flags darien lake hotel & campground": 999,
        "six flags discovery kingdom": 936,
        "dorney park": 8,
        "six flags fiesta texas": 914,
        "six flags great adventure": 905,
        "frontier city": 943,
        "six flags great america": 910,
        "great escape": 924,
        "six flags great escape lodge": 923,
        "six flags hurricane harbor, chicago": 920,
        "hurricane harbor, concord": 942,
        "six flags hurricane harbor, los angeles": 911,
        "six flags hurricane harbor, jackson": 925,
        "hurricane harbor, rockford": 948,
        "hurricane harbor, oklahoma city": 944,
        "hurricane harbor, oaxtepec": 959,
        "hurricane harbor, arlington": 913,
        "kings dominion": 25,
        "la ronde": 969,
        "six flags mexico": 960,
        "knott's berry farm": 4,
        "kings island": 20,
        "six flags magic mountain": 906,
        "michigan’s adventure": 12,
        "six flags over texas": 901,
        "six flags over georgia": 902,
        "six flags new england": 935,
        "hurricane harbor, phoenix": 946,
        "six flags savannah sunset resort & spa": 50,
        "schlitterbahn galveston": 27,
        "sawmill creek resort": 999,
        "schlitterbahn new braunfels": 26,
        "valleyfair": 14,
        "six flags st. louis": 903,
        "hurricane harbor, splashtown": 947,
        "six flags white water": 922,
        "worlds of fun": 6,
    }


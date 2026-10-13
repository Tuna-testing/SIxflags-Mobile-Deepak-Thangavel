import requests
from end_points import EndPoint
from typing import Optional

class ParkManager:

    def __init__(self, env="prod"):
        self.timeout = None
        self.env = env
        self.parks = {}
        self._fetch_and_store_parks()

    def _fetch_and_store_parks(self):
        url = EndPoint.get_url("ALL_PARKS", self.env)
        data = EndPoint.get_response(url, timeout=self.timeout)

        # Store as {parkName.lower(): parkId}
        self.parks = {
            park["parkName"].lower(): str(park["parkId"])
            for park in data if isinstance(park, dict)
        }

    def get_park_id(self, park_namee: str) -> Optional[int]:
        return self.parks.get(park_namee.lower())

    def get_park_name(self, park_idd: int) -> Optional[str]:
        for name, pid in self.parks.items():
            if pid == park_idd:
                return name
        return None

    def display_all_parks(self):
        for name, pid in self.parks.items():
            print(f"{name} : {pid}")

if __name__ == "__main__":

    env = "prod"
    park_name = "Cedar Point"
    park_id = "30"
    manager = ParkManager(env)

    # Display all parks - manager.display_all_parks()

    #Display park ID by name
    print("Park ID for the", park_name, ":", manager.get_park_id(park_name))

    #Display park name by ID
    print("Park with ID", park_id, ":", manager.get_park_name(park_id))


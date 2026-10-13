from api.end_points import EndPoint


class GetParkNameAndID:

    def __init__(self, env="prod"):
        self.env = env
        self.parks = {}
        self._fetch_and_store_parks()

    def _fetch_and_store_parks(self):
        """Fetch all parks from API and store in dictionary."""
        url = EndPoint.get_all_parks_url(self.env)
        data = EndPoint.fetch_data(url, timeout=10)
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
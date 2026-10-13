import requests
from datetime import datetime

from execnet.gateway_base import pid


class ParkManager:
    # Environment-specific URLs
    allParks = {
        "uat": "https://d30xtgvjwxyou.cloudfront.net/content/all-parks",
        "prod": "https://content.prod.six-mt.com/content/all-parks",
    }

    operatingHours = {
        "uat": "https://d3f9rays5zpug9.cloudfront.net/operating-hours/all-parks",
        "prod": "https://d3f9rays5zpug9.cloudfront.net/operating-hours/all-parks",
    }

    def __init__(self, env: str = "prod"):
        env = env.lower()
        if env not in self.allParks or env not in self.operatingHours:
            raise ValueError(f"Unknown environment: {env}. Choose 'uat' or 'prod'.")
        self.env = env
        self.PARKS = self.get_parks()

    def get_parks(self) -> dict:
        url = self.allParks[self.env]
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            parks_map = {}
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        # Flexible key matching
                        pid = item.get("parkId") or item.get("id") or item.get("park_id")
                        pname = item.get("parkName") or item.get("name") or item.get("title")
                        print(pname , pid)
                        if pid is not None and pname:
                            # Normalize ID to string without extra spaces
                            clean_id = str(pid).strip()
                            parks_map[clean_id] = str(pname).strip()
            return parks_map
        except Exception as e:
            print(f"[DEBUG ERROR] Failed to fetch parks metadata from {url}: {e}")
            return {}

    def get_park_name(self, park_id: str) -> str:
        clean_id = str(park_id).strip()
        return self.PARKS.get(clean_id, f"Park ID {clean_id}")

    def get_park_id(self, park_name: str) -> str | None:
        target = park_name.strip().lower()
        for pid, pname in self.PARKS.items():
            if pname.lower() == target:
                return pid
        return None

    @staticmethod
    def fetch_json(url: str) -> list:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_operating_hours_url(self) -> str:
        return self.operatingHours[self.env]

    @staticmethod
    def format_time(time24: str) -> str:
        if not time24 or not isinstance(time24, str):
            return "N/A"
        try:
            t = datetime.strptime(time24.strip(), "%H:%M")
            return t.strftime("%I:%M %p")
        except Exception:
            return time24

    def _extract_operating_times(self, park_data: dict) -> str | None:
        """Helper to extract operating times safely from various nested schemas."""
        operatings = park_data.get("operatings") or park_data.get("operatingHours") or []
        if isinstance(operatings, list) and len(operatings) > 0:
            first_op = operatings[0]
            if isinstance(first_op, dict):
                items = first_op.get("items") or first_op.get("hours") or []
                if isinstance(items, list) and len(items) > 0:
                    first_item = items[0]
                    if isinstance(first_item, dict):
                        time_from = self.format_time(first_item.get("timeFrom") or first_item.get("open"))
                        time_to = self.format_time(first_item.get("timeTo") or first_item.get("close"))
                        return f"{time_from} - {time_to}"
        return None

    def get_all_operating_hours(self):
        url = self.get_operating_hours_url()
        try:
            arr = self.fetch_json(url)
        except Exception as e:
            print(f"[DEBUG ERROR] Failed to fetch operating hours: {e}")
            return

        open_parks, closed_parks = [], []

        for park in arr:
            if not isinstance(park, dict):
                continue

            raw_id = park.get("parkId") if park.get("parkId") is not None else park.get("id")
            if raw_id is None:
                continue

            park_id = str(raw_id).strip()
            park_name = self.get_park_name(park_id)

            # Check explicit closure flags or presence of active operating hours
            is_closed = park.get("isParkClosed") or park.get("isClosed") or park.get("closed")
            times_str = self._extract_operating_times(park)

            if is_closed is True or (is_closed is None and not times_str):
                closed_parks.append(f"{park_name} - Closed")
            else:
                hours_display = times_str if times_str else "Hours not specified"
                open_parks.append(f"{park_name} - {hours_display}")

        print(f"==========================================")
        print(f" OPERATING HOURS [ENVIRONMENT: {self.env.upper()}]")
        print(f" (Loaded {len(self.PARKS)} parks from metadata)")
        print(f"==========================================")

        print("Open Parks:")
        if open_parks:
            for op in open_parks:
                print(f" - {op}")
        else:
            print(" (None)")

        print("\nClosed Parks:")
        if closed_parks:
            for cp in closed_parks:
                print(f" - {cp}")
        else:
            print(" (None)")

    def park_status(self, park_name: str) -> str:
        park_id = self.get_park_id(park_name)
        if not park_id:
            return f"Unknown park '{park_name}' in {self.env.upper()} metadata"

        arr = self.fetch_json(self.get_operating_hours_url())
        for park in arr:
            if not isinstance(park, dict):
                continue

            raw_id = park.get("parkId") if park.get("parkId") is not None else park.get("id")
            if str(raw_id).strip() == park_id:
                is_closed = park.get("isParkClosed") or park.get("isClosed") or park.get("closed")
                times_str = self._extract_operating_times(park)

                if is_closed is True or (is_closed is None and not times_str):
                    return "Closed"
                return times_str if times_str else "Open (Hours N/A)"

        return "Closed"


# -------------------------
# Execution
# -------------------------
if __name__ == "__main__":
    park_name = "Knott's Berry Farm"
    env = "prod"  # Set "uat" or "prod"

    manager = ParkManager(env=env)
    manager.get_all_operating_hours()
    print(f"\nPark Status of '{park_name}' in {env.upper()}: {manager.park_status(park_name)}")
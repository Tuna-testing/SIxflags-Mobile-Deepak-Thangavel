import requests
from end_points import EndPoint
from get_api.park_name_and_park_id import ParkManager
from requests.exceptions import HTTPError
from typing import cast


class AppBanner:
    def __init__(self, env="prod"):
        self.env = env

    def check_banner(self, park_name: str, park_id: int) -> tuple[str, bool, str | None]:
        url = EndPoint.get_url("MOBILE_APP_BANNER", self.env, park_id=park_id)
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            # If API returns error JSON instead of banner list
            if isinstance(data, dict) and "error" in data:
                return park_name, False, None

            # Loop through banners
            for banner in data:
                link = banner.get("mobileLink", {}).get("link", "").lower()
                image_url = banner.get("image", {}).get("url")

                if park_name.lower().replace(" ", "") in link:
                    if image_url:
                        return park_name, True, image_url
                    else:
                        return park_name, False, None

            return park_name, False, None

        except HTTPError as e:
            # If it's a 404, return False cleanly
            if e.response.status_code == 404:
                return park_name, False, None
            # For other HTTP errors, re‑raise so you notice them
            raise


if __name__ == "__main__":
    envv = "uat"
    park_namee = "carowinds"
    park_idd = cast(int, ParkManager(envv).get_park_id(park_namee))
    checker = AppBanner(envv)

    # Carowinds → parkId = 30
    result = checker.check_banner(park_namee,park_idd)
    print(result)


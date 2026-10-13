from get_api.api_end_points import EndPoint
from get_api.api_park_helper import ParkHelper

class AppBannerChecker:

    @staticmethod
    def check_mobile_app_banner(park_id: str | int, env: str = "prod") -> tuple[bool, str]:
        # Build the correct URL for mobile app banner
        url = EndPoint.get_url(EndPoint.MOBILE_APP_BANNER, env=env, park_id=park_id)

        try:
            helper = ParkHelper(url)
            data = helper.data

            if isinstance(data, list) and len(data) > 0:
                # Loop through banners and check for image URL
                for item in data:
                    image_url = item.get("image")
                    if image_url:
                        return True, image_url

        except Exception as e:
            return False, f"[ERROR] {e}"

        # Otherwise return False with a message
        return False, "The requested resource could not be found."


# -------------------------
# Usage Example
# -------------------------
if __name__ == "__main__":
    is_available, result = AppBannerChecker.check_mobile_app_banner(park_id=969, env="prod")
    print(f"Success: {is_available}", f"Result: {result}")

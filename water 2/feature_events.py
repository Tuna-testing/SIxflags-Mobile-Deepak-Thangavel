from api_end_points import EndPoint
from all_parks import GetParkNameAndID
from api_park_helper import ParkHelper
from datetime import datetime, timedelta
import pytz


class FeaturedEvents:
    def __init__(self, park_name: str, env: str = "prod", timeout: int = 10):
        manager = GetParkNameAndID(env=env)
        self.park_id = manager.get_park_id(park_name)
        if not self.park_id:
            raise ValueError(f"Park '{park_name}' not found in {env.upper()} environment metadata.")

        self.env = env
        self.timeout = timeout

        # Load events data via ParkHelper
        url = EndPoint.get_url("EVENTS", env=env, park_id=self.park_id)
        self.helper = ParkHelper(url, timeout=timeout)

    def _get_cst_yesterday(self) -> str:
        """Return yesterday's date in CST/CDT (America/Chicago)."""
        tz = pytz.timezone("America/Chicago")
        now_cst = datetime.now(tz)
        yesterday = now_cst - timedelta(days=1)
        return yesterday.strftime("%Y-%m-%d")

    def get_featured_events(self) -> list[dict]:
        """
        Return events where endDate == yesterday's CST date.
        Each result contains {"fimsId": ..., "title": ...}.
        """
        feature_date = self._get_cst_yesterday()
        results = []

        if isinstance(self.helper.data, list):
            for ev in self.helper.data:
                if isinstance(ev, dict):
                    schedules = ev.get("showTimesSchedule", [])
                    for sched in schedules:
                        if sched.get("endDate") == feature_date and not ev.get("hideFromMobileAppFeaturedList", False):
                            results.append({
                                "fimsId": ev.get("fimsId") or ev.get("id"),
                                "title": ev.get("title")
                            })
        return results

    def display_featured_events(self):
        """Pretty print featured events."""
        events = self.get_featured_events()
        for ev in events:
            print(f"{ev['title']} | {ev['fimsId']}")

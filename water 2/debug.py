from datetime import datetime
from typing import Any, Dict, List, Union
from end_points import EndPoint


class SixFlagsGreatAdventureScheduleService:
    """Dedicated service class to parse operating hours for Six Flags Great Adventure,

    handling its split API park IDs (Theme Park, Water Park, and Safari).
    """

    PARK_NAME = "Six Flags Great Adventure"
    PRIMARY_ID = 905

    FACILITIES_CONFIG = {
        905: "Park",
        925: "Water Park",
        915: "Safari Park",
    }

    def __init__(self, env: str = "prod", timeout: int = 10):
        self.env = env.lower()
        self.timeout = timeout

    def _fetch_operating_hours(self) -> List[Dict[str, Any]]:
        """Fetches live operating hours schedule from the endpoint."""
        url = EndPoint.get_url("ALL_PARKS_OPERATING_HOURS", env=self.env)
        response = EndPoint.get_response(url, timeout=self.timeout)
        return response if isinstance(response, list) else []

    @staticmethod
    def _format_time(time_str: str) -> str:
        """Converts '10:00' -> '10:00 AM' / '19:00' -> '07:00 PM'."""
        if not time_str:
            return ""
        dt = datetime.strptime(time_str, "%H:%M")
        return dt.strftime("%I:%M %p").lstrip("0")

    @classmethod
    def _extract_facility_time(cls, p_data: dict) -> str:
        """Extracts operating hours for a dedicated facility API payload."""
        if not p_data or p_data.get("isParkClosed", True):
            return "Closed"

        for op in p_data.get("operatings", []):
            items = op.get("items", [])
            for item in items:
                t_from = cls._format_time(item.get("timeFrom"))
                t_to = cls._format_time(item.get("timeTo"))

                if t_from and t_to:
                    return f"{t_from} - {t_to}"
                elif t_from:
                    return t_from

        return "Closed"

    def get_hours(self) -> str:
        """Fetches and parses operating hours specifically for Six Flags Great Adventure."""
        hours_data = self._fetch_operating_hours()

        # Build ID lookup dictionary normalizing keys to integers
        hours_by_id = {}
        for item in hours_data:
            p_id = item.get("parkId")
            if p_id is not None:
                try:
                    hours_by_id[int(p_id)] = item
                except (ValueError, TypeError):
                    pass

        # Evaluate each facility independently (Theme Park, Water Park, Safari)
        schedules = []
        for fac_id, fac_label in self.FACILITIES_CONFIG.items():
            p_data = hours_by_id.get(fac_id, {})
            time_status = self._extract_facility_time(p_data)
            schedules.append(f"{fac_label}: {time_status}")

        schedule_str = " ".join(schedules)
        return f"{self.PARK_NAME} , {self.PRIMARY_ID} , {schedule_str}"


# -------------------------------------------------------------------------
# Execution Test
# -------------------------------------------------------------------------
if __name__ == "__main__":
    service = SixFlagsGreatAdventureScheduleService("uat")

    print("--- SIX FLAGS GREAT ADVENTURE HOURS ---")
    print(service.get_hours())
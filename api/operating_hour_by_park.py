from datetime import datetime
from typing import Any, Dict, List, Union
from end_points import EndPoint


class GetOperatingHours:
    def __init__(self, env: str = "prod", timeout: int = 10):
        self.env = env.lower()
        self.timeout = timeout

    # -------------------------------------------------------------------------
    # Helper & API Methods
    # -------------------------------------------------------------------------
    def _fetch_operating_hours(self) -> List[Dict[str, Any]]:
        url = EndPoint.get_all_parks_operating_hours_url(env=self.env)
        response = EndPoint.fetch_data(url, timeout=self.timeout)
        return response if isinstance(response, list) else []

    @staticmethod
    def _format_time(time_str: str) -> str:
        if not time_str:
            return ""
        dt = datetime.strptime(time_str, "%H:%M")
        return dt.strftime("%I:%M %p").lstrip("0")

    @classmethod
    def _extract_time(cls, p_data: dict) -> str:
        """Extracts time string regardless of operatingTypeName if isParkClosed is False."""
        if not p_data or p_data.get("isParkClosed", False) is True:
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

    # -------------------------------------------------------------------------
    # Core Parser Engine
    # -------------------------------------------------------------------------
    @classmethod
    def _parse_park_schedule(
        cls, park_name: str, config: dict, hours_by_id: dict
    ) -> str:
        primary_id = next(iter(config.keys()))
        schedules = []

        for p_id, fac_config in config.items():
            p_data = hours_by_id.get(int(p_id), {})

            # Case 1: Single-ID containing nested flags e.g. {Park: True, Water Park: True}
            if isinstance(fac_config, dict):
                hours_map = {}
                if not p_data.get("isParkClosed", False):
                    for op in p_data.get("operatings", []):
                        op_name = op.get("operatingTypeName", "").lower()
                        items = op.get("items", [])
                        if items:
                            t_from = cls._format_time(items[0].get("timeFrom"))
                            t_to = cls._format_time(items[0].get("timeTo"))
                            hours_map[op_name] = (
                                f"{t_from} - {t_to}"
                                if t_from and t_to
                                else t_from
                            )

                if fac_config.get("Park"):
                    schedules.append(f"Park: {hours_map.get('park', 'Closed')}")
                if fac_config.get("Water Park"):
                    schedules.append(
                        f"Water Park: {hours_map.get('waterpark', 'Closed')}"
                    )

            # Case 2: Multi-ID explicit facility string e.g. {915: "Safari Park"}
            elif isinstance(fac_config, str):
                time_status = cls._extract_time(p_data)
                schedules.append(f"{fac_config}: {time_status}")

        schedule_str = " ".join(schedules) if schedules else "Park: Closed"
        return f"{park_name} , {primary_id} , {schedule_str}"

    # -------------------------------------------------------------------------
    # Main Engine
    # -------------------------------------------------------------------------
    def get_hours(self, query: Union[str, int]) -> Union[str, List[str]]:
        hours_data = self._fetch_operating_hours()

        # Safely normalize all keys in hours_by_id to integers
        hours_by_id = {}
        for item in hours_data:
            p_id = item.get("parkId")
            if p_id is not None:
                try:
                    hours_by_id[int(p_id)] = Any
                except (ValueError, TypeError):
                    pass

        query_str = str(query).strip().lower().replace("’", "'")

        if query_str == "all":
            return [
                self._parse_park_schedule(name, cfg, hours_by_id)
                for name, cfg in self.PARK_CONFIGS.items()
            ]

        if query_str.isdigit():
            target_id = int(query_str)
            for name, cfg in self.PARK_CONFIGS.items():
                if target_id in cfg:
                    return self._parse_park_schedule(name, cfg, hours_by_id)

        for name, cfg in self.PARK_CONFIGS.items():
            if query_str == name.lower().replace("’", "'"):
                return self._parse_park_schedule(name, cfg, hours_by_id)

        return f"Park '{query}' not found."


# -------------------------------------------------------------------------
# Test Script
# -------------------------------------------------------------------------
if __name__ == "__main__":
    service = GetOperatingHours("prod")

    print(service.get_hours("Six Flags Great Adventure"))
    print(service.get_hours("Cedar Point"))
    print(service.get_hours("Canada's Wonderland"))
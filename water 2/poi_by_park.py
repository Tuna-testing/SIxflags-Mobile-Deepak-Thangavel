from typing import Any

import requests
from api_end_points import EndPoint

class POICategoryHelper:

    @staticmethod
    def fetch_pois(env="prod", park_id=30):
        url = EndPoint.get_url("POI_DETAILS", env=env, park_id=park_id)
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_category_map(env="prod", park_id=30) -> dict:
        """
        1. Return {fimsId: name} for all POIs grouped by category prefix.
        Example: {"RIDE-030-00058": "Ripcord", "RIDE-030-00072": "Fury 325"}
        """
        pois = POICategoryHelper.fetch_pois(env, park_id)
        category_map = {}
        for poi in pois:
            fims_id = poi.get("fimsId", "")
            name = poi.get("name", "").replace("<p>", "").replace("</p>", "")
            if fims_id:
                category_map[fims_id] = name
        return category_map

    @staticmethod
    def get_category_names(env="prod", park_id=30) -> set:
        """
        2. Return unique category names only.
        Example: {"RIDE", "RESTAURANT", "SHOW", "RETAIL", "GS", "PARKING", "REALITY"}
        """
        pois = POICategoryHelper.fetch_pois(env, park_id)
        categories = set()
        for poi in pois:
            fims_id = poi.get("fimsId", "")
            if fims_id:
                prefix = fims_id.split("-")[0]
                categories.add(prefix)
        return categories

    @staticmethod
    def get_active_mobile_by_category(env="prod", park_id=30) -> dict:
        """
        3. Return POIs grouped by category where isActive=True and isMobile=True.
        Example: {"RIDE": ["Ripcord", "Fury 325"], "RESTAURANT": [...]}
        """
        pois = POICategoryHelper.fetch_pois(env, park_id)
        grouped = {}
        for poi in pois:
            if poi.get("isActive") and poi.get("isMobile"):
                fims_id = poi.get("fimsId", "")
                prefix = fims_id.split("-")[0] if fims_id else "UNKNOWN"
                name = poi.get("name", "").replace("<p>", "").replace("</p>", "")
                grouped.setdefault(prefix, []).append(name)
        return grouped

    @staticmethod
    def get_active_non_mobile_by_category(env="prod", park_id=30) -> dict:
        """
        4. Return POIs grouped by category where isActive=True and isMobile=False.
        Example: {"RIDE": ["Slingshot"], "SHOW": [...]}
        """
        pois = POICategoryHelper.fetch_pois(env, park_id)
        grouped = {}
        for poi in pois:
            if poi.get("isActive") and not poi.get("isMobile"):
                fims_id = poi.get("fimsId", "")
                prefix = fims_id.split("-")[0] if fims_id else "UNKNOWN"
                name = poi.get("name", "").replace("<p>", "").replace("</p>", "")
                grouped.setdefault(prefix, []).append(name)
        return grouped

    @staticmethod
    def get_pois_by_category_prefix(prefix: str, env="prod", park_id=30) -> list[Any]:
        """
        5. Return POIs whose fimsId starts with the given prefix.
        Example: get_pois_by_category_prefix("RIDE") → {"RIDE-030-00058": "Ripcord", "RIDE-030-00072": "Fury 325"}
        """
        pois = POICategoryHelper.fetch_pois(env, park_id)
        names = []
        for poi in pois:
            fims_id = poi.get("fimsId", "")
            name = poi.get("name", "").replace("<p>", "").replace("</p>", "")
            if fims_id.startswith(prefix.upper()):
                names.append(name)
        return sorted(names)

if __name__ == "__main__":

        env = "prod"
        park_id = 4
        rides = POICategoryHelper.get_pois_by_category_prefix("RIDE", env, park_id)
        restaurants = POICategoryHelper.get_pois_by_category_prefix("RESTAURANT", env, park_id)
        restroom = POICategoryHelper.get_pois_by_category_prefix("RESTROOM", env, park_id)
        shows_and_entertainment  = POICategoryHelper.get_pois_by_category_prefix("SHOW", env, park_id)
        shopping_and_activity = POICategoryHelper.get_pois_by_category_prefix("RETAIL", env, park_id)
        guest_services = POICategoryHelper.get_pois_by_category_prefix("GS", env, park_id)
        AR_games = POICategoryHelper.get_pois_by_category_prefix("REALITY", env, park_id)
        print("Rides:", rides)
        print("Restaurants:", restaurants)
        print("shows & entertainment:", shows_and_entertainment)
        print("shopping & activity:", shopping_and_activity)
        print("Restroom:", restroom)
        print("Guest Services:", guest_services)
        print("AR Games:", AR_games)



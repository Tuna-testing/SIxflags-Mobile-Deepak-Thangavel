import requests
from bs4 import BeautifulSoup
from api_end_points import EndPoint
from all_parks import GetParkNameAndID
from api_park_helper import ParkHelper
from feature_events import FeaturedEvents


class FeaturePOI:
    def __init__(self, park_name: str, env: str = "prod"):
        manager = GetParkNameAndID(env=env)
        self.park_id = manager.get_park_id(park_name)
        if not self.park_id:
            raise ValueError(f"Park '{park_name}' not found in {env.upper()} environment metadata.")
        self.env = env

        self.poi_helper = ParkHelper(EndPoint.get_url("POI_DETAILS", env=env, park_id=self.park_id))
        self.event_helper = ParkHelper(EndPoint.get_url("EVENTS", env=env, park_id=self.park_id))
        self.featured_helper = ParkHelper(EndPoint.get_url("FEATURED_POIS", env=env, park_id=self.park_id))

        self.featured = FeaturedEvents("La Ronde", env="prod")
        print("--- Featured Events ---")
        self.featured.display_featured_events()

    def _build_lookup(self, helper: ParkHelper) -> dict:   # fixed
        lookup = {}
        if isinstance(helper.data, list):
            for obj in helper.data:
                if isinstance(obj, dict):
                    fims_id = obj.get("fimsId") or obj.get("id")
                    name = obj.get("name") or obj.get("title")
                    if fims_id and name:
                        lookup[str(fims_id)] = name
        return lookup
    def _display_category(self, list_type: str, heading: str, lookup: dict) -> list:
        results = []
        if isinstance(self.featured_helper.data, list):
            for section in self.featured_helper.data:
                if isinstance(section, dict) and section.get("listType", "").lower() == list_type.lower():
                    print(f"\n{heading}:")
                    docs = section.get("poiDocuments", [])
                    for doc in docs:
                        if isinstance(doc, dict):
                            if "fimsId" in doc:
                                fid = str(doc["fimsId"])
                                results.append(lookup.get(fid, fid))
                            elif "fimsIds" in doc:
                                for f_id in doc["fimsIds"]:
                                    fid = str(f_id)
                                    results.append(lookup.get(fid, fid))
        return [BeautifulSoup(str(poi), "html.parser").get_text().strip() for poi in results]

    def display_featured_rides(self) -> list:
        lookup = self._build_lookup(self.poi_helper)
        return self._display_category("ride", "Popular Rides", lookup)

    def display_featured_dinning(self) -> list:
        lookup = self._build_lookup(self.poi_helper)
        return self._display_category("restaurant", "Featured Restaurants", lookup)

    def display_featured_events(self) -> list:
        lookup = self._build_lookup(self.event_helper)
        return self._display_category("events", "Featured Events", lookup)

if __name__ == "__main__":
    park_name = "La ronde"
    env = "prod"

    featured_events = FeaturedEvents(park_name, env)

    feature_poi = FeaturePOI(park_name, env)

    print("--- Featured Rides ---")
    print(feature_poi.display_featured_rides())

    print("--- Featured Dining ---")
    print(feature_poi.display_featured_dinning())

    print("--- Featured Events ---")
    print(featured_events.display_featured_events())

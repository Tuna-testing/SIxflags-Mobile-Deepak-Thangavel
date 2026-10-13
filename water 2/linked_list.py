import requests

# Dictionary of all park IDs and names
PARKS = {
    "1": "Cedar Point",
    "4": "Knott's Berry Farm",
    "6": "Worlds of Fun",
    "8": "Dorney Park",
    "12": "Michigan’s Adventure",
    "14": "Valleyfair",
    "20": "Kings Island",
    "25": "Kings Dominion",
    "26": "New Braunfels",
    "27": "Galveston",
    "30": "Carowinds",
    "35": "Great America",
    "40": "Canada’s Wonderland",
    "202": "Cedar Point Shores",
    "203": "Cedar Point Castaway Bay",
    "901": "Six Flags Over Texas",
    "902": "Six Flags Over Georgia",
    "903": "Six Flags St. Louis",
    "905": "SF Great Adventure",
    "906": "Six Flags Magic Mountain",
    "909": "Six Flags America",
    "910": "Six Flags Great America",
    "911": "Hurricane Harbor Los Angeles",
    "913": "Hurricane Harbor Arlington",
    "914": "Six Flags Fiesta Texas",
    "915": "Wild Safari Adventure",
    "920": "Hurricane Harbor Chicago",
    "922": "Six Flags White Water",
    "923": "Great Escape Lodge",
    "924": "Six Flags Great Escape",
    "925": "Hurricane Harbor New Jersey",
    "935": "Six Flags New England",
    "936": "Six Flags Discovery Kingdom",
    "943": "Six Flags Frontier City",
    "944": "Hurricane Harbor Oklahoma City",
    "945": "Six Flags Darien Lake",
    "946": "Hurricane Harbor Phoenix",
    "947": "Hurricane Harbor Splashtown",
    "948": "Hurricane Harbor Rockford",
    "959": "Hurricane Harbor Oaxtepec",
    "960": "Six Flags Mexico",
    "969": "Six Flags La Ronde",
    "942": "Hurricane Harbor Concord"
}

TARGET_SCREEN_PLACEMENT = "more_menu"


class ParkMenuChecker:
    # Base URL mappings
    ENV_URLS = {
        "UAT": "https://d30xtgvjwxyou.cloudfront.net/content/link-list/park/",
        "PROD": "https://content.prod.six-mt.com/content/link-list/park/"
    }

    def __init__(self, park_dict, target_placement, environment="UAT"):
        self.parks = park_dict
        self.target_placement = target_placement
        self.environment = environment.upper()

        # Validate environment input
        if self.environment not in self.ENV_URLS:
            raise ValueError(f"Invalid environment '{environment}'. Choose either 'UAT' or 'PROD'.")

        self.base_url = self.ENV_URLS[self.environment]
        self.showing_list = []
        self.not_showing_list = []

    def process_all_parks(self):
        """Fetch API data for each park and process screenPlacement and link titles."""
        for park_id, name in self.parks.items():
            url = f"{self.base_url}{park_id}"

            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    self._check_and_extract(park_id, name, data)
                else:
                    self.not_showing_list.append({"name": name, "id": park_id})
            except Exception:
                self.not_showing_list.append({"name": name, "id": park_id})

    def _check_and_extract(self, park_id, name, data):
        """Helper to scan JSON structure for screenPlacement and extract titles."""
        found = False

        if isinstance(data, list):
            for group in data:
                if isinstance(group, dict) and group.get("screenPlacement") == self.target_placement:
                    links = group.get("links", [])
                    titles = [link.get("title") for link in links if isinstance(link, dict) and "title" in link]

                    self.showing_list.append({
                        "name": name,
                        "id": park_id,
                        "screenPlacement": self.target_placement,
                        "titles": titles
                    })
                    found = True
                    break

        if not found:
            self.not_showing_list.append({"name": name, "id": park_id})

    def print_report(self):
        """Print results formatted as requested."""
        print(f"--- ENVIRONMENT: {self.environment} ---")
        print(f'screenPlacement:"{self.target_placement}" is showing')
        for park in self.showing_list:
            titles_str = ", ".join(park["titles"])
            print(f'{park["name"]} , {park["id"]} , {park["screenPlacement"]} , {titles_str}')

        print(f'\nscreenPlacement:"{self.target_placement}" is not showing')
        for park in self.not_showing_list:
            print(f'{park["name"]} , {park["id"]}')


if __name__ == "__main__":
    # Declare your environment here: "UAT" or "PROD"
    ENV = "UAT"

    checker = ParkMenuChecker(PARKS, TARGET_SCREEN_PLACEMENT, environment=ENV)
    checker.process_all_parks()
    checker.print_report()
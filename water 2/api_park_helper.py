import requests

class ParkHelper:
    def _fetch_data(self):
        """Fetch JSON data from the given URL with error handling."""
        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Request failed: {e}")
            return []
        except ValueError as e:
            print(f"[ERROR] Invalid JSON: {e}")
            return []


    def extract_key(self, key: str) -> list:
        """
        Extract values for a given key from all items in the response.
        Example: key="parkName" → returns list of all park names.
        """
        results = []
        if isinstance(self.data, list):
            for item in self.data:
                if isinstance(item, dict):
                    value = item.get(key)
                    if value is not None:
                        results.append(value)
        else:
            print("[WARNING] Response is not a list of objects.")
        return results


    def extract_multiple_keys(self, keys: list[str]) -> list[dict]:
        """
        Extract multiple keys from each item.
        Example: keys=["parkName","parkId","slug"]
        Returns list of dicts with those fields.
        """
        results = []
        if isinstance(self.data, list):
            for item in self.data:
                if isinstance(item, dict):
                    entry = {k: item.get(k) for k in keys}
                    results.append(entry)
        return results


    def display_data(self, keys: list[str]):
        """Pretty print selected keys for all items."""
        extracted = self.extract_multiple_keys(keys)
        for entry in extracted:
            print(" | ".join(f"{k}: {v}" for k, v in entry.items()))

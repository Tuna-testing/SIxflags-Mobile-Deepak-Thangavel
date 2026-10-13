import get_api as api
import requests


class GetAllParks:

  @staticmethod
  def get_all_parks(env):
    """Fetches all raw park data from API."""
    url = api.get_all_parks_url(env=env)
    response = requests.get(url)
    return response.json()

  @staticmethod
  def get_park_name_by_id(park_id: str):
    """Accepts a park ID and returns the corresponding park name."""
    parks = GetAllParks.get_all_parks("prod")
    target_id = int(park_id)

    for park in parks:
      if park.get("parkId") == target_id:
        return park.get("parkName")

    return None

  @staticmethod
  def get_park_id_by_name(park_name: str):
    """Accepts a park name (case-insensitive) and returns the park ID."""
    parks = GetAllParks.get_all_parks("prod")
    target_name = park_name.strip().lower()

    for park in parks:
      current_name = park.get("parkName", "").strip().lower()
      if current_name == target_name:
        return park.get("parkId")

    return None

  @staticmethod
  def get_all_parks_dict(envv) -> dict:
    """Returns a dictionary of {"park_name": park_id}."""
    parks = GetAllParks.get_all_parks(envv)
    return {
        park.get("parkName", "").strip().lower(): park.get("parkId")
        for park in parks
        if isinstance(park, dict)
        and park.get("parkName")
        and park.get("parkId")
    }

  @staticmethod
  def display_all_parks(envv):
    """Prints all parks with their IDs."""
    parks_dict = GetAllParks.get_all_parks_dict(envv)
    for name, pid in parks_dict.items():
      print(f'"{name}" : {pid},')


if __name__ == "__main__":
  park_idd = "30"
  park_namee = "six flags america"
  env = "prod"

  # 2. Display formatted list of all parks
  print("\n--- All Parks List ---")
  GetAllParks.display_all_parks(env)

  # 3. Lookups without env
  name_from_id = GetAllParks.get_park_name_by_id(park_idd)
  id_from_name = GetAllParks.get_park_id_by_name(park_namee)

  print(f"\nPark ID {park_idd} -> Park Name: {name_from_id}")
  print(f"Park Name '{park_namee}' -> ID: {id_from_name}")
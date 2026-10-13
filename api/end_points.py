import argparse
from typing import Any, Dict, Optional
import requests


class EndPoint:
  # Base URL Mappings (Added 'dev' mapping to match CLI options)
  FIMS_URL = {
      "dev": "https://d2drkhmmovtf5u.cloudfront.net",
      "uat": "https://d2drkhmmovtf5u.cloudfront.net",
      "prod": "https://fims.prod.six-mt.com",
  }

  CONTENT_URL = {
      "dev": "https://d2es6ucq9ddbh1.cloudfront.net",
      "uat": "https://d2es6ucq9ddbh1.cloudfront.net",
      "prod": "https://content.prod.six-mt.com",
  }

  @staticmethod
  def _get_env_from_cli() -> str:
    """Detects --env parameter passed via command line, defaults to prod."""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--env", choices=["dev", "uat", "prod"], default="prod")
    args, _ = parser.parse_known_args()
    return args.env

  DEFAULT_ENV = _get_env_from_cli()

  # ==========================================
  # 1. No Parameter EndPoint
  # ==========================================
  @staticmethod
  def get_all_parks_url(env: str = DEFAULT_ENV) -> str:
    return f"{EndPoint.CONTENT_URL[env]}/content/all-parks"

  @staticmethod
  def get_all_parks_operating_hours_url(env: str = DEFAULT_ENV) -> str:
    return f"{EndPoint.FIMS_URL[env]}/operating-hours/all-parks"

  # ==========================================
  # 2. Park ID Parameter EndPoint
  # ==========================================
  @staticmethod
  def get_product_list_url(
      park_id: str | int, env: str = DEFAULT_ENV
  ) -> str:
    return f"{EndPoint.CONTENT_URL[env]}/content/product-list/park/{park_id}"

  @staticmethod
  def get_events_url(park_id: str | int, env: str = DEFAULT_ENV) -> str:
    return f"{EndPoint.CONTENT_URL[env]}/content/events/park/{park_id}"

  @staticmethod
  def get_more_link_list_url(
      park_id: str | int, env: str = DEFAULT_ENV
  ) -> str:
    return f"{EndPoint.CONTENT_URL[env]}/content/link-list/park/{park_id}"

  @staticmethod
  def get_featured_pois_url(
      park_id: str | int, env: str = DEFAULT_ENV
  ) -> str:
    return f"{EndPoint.CONTENT_URL[env]}/content/poi-list/park/{park_id}"

  @staticmethod
  def get_product_taxonomy_url(
      park_id: str | int, env: str = DEFAULT_ENV
  ) -> str:
    return (
        f"{EndPoint.CONTENT_URL[env]}/content/product-taxonomy/park/{park_id}"
    )

  @staticmethod
  def get_loyalty_entitlements_url(
      park_id: str | int, env: str = DEFAULT_ENV
  ) -> str:
    return f"{EndPoint.CONTENT_URL[env]}/content/loyalty-entitlement/park/{park_id}"

  @staticmethod
  def get_poi_details_url(park_id: str | int, env: str = DEFAULT_ENV) -> str:
    return f"{EndPoint.FIMS_URL[env]}/poi/park/{park_id}"

  @staticmethod
  def get_wait_times_url(park_id: str | int, env: str = DEFAULT_ENV) -> str:
    return f"{EndPoint.FIMS_URL[env]}/wait-times/park/{park_id}"

  @staticmethod
  def get_venue_status_url(park_id: str | int, env: str = DEFAULT_ENV) -> str:
    return f"{EndPoint.FIMS_URL[env]}/venue-status/park/{park_id}"

  @staticmethod
  def get_mobile_app_banner_url(
      park_id: str | int, env: str = DEFAULT_ENV
  ) -> str:
    return f"{EndPoint.CONTENT_URL[env]}/content/mobile-app-banner/park/{park_id}"

  # ==========================================
  # 3. Multi-Parameter & Query EndPoint
  # ==========================================
  @staticmethod
  def get_operating_hours_by_date_url(
      park_id: str | int, date: str, env: str = DEFAULT_ENV
  ) -> str:
    return (
        f"{EndPoint.FIMS_URL[env]}/operating-hours/park/{park_id}?date={date}"
    )

  @staticmethod
  def get_operating_hours_by_month_url(
      park_id: str | int, year_month: str, env: str = DEFAULT_ENV
  ) -> str:
    return f"{EndPoint.FIMS_URL[env]}/operating-hours/park/{park_id}?date={year_month}"

  # ==========================================
  # 4. Get API Helper
  # ==========================================
  @staticmethod
  def fetch_data(url: str, timeout: int = 10) -> Any:
    """Fetch JSON data from the given URL with error handling."""
    try:
      response = requests.get(url, timeout=timeout)
      response.raise_for_status()
      return response.json()
    except requests.exceptions.RequestException as e:
      print(f"[ERROR] Request failed: {e}")
      return []
    except ValueError as e:
      print(f"[ERROR] Invalid JSON: {e}")
      return []
import argparse
import os
import requests
from typing import Any, Optional


class EndPoint:
    # Base URL Mappings
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

    # ------------------------------------------------------------
    # FIX 1: Do NOT freeze the env at import time.
    # Resolve it lazily, per-call, with a clear priority:
    #   1. explicit argument
    #   2. --env on CLI
    #   3. TEST_ENV environment variable
    #   4. "prod" default
    # ------------------------------------------------------------
    @staticmethod
    def _get_env_from_cli() -> Optional[str]:
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("--env", choices=["dev", "uat", "prod"], default=None)
        args, _ = parser.parse_known_args()
        return args.env

    @staticmethod
    def _resolve_env(env: Optional[str]) -> str:
        if env:
            return env
        cli_env = EndPoint._get_env_from_cli()
        if cli_env:
            return cli_env
        return os.getenv("TEST_ENV", "prod")

    # ==========================================
    # 1. No Parameter EndPoint
    # ==========================================
    @staticmethod
    def get_all_parks_url(env: Optional[str] = None) -> str:
        env = EndPoint._resolve_env(env)
        return f"{EndPoint.CONTENT_URL[env]}/content/all-parks"

    @staticmethod
    def get_all_parks_operating_hours_url(env: Optional[str] = None) -> str:
        env = EndPoint._resolve_env(env)
        return f"{EndPoint.FIMS_URL[env]}/operating-hours/all-parks"

    # ==========================================
    # 2. Park ID Parameter EndPoint
    # ==========================================
    @staticmethod
    def get_product_list_url(park_id, env: Optional[str] = None) -> str:
        env = EndPoint._resolve_env(env)
        return f"{EndPoint.CONTENT_URL[env]}/content/product-list/park/{park_id}"

    @staticmethod
    def get_events_url(park_id, env: Optional[str] = None) -> str:
        env = EndPoint._resolve_env(env)
        return f"{EndPoint.CONTENT_URL[env]}/content/events/park/{park_id}"

    @staticmethod
    def get_more_link_list_url(park_id, env: Optional[str] = None) -> str:
        env = EndPoint._resolve_env(env)
        return f"{EndPoint.CONTENT_URL[env]}/content/link-list/park/{park_id}"

    @staticmethod
    def get_featured_pois_url(park_id, env: Optional[str] = None) -> str:
        env = EndPoint._resolve_env(env)
        return f"{EndPoint.CONTENT_URL[env]}/content/poi-list/park/{park_id}"

    @staticmethod
    def get_product_taxonomy_url(park_id, env: Optional[str] = None) -> str:
        env = EndPoint._resolve_env(env)
        return f"{EndPoint.CONTENT_URL[env]}/content/product-taxonomy/park/{park_id}"

    @staticmethod
    def get_loyalty_entitlements_url(park_id, env: Optional[str] = None) -> str:
        env = EndPoint._resolve_env(env)
        return f"{EndPoint.CONTENT_URL[env]}/content/loyalty-entitlement/park/{park_id}"

    @staticmethod
    def get_poi_details_url(park_id, env: Optional[str] = None) -> str:
        env = EndPoint._resolve_env(env)
        return f"{EndPoint.FIMS_URL[env]}/poi/park/{park_id}"

    @staticmethod
    def get_wait_times_url(park_id, env: Optional[str] = None) -> str:
        env = EndPoint._resolve_env(env)
        return f"{EndPoint.FIMS_URL[env]}/wait-times/park/{park_id}"

    @staticmethod
    def get_venue_status_url(park_id, env: Optional[str] = None) -> str:
        env = EndPoint._resolve_env(env)
        return f"{EndPoint.FIMS_URL[env]}/venue-status/park/{park_id}"

    @staticmethod
    def get_mobile_app_banner_url(park_id, env: Optional[str] = None) -> str:
        env = EndPoint._resolve_env(env)
        return f"{EndPoint.CONTENT_URL[env]}/content/mobile-app-banner/park/{park_id}"

    # ==========================================
    # 3. Multi-Parameter & Query EndPoint
    # ==========================================
    @staticmethod
    def get_operating_hours_by_date_url(park_id, date: str, env: Optional[str] = None) -> str:
        env = EndPoint._resolve_env(env)
        return f"{EndPoint.FIMS_URL[env]}/operating-hours/park/{park_id}?date={date}"

    @staticmethod
    def get_operating_hours_by_month_url(park_id, year_month: str, env: Optional[str] = None) -> str:
        env = EndPoint._resolve_env(env)
        return f"{EndPoint.FIMS_URL[env]}/operating-hours/park/{park_id}?date={year_month}"

    # ==========================================
    # 4. Get API Helper
    # ==========================================
    # FIX 3: No more silent [] on failure. Raise so callers/tests see the real error.
    @staticmethod
    def fetch_data(url: str, timeout: int = 10) -> Any:
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"[ERROR] HTTP error for {url}: {e}")
            raise
        except requests.exceptions.ConnectionError as e:
            print(f"[ERROR] Connection error for {url}: {e}")
            raise
        except requests.exceptions.Timeout as e:
            print(f"[ERROR] Timeout after {timeout}s for {url}: {e}")
            raise
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Request failed for {url}: {e}")
            raise
        except ValueError as e:
            print(f"[ERROR] Invalid JSON from {url}: {e}")
            raise
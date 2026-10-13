import requests

class EndPoint:
    # Define base URLs per environment

    fims ={
            "dev": "https://d32k9x3lmi2sdi.cloudfront.net",
            "uat": "https://d2drkhmmovtf5u.cloudfront.net",
            "prod": "https://fims.prod.six-mt.com"
        }
    content={
            "dev": "https://d376sgfm22b4hx.cloudfront.net",
            "uat": "https://d2es6ucq9ddbh1.cloudfront.net",
            "prod": "https://content.prod.six-mt.com"
        }


    # Endpoint paths relative to base
    PATHS = {
        "ALL_PARKS": "/content/all-parks",
        "ALL_PARKS_OPERATING_HOURS": "/operating-hours/all-parks",

        "PRODUCT_LIST": "/content/product-list/park/{park_id}",
        "EVENTS": "/content/events/park/{park_id}",
        "MORE_LINK_LIST": "/content/link-list/park/{park_id}",
        "FEATURED_POIS": "/content/poi-list/park/{park_id}",
        "PRODUCT_TAXONOMY": "/content/product-taxonomy/park/{park_id}",
        "LOYALTY_ENTITLEMENTS": "/content/loyalty-entitlement/park/{park_id}",
        "POI_DETAILS": "/poi/park/{park_id}",
        "WAIT_TIMES": "/wait-times/park/{park_id}",
        "VENUE_STATUS": "/venue-status/park/{park_id}",
        "MOBILE_APP_BANNER": "/content/mobile-app-banner/park/{park_id}",

        "OPERATING_HOURS_BY_DATE": "/operating-hours/park/{park_id}?date={date}",
        "OPERATING_HOURS_BY_MONTH": "/operating-hours/park/{park_id}?date={year_month}"



    }

    @classmethod
    def get_url(cls, key: str, env: str = "prod", **kwargs) -> str:
        """
        Build full URL for given endpoint key and environment.
        """
        # Decide if endpoint belongs to fims or content
        if key in ["OPERATING_HOURS_BY_DATE", "OPERATING_HOURS_BY_MONTH",
                   "ALL_PARKS_OPERATING_HOURS", "POI_DETAILS",
                   "WAIT_TIMES", "VENUE_STATUS"]:
            base = cls.BASES["fims"][env]
        else:
            base = cls.BASES["content"][env]

        path = cls.PATHS[key]
        return base + path.format(**kwargs)

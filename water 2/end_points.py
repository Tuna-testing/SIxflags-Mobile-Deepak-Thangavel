# Define base URLs per environment
from typing import Any, Optional
import requests


class EndPoint:


    FIMS_URL ={
            "dev": "https://d32k9x3lmi2sdi.cloudfront.net",
            "uat": "https://d2drkhmmovtf5u.cloudfront.net",
            "prod": "https://fims.prod.six-mt.com"
        }
    CONTENT_URL = {
            "dev": "https://d376sgfm22b4hx.cloudfront.net",
            "uat": "https://d2es6ucq9ddbh1.cloudfront.net",
            "prod": "https://content.prod.six-mt.com"
        }


    # Endpoint paths relative to base
    PATHS = {
        # No args
        "ALL_PARKS": "/content/all-parks",
        "ALL_PARKS_OPERATING_HOURS": "/operating-hours/all-parks",
        # Park ID as args
        "PRODUCT_LIST": "/content/product-list/park/{park_id}",
        "EVENTS": "/content/events/park/{park_id}",
        "MORE_LINK_LIST": "/content/link-list/park/{park_id}",
        "FEATURED_POI'S": "/content/poi-list/park/{park_id}",
        "PRODUCT_TAXONOMY": "/content/product-taxonomy/park/{park_id}",
        "LOYALTY_ENTITLEMENTS": "/content/loyalty-entitlement/park/{park_id}",
        "POI_DETAILS": "/poi/park/{park_id}",
        "WAIT_TIMES": "/wait-times/park/{park_id}",
        "VENUE_STATUS": "/venue-status/park/{park_id}",
        "MOBILE_APP_BANNER": "/content/mobile-app-banner/park/{park_id}",
        # Park id , date as args
        "OPERATING_HOURS_BY_DATE": "/operating-hours/park/{park_id}?date={date}",
        # Park id , month as args
        "OPERATING_HOURS_BY_MONTH": "/operating-hours/park/{park_id}?date={year_month}",
    }



    """
            six flags america : 909
            canada's wonderland : 40
            california’s great america : 35
            carowinds : 30
            castaway bay : 203
            cedar point sports center : 204
            cedar point : 1
            six flags darien lake : 945
            six flags darien lake hotel & campground : 999
            six flags discovery kingdom : 936
            dorney park : 8
            six flags fiesta texas : 914
            six flags great adventure : 905
            frontier city : 943
            six flags great america : 910
            great escape : 924
            six flags great escape lodge : 923
            six flags hurricane harbor, chicago : 920
            hurricane harbor, concord : 942
            six flags hurricane harbor, los angeles : 911
            six flags hurricane harbor, jackson : 925
            hurricane harbor, rockford : 948
            hurricane harbor, oklahoma city : 944
            hurricane harbor, oaxtepec : 959
            hurricane harbor, arlington : 913
            kings dominion : 25
            la ronde : 969
            six flags mexico : 960
            knott's berry farm : 4
            kings island : 20
            six flags magic mountain : 906
            michigan’s adventure : 12
            six flags over texas : 901
            six flags over georgia : 902
            six flags new england : 935
            hurricane harbor, phoenix : 946
            six flags savannah sunset resort & spa : 50
            schlitterbahn galveston : 27
            sawmill creek resort : 999
            schlitterbahn new braunfels : 26
            valleyfair : 14
            six flags st. louis : 903
            hurricane harbor, splashtown : 947
            six flags white water : 922
            worlds of fun : 6
    """
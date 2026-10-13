from typing import cast

import requests
from tabulate import tabulate

from get_api.end_points import EndPoint
from get_api.park_name_and_park_id import ParkManager


def get_wait_time(park_name: str, park_id: int, env: str = "prod"):

    url = EndPoint.get_url(
        "WAIT_TIMES",
        env,
        park_id=park_id
    )

    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        print(
            f"Request failed with status code: "
            f"{response.status_code}"
        )
        return None

    data = response.json()

    rows = []

    for venue in data["venues"]:
        for ride in venue["details"]:
            rows.append([
                ride["fimsId"],
                venue["venueName"],
                ride["name"],
                "Yes" if ride["isFastLane"] else "No",
                ride["regularWaittime"]["waitTime"],
                ride["fastlaneWaittime"]["waitTime"]
            ])

    headers = [
        "FIMS ID",
        "Category",
        "Ride",
        "Fast Lane",
        "Regular Wait",
        "Fast Lane Wait"
    ]

    print(f"\nPark      : {data['parkName']}")
    print(f"Park ID   : {data['parkId']}")
    print(f"Date      : {data['parkDateTime']}\n")

    print(
        tabulate(
            rows,
            headers=headers,
            tablefmt="rounded_outline"
        )
    )

    return data


if __name__ == "__main__":

    env = "uat"
    park_name = "carowinds"

    park_id = cast(
        int,
        ParkManager(env).get_park_id(park_name)
    )

    result = get_wait_time(
        park_name,
        park_id,
        env
    )

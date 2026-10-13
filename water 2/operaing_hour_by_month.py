from datetime import datetime
from typing import Any
import requests

BASE_URLS = {
    "uat": "https://d3f9rays5zpug9.cloudfront.net",
    "prod": "https://fims.prod.six-mt.com",
}


# METHOD 1: Fetch raw JSON data from API
def fetch_operating_hours_data(
        park_id: str | int, month: str, env: str = "uat"
) -> dict[str, Any] | list[Any]:
    clean_park_id = str(int(park_id))
    env_key = env.strip().lower()

    if env_key not in BASE_URLS:
        raise ValueError(
            f"Unsupported environment '{env}'. Choose 'uat' or 'prod'."
        )

    url = f"{BASE_URLS[env_key]}/operating-hours/park/{clean_park_id}"
    response = requests.get(url, params={"date": month}, timeout=10)
    response.raise_for_status()
    return response.json()


# METHOD 2: Process payload, reformat date to DD/MM/YYYY, and capture hours
def process_operating_hours(
        raw_data: dict[str, Any] | list[Any], default_park_id: str | int
) -> list[dict[str, Any]]:
    processed_records = []

    if isinstance(raw_data, dict):
        park_name = raw_data.get("parkName", "N/A")
        dates_list = raw_data.get("dates", [])
        park_id = str(raw_data.get("parkId", default_park_id))
    elif isinstance(raw_data, list):
        park_name = "N/A"
        dates_list = raw_data
        park_id = str(default_park_id)
    else:
        return []

    for day in dates_list:
        if not isinstance(day, dict):
            continue

        raw_date_str = day.get("date", "")

        # Convert MM/DD/YYYY to DD/MM/YYYY
        formatted_date = "N/A"
        if raw_date_str:
            try:
                dt = datetime.strptime(raw_date_str.strip(), "%m/%d/%Y")
                formatted_date = dt.strftime("%d/%m/%Y")  # Output format: DD/MM/YYYY
            except ValueError:
                formatted_date = raw_date_str

        is_closed = day.get("isParkClosed", True)
        time_entries = []

        if not is_closed:
            # 1. Parse 'operatings' array (Main Park, Waterpark, etc.)
            for op in day.get("operatings", []):
                op_type = op.get("operatingTypeName", "").strip()
                for item in op.get("items", []):
                    label = item.get("assignmentDisplayName") or op_type or "Theme Park"
                    t_from = item.get("timeFrom", "").strip()
                    t_to = item.get("timeTo", "").strip()
                    if t_from and t_to:
                        time_entries.append((label, t_from, t_to))

            # 2. Fallback to 'venues' array if 'operatings' is empty
            if not time_entries:
                for venue in day.get("venues", []):
                    venue_name = venue.get("venueName", "").strip()
                    for assign in venue.get("assignmentHours", []):
                        t_from = assign.get("timeFrom", "").strip()
                        t_to = assign.get("timeTo", "").strip()
                        if t_from and t_to:
                            time_entries.append((venue_name, t_from, t_to))

        # Deduplicate while preserving order
        unique_entries = list(dict.fromkeys(time_entries))

        processed_records.append(
            {
                "park_id": park_id,
                "park_name": park_name,
                "date": formatted_date,
                "is_closed": is_closed,
                "time_entries": unique_entries,
            }
        )

    return processed_records


# METHOD 3: Format 24-hr time ranges into 12-hr AM/PM string with labels
def format_time_ranges(time_entries: list[tuple[str, str, str]]) -> str:
    if not time_entries:
        return "N/A"

    formatted_list = []
    for label, t_from, t_to in time_entries:
        try:
            from_12 = datetime.strptime(t_from, "%H:%M").strftime("%I:%M %p")
            to_12 = datetime.strptime(t_to, "%H:%M").strftime("%I:%M %p")
            formatted_list.append(f"{label}: {from_12} - {to_12}")
        except ValueError:
            formatted_list.append(f"{label}: {t_from} - {t_to}")

    return ", ".join(formatted_list)


# METHOD 4: Display formatted output
def display_output(records: list[dict[str, Any]]) -> None:
    for rec in records:
        status_str = "Closed" if rec["is_closed"] else "Open"
        hours_str = format_time_ranges(rec["time_entries"])

        print(
            f'"{rec["date"]}"  "{status_str}" "{hours_str}"  "{rec["park_name"]}" "{rec["park_id"]}"'
        )


# MAIN CONTROLLER
def by_month(park_id: str | int, month: str, env: str = "uat") -> None:
    raw_data = fetch_operating_hours_data(park_id, month, env)
    records = process_operating_hours(raw_data, default_park_id=park_id)
    display_output(records)


if __name__ == "__main__":
    by_month("30", "202608","prod")
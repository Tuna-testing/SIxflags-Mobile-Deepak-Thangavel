import requests

from page.base_page import BasePage
from utils import PropertyReader


def get_customer_entitlements(
    auth_token: str, waf_token: str, site_code: str = "CA"
):
    """Fetches customer entitlements from dev.six-mt.com using fresh tokens."""
    url = "https://dev.six-mt.com/v2/customer/entitlements"

    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Cookie": f"aws-waf-token={waf_token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "ktor-client",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
    }

    params = {"siteCode": site_code}

    return  requests.get(url, headers=headers, params=params)



if __name__ == "__main__":
    # Pass your fresh tokens here at launch
    FRESH_AUTH_TOKEN = PropertyReader.get_prop("authToken")
    FRESH_WAF_TOKEN = PropertyReader.get_prop("wafToken")
    response = get_customer_entitlements(FRESH_AUTH_TOKEN, FRESH_WAF_TOKEN)

    print(f"Status Code: {response.status_code}\n")

    if response.status_code == 200:
        data = response.json()
        print("Response JSON:")
        print(data)
    else:
        print("Failed to fetch data:")
        print(response.text)
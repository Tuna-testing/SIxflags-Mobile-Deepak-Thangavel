import requests

class RestAssured:

    @staticmethod
    def get_response(endpoint: str, ) -> list[dict] | dict:
        return (
            RestAssured()
            .given()
            .header("Accept", "application/json")
            .when()
            .get(endpoint)
            .then()
            .status_code(200)
            .extract_json()
        )

    def __init__(self):
        self.base_url = ""
        self.headers = {}
        self.response = None

    def given(self):
        return self

    def header(self, key, value):
        self.headers[key] = value
        return self

    def when(self):
        return self

    def get(self, url):
        self.response = requests.get(url, headers=self.headers)
        return self

    def then(self):
        return self

    def status_code(self, expected_code):
        assert self.response.status_code == expected_code, f"Expected {expected_code}, got {self.response.status_code}"
        return self

    def extract_json(self):
        return self.response.json()



import re
import time
import requests


class OTPReader:
    BASE_URL = "https://api.mail.tm"

    # Step 1: Auth token
    @classmethod
    def auth(cls) -> str:
        url = f"{cls.BASE_URL}/token"
        payload = {
            "address": "olivefrancine@chefalicious.com",
            "password": "G%CJP6~x9O",
        }
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            token = response.json().get("token")
            return token
        except Exception as e:
            print(f"❌ Failed to generate token: {e}")
            raise e

    # Step 2: Get all messages
    @classmethod
    def get_all_messages(cls, token: str) -> list:
        url = f"{cls.BASE_URL}/messages?page=1"
        headers = {"Authorization": f"Bearer {token}"}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json().get("hydra:member", [])
        except Exception as e:
            print(f"❌ Failed to fetch messages: {e}")
            return []

    # Step 3: Get latest message ID
    @staticmethod
    def get_latest_message_id(messages: list) -> str:
        if messages:
            message_id = messages[0].get("id")
            print(f"📨 Latest message ID: {message_id}")
            return message_id
        else:
            print("📭 No messages found.")
            return None

    # Step 4: Read message & extract OTP
    @classmethod
    def read_message(cls, message_id: str, token: str) -> str:
        if not message_id:
            return None

        url = f"{cls.BASE_URL}/messages/{message_id}"
        headers = {"Authorization": f"Bearer {token}"}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            message_data = response.json()

            html_array = message_data.get("html", [])
            if html_array:
                html_content = html_array[0]
                otp = cls.extract_last_6_digits(html_content)
                return otp
        except Exception as e:
            print(f"❌ Failed to read message: {e}")

        return None

    # Step 5: Delete message (Optional / Commentable)
    @classmethod
    def delete_message(cls, message_id: str, token: str) -> None:
        if not message_id:
            return

        url = f"{cls.BASE_URL}/messages/{message_id}"
        headers = {"Authorization": f"Bearer {token}"}

        try:
            response = requests.delete(url, headers=headers)
            response.raise_for_status()
            print(f"🗑️ Message deleted: {message_id}")
        except Exception as e:
            print(f"❌ Failed to delete message: {e}")

    # Helper: Extract 6-digit OTP regex
    @staticmethod
    def extract_last_6_digits(html_content: str) -> str:
        matches = re.findall(r"\b\d{6}\b", html_content)
        return matches[-1] if matches else None

    # Step 6: Sequential Orchestrator (Exact match to your Java flow)
    @classmethod
    def get_otp(cls, timeout_seconds: int = 60, poll_interval: int = 5) -> str:
        start_time = time.time()

        while time.time() - start_time < timeout_seconds:
            # 1. Get token
            token = cls.auth()
            print("*********************")
            print(f"The Token is {token}")
            print("*********************")

            # 2. Get all messages
            all_messages = cls.get_all_messages(token)
            print("*********************")
            print(f"The message array is {all_messages}")
            print("*********************")

            # 3. Get latest message ID
            message_id = cls.get_latest_message_id(all_messages)
            print("*********************")
            print(f"The current message ID {message_id}")
            print("*********************")

            if message_id:
                # 4. Read message content & get OTP
                otp = cls.read_message(message_id, token)
                print("*********************")
                print(f"The OTP is {otp}")
                print("*********************")

                if otp:
                    # 5. Delete message (Comment out this single line whenever you don't want to delete)
                   # cls.delete_message(message_id, token)

                    # 6. Return OTP
                    return otp

            print(f"⏳ Message not ready yet. Retrying in {poll_interval}s...")
            time.sleep(poll_interval)

        raise TimeoutError(f"❌ Timed out after {timeout_seconds}s waiting for OTP email.")


if __name__ == "__main__":
    OTPReader.get_otp()
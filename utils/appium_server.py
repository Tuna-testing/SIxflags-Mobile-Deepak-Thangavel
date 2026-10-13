import os
import socket
import time
import urllib.request
from urllib.error import HTTPError, URLError
from appium.webdriver.appium_service import AppiumService


class AppiumServerManager:
    """Utility class to programmatically start, stop, and manage Appium server instances."""

    @staticmethod
    def get_free_system_port(start_port: int = 8201, end_port: int = 8299) -> int:
        """Finds a free port for the Appium HTTP server outside the systemPort range (8200-8299)."""
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("", 0))
                port = s.getsockname()[1]
                # Keep HTTP server completely outside 8200-8299
                if not (8200 <= port <= 8299):
                    return port

    @staticmethod
    def _wait_for_server(url: str, timeout: int = 15) -> bool:
        start_time = time.time()
        status_url = f"{url}/status"

        while time.time() - start_time < timeout:
            try:
                with urllib.request.urlopen(status_url, timeout=1) as response:
                    if response.status == 200:
                        return True
            except (URLError, HTTPError, TimeoutError, OSError):
                time.sleep(0.5)
        return False

    @classmethod
    def start(cls, port: int = None, worker_id: str = None) -> tuple[str, AppiumService]:
        if port is None:
            port = cls.get_free_system_port()

        log_dir = os.path.join(os.getcwd(), "logs", "appium")
        os.makedirs(log_dir, exist_ok=True)

        worker_suffix = f"_{worker_id}" if worker_id else ""
        log_filename = f"Appium_{time.strftime('%Y%m%d_%H%M%S')}{worker_suffix}.log"
        log_file_path = os.path.join(log_dir, log_filename)

        service = AppiumService()

        try:
            service.start(args=[
                '--log', log_file_path,
                '--log-level', 'debug',
                '--relaxed-security',
                '--port', str(port),
            ])

            url = f"http://127.0.0.1:{port}"

            if not cls._wait_for_server(url, timeout=15):
                raise RuntimeError(f"Appium server started on port {port} but failed health check polling.")

            print(f"[INFO] Appium Server started for worker '{worker_id or 'main'}' at {url}")
            return url, service

        except Exception as e:
            print(f"[ERROR] Failed to start Appium server on port {port}: {e}")
            if service.is_running:
                service.stop()
            raise e

    @staticmethod
    def stop(service: AppiumService):
        if service and service.is_running:
            service.stop()
            print("[INFO] Appium server stopped successfully.")

import requests
from enum import Enum
from umcn_consent.auth import AuthHandler
from umcn_consent.config import Config
from umcn_consent.error_handler import ErrorHandler


class AuthenticatedClient:
    def __init__(self):
        self.session = AuthHandler.authenticate()

    def fetch_data(self, pid):
        """
        Retrieves patient data for a given patient ID (PID)
        by making an HTTP request to a configured URL.

        Parameters
        ----------
        pid : str
            The patient ID to fetch data for.

        Returns
        -------
        dict
            Patient data as JSON, or None if an error occurs
            (e.g., empty PID, no session, invalid URL, or HTTP error).
        """
        if not pid or not pid.strip():
            ErrorHandler.handle_gen_error("Invalid patient ID, PID cannot be empty.")
            return None

        if not self.session:
            return None

        url = Config.get_url()
        if not url:
            ErrorHandler.handle_gen_error("Invalid URL.")
            return None

        full_url = f"{url}{pid}"
        response = None

        try:
            response = self.session.get(full_url)
            response.raise_for_status()
            print(response.text)
            data = response.json()
            status = self.parse_status(data)
            print(f"\nConsent Status: {status}")

        except requests.exceptions.HTTPError:
            ErrorHandler.handle_http_error(response)
            print(response.text)

    @staticmethod
    def parse_status(data):
        consent_status_str = data["entry"][0]["resource"]["status"]["code"].lower()

        try:
            consent_status = ConsentStatus(consent_status_str)
            if consent_status == ConsentStatus.ACTIVE:
                return True
            elif consent_status == ConsentStatus.REJECTED:
                return False
        except ValueError as err:
            raise ValueError("Consent status not recognized.") from err


class ConsentStatus(Enum):
    ACTIVE = "active"
    REJECTED = "rejected"

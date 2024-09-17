import requests
from umcn_consent.config import Config


class AuthHandler:
    @staticmethod
    def authenticate():
        """
        Initializes an authenticated requests session based on configuration data.

        Returns
        -------
        requests.Session or None
            An authenticated session if the data is correct, or None if required
            configuration data is missing or in case of an error.

        """
        username = Config.get_user()
        password = Config.get_password()

        if not username or not password:
            return None

        client_id = Config.get_client_id()
        auth_token = Config.get_auth_token()

        if not client_id or not auth_token:
            return None

        try:
            session = requests.sessions.Session()
            session.auth = (username, password)
            session.headers.update(
                {
                    "Client-ID": client_id,
                    "Authorization": auth_token,
                }
            )
            print(session is None)
            return session
        except requests.RequestException as e:
            print(e)
            return None

import os
from dotenv import load_dotenv
from umcn_consent.error_handler import ErrorHandler

load_dotenv()


class Config:
    # Template Design Pattern
    @staticmethod
    def get_env_variable(var_name):
        value = os.getenv(var_name)

        if not value:
            ErrorHandler.handle_missing_env(var_name)
            return None

        return value

    @staticmethod
    def get_user():
        return Config.get_env_variable("USER")

    @staticmethod
    def get_password():
        return Config.get_env_variable("PASSWORD")

    @staticmethod
    def get_url():
        return Config.get_env_variable("URL")

    @staticmethod
    def get_client_id():
        return Config.get_env_variable("CLIENT_ID")

    @staticmethod
    def get_auth_token():
        return Config.get_env_variable("AUTH_TOKEN")

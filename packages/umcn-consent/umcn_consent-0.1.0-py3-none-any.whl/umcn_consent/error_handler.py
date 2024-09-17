import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger()


class ErrorHandler:
    ERROR_MESSAGES = {  # HTTP Error codes
        401: "Unauthorized: Login credentials are invalid.",
        403: "Forbidden: You do not have permission to perform this operation.",
        404: "Not Found: Resource not found.",
        500: "Internal Server Error",
    }

    @staticmethod
    def handle_http_error(response):
        status_code = response.status_code
        error_message = ErrorHandler.ERROR_MESSAGES.get(status_code)
        logger.error(f"{status_code} {error_message}")

    @staticmethod
    def handle_missing_env(variable_name):
        logger.error(f"Environment variable {variable_name} is missing.")

    @staticmethod
    def handle_gen_error(error):
        logger.error(f"{error}")

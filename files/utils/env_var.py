from dotenv import load_dotenv
import os

load_dotenv()


def get_env_var(var: str) -> str | None:
    """Function that centralizes the search for variables in the locally loaded .env file

    :returns: Value the variable as string and if it doesn't find it returns None.
    """
    return os.getenv(var)
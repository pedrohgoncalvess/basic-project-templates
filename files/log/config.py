from datetime import datetime
from string import Template
import re
import os

from utils.env_var import get_env_var


class RelationalLogger:
    def __init__(self, log_format: str | None = None):
        self._log_file_dir_ = get_env_var('LOG_PATH') if get_env_var('LOG_PATH') is not None else "."
        self._log_file_format_ = f".{re.sub(r'[^a-zA-Z0-9]', '', log_format)}.log" if log_format else ".log"
        self._log_path_ = f"{self._log_file_dir_}\\{self._log_file_dir_}"
        self._env_ = get_env_var('ENV') if get_env_var('ENV') is not None else "dev"

        self.headers = ["MODE", "CREATED_AT", "MESSAGE", "OBS"]
        self.time_format = "%Y-%m-%d %H:%M%S"
        self.format = Template(f"""$mode | {datetime.now().strftime(self.time_format)} | $primary_message | $obs """)

        if not os.path.exists(self._log_path_):
            with open(self._log_path_, 'w') as f:
                f.write(" | ".join(self.headers))

    def _write_log_(self, log_message: str):
        with open(self._log_path_, 'a') as f:
            f.write(log_message)

    def error(self, error_type:str, exception: str | None = None):
        self._write_log_(self.format.substitute(mode="ERROR", primary_message=error_type, obs=exception if exception else "null"))

    def info(self, info_type:str, message:str):
        self._write_log_(self.format.substitute(mode="INFO", primary_message=info_type, obs=message))


# Customize your log formats and files
logger = RelationalLogger()
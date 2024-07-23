import logging
import logging.handlers
from colorama import Fore, Style, init

init(autoreset=True)  # (required for Windows)


class ColoredFormatter(logging.Formatter):
    COLORS = {
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "CRITICAL": Fore.RED + Style.BRIGHT,
    }

    def format(self, record):
        log_message = super().format(record)
        if record.levelname in self.COLORS:
            return f"{self.COLORS[record.levelname]}{log_message}{Style.RESET_ALL}"
        return log_message


def get_logger(name: str, level=logging.DEBUG) -> logging.Logger:
    name = name.split(".")[-1]
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        ColoredFormatter("%(asctime)s::%(name)s:: %(levelname)s: %(message)s")
    )

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(console_handler)
    return logger

import logging
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(show_path=False)]
)

# create file handler which logs messages
# fh = logging.FileHandler(PATHS.LOGS_FILE_PATH)
# fh.setLevel(logging.INFO)

log = logging.getLogger("rich")

if __name__ == '__main__':
    log.info("This is an info message")
    log.warning("This is a warning message")
    log.error("This is an error message")
    log.critical("This is a critical message")

import logging

from rich.logging import RichHandler

from decentnet.consensus.dev_constants import LOG_LEVEL


def setup_logger(debug: bool, logger):
    if not debug:
        logging.disable(logging.DEBUG)
    root = logging.getLogger()
    root.setLevel(logging.FATAL)
    logger.setLevel(LOG_LEVEL)
    logging.basicConfig(
        level=LOG_LEVEL if debug else logging.CRITICAL,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler()]
    )

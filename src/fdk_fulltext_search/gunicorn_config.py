from dotenv import load_dotenv
from os import environ as env
import sys
import logging
from gunicorn import glogging
import multiprocessing
from pythonjsonlogger import jsonlogger

load_dotenv()

PORT = env.get("HOST_PORT", "8080")
DEBUG_MODE = env.get("DEBUG_MODE", False)
LOG_LEVEL = env.get("LOG_LEVEL", "INFO")

# Gunicorn config
bind = ":" + PORT
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2 * multiprocessing.cpu_count()
loglevel = str(LOG_LEVEL)
accesslog = "-"


class StackdriverJsonFormatter(jsonlogger.JsonFormatter, object):
    """json log formatter."""

    def __init__(self, fmt="%(levelname) %(message)", style="%", *args, **kwargs):
        jsonlogger.JsonFormatter.__init__(self, fmt=fmt, *args, **kwargs)

    def process_log_record(self, log_record):
        log_record["severity"] = log_record["levelname"]
        del log_record["levelname"]
        return super(StackdriverJsonFormatter, self).process_log_record(log_record)


# Override the logger to remove healthcheck (ping) from the access log and format logs as json
class CustomGunicornLogger(glogging.Logger):
    def setup(self, cfg):
        super().setup(cfg)

        # Add filters to Gunicorn logger
        access_logger = logging.getLogger("gunicorn.access")
        access_logger.addFilter(PingFilter())
        access_logger.addFilter(ReadyFilter())

        root_logger = logging.getLogger()
        root_logger.setLevel(loglevel)

        other_loggers = [
            "gunicorn",
            "gunicorn.error",
            "gunicorn.http",
            "gunicorn.http.wsgi",
        ]
        loggers = [logging.getLogger(name) for name in other_loggers]
        loggers.append(root_logger)
        loggers.append(access_logger)

        json_handler = logging.StreamHandler(sys.stdout)
        json_handler.setFormatter(StackdriverJsonFormatter())

        for logger in loggers:
            for handler in logger.handlers:
                logger.removeHandler(handler)
            logger.addHandler(json_handler)


class PingFilter(logging.Filter):
    def filter(self, record):
        return "GET /ping" not in record.getMessage()


class ReadyFilter(logging.Filter):
    def filter(self, record):
        return "GET /ready" not in record.getMessage()


logger_class = CustomGunicornLogger

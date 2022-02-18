import logging
from logging.config import dictConfig


def set_log_config():
    """set_log_config"""
    log_conf = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "console": {
                "format": '{"@timestamp":"%(asctime)s",'
                          '"level":"%(levelname)s",'
                          '"message":"%(message)s"'
                          '}'
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "console",
                "stream": "ext://sys.stdout"
            }
        },
        "loggers": {
            "": {
                "name": "nyc_etl_pipeline",
                "level": "INFO",
                "handlers": [
                    "console"
                ],
                "propagate": 1,
                "qualname": "root"
            },
            "botocore": {
                "level": "WARNING"
            }
        }
    }
    logging.getLogger('werkzeug').disabled = True
    dictConfig(log_conf)


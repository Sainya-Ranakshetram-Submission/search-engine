import logging


class AutoreloadLogFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if record.name.find("django.utils.autoreload") != -1:
            return False
        return True


LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "console": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(log_color)s %(asctime)s | %(name)s/%(funcName)s | "
            "%(levelname)s:%(reset)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "filters": {
        "autoreloadFilter": {
            "()": AutoreloadLogFilter
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
            "filters": ["autoreloadFilter"],
        },
        "mail_admins": {
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "root": {
        "level": "DEBUG",
        "handlers": [
            "console",
        ],
    },
    "loggers": {
        "django": {
            "level": "DEBUG",
            "handlers": [
                "console",
            ],
        },
        "django.template": {
            "level": "ERROR",
            "handlers": [
                "console",
            ],
        },
    },
}
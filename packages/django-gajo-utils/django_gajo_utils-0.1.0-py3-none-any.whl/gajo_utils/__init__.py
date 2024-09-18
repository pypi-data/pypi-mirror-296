from django.conf import settings

DEFAULT_GAJO_UTILS_CONFIG = {
    "REQUEST_TIMER": False,
    "REQUEST_DELAY": False,
    "REQUEST_COOKIES": False,
    "RESPONSE_COOKIES": False,
    "RESPONSE_CONTENT": False,
    "RESPONSE_QUERIES": False,
}


def get_config():
    USER_CONFIG = getattr(settings, "GAJO_UTILS_CONFIG", {})
    return DEFAULT_GAJO_UTILS_CONFIG | USER_CONFIG

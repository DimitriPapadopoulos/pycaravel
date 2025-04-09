import enum


class WithRequester:
    API_URL = NotImplementedError

    def __init__(self, requester):
        self._requester = requester

    @property
    def requester(self):
        """Get requester instance"""
        # dynamically set API_URL for requester
        self._requester.API_URL = self.API_URL
        self._requester.SUCCESS_CODE = getattr(self, "SUCCESS_CODE", None)
        return self._requester


class OCSCode(enum.IntEnum):
    OK = 100
    SERVER_ERROR = 996
    NOT_AUTHORIZED = 997
    NOT_FOUND = 998
    UNKNOWN_ERROR = 999


class ShareType(enum.IntEnum):
    USER = 0
    GROUP = 1
    PUBLIC_LINK = 3
    FEDERATED_CLOUD_SHARE = 6
    CIRCLE = 7


class Permission(enum.IntEnum):
    """Permission for Share have to be sum of selected permissions."""

    READ = 1
    UPDATE = 2
    CREATE = 4
    DELETE = 8
    SHARE = 16
    ALL = 31


QUOTA_UNLIMITED = -3


def datetime_to_expire_date(date):
    return date.strftime("%Y-%m-%d")

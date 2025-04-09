import logging
from functools import wraps

import requests

from .response import OCSResponse, WebDAVResponse

logger = logging.getLogger("rlink")


class NextCloudConnectionError(Exception):
    """A connection error occurred."""


def catch_connection_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.RequestException as e:
            raise NextCloudConnectionError(
                "Failed to establish connection to NextCloud",
                getattr(e.request, "url", None),
                e,
            )

    return wrapper


class Requester:
    def __init__(self, endpoint, user, passwd, json_output=False, verify=True):
        self.query_components = []
        self.json_output = json_output
        self.verify = verify
        self.base_url = endpoint
        self.h_get = {"OCS-APIRequest": "true"}
        self.h_post = {
            "OCS-APIRequest": "true",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        self.auth_pk = (user, passwd)
        self.API_URL = None
        self.SUCCESS_CODE = None

    def rtn(self, resp):
        if self.json_output:
            return resp.json()
        else:
            return resp.content.decode("UTF-8")

    @catch_connection_error
    def get(self, url="", params=None):
        url = self.get_full_url(url)
        logger.debug(url)
        logger.debug(params)
        res = requests.get(
            url,
            auth=self.auth_pk,
            headers=self.h_get,
            params=params,
            verify=self.verify,
        )
        return self.rtn(res)

    @catch_connection_error
    def post(self, url="", data=None):
        url = self.get_full_url(url)
        logger.debug(url)
        logger.debug(data)
        res = requests.post(
            url, auth=self.auth_pk, data=data, headers=self.h_post, verify=self.verify
        )
        return self.rtn(res)

    @catch_connection_error
    def put(self, url="", data=None):
        url = self.get_full_url(url)
        logger.debug(url)
        res = requests.put(
            url, auth=self.auth_pk, data=data, headers=self.h_post, verify=self.verify
        )
        return self.rtn(res)

    @catch_connection_error
    def delete(self, url="", data=None):
        url = self.get_full_url(url)
        logger.debug(url)
        logger.debug(data)
        res = requests.delete(
            url, auth=self.auth_pk, data=data, headers=self.h_post, verify=self.verify
        )
        return self.rtn(res)

    def get_full_url(self, additional_url=""):
        """
        Build full url for request to NextCloud api

        Construct url from self.base_url, self.API_URL, additional_url
        (if given), add format=json param if self.json

        :param additional_url: str
            add to url after api_url
        :return: str
        """
        if additional_url and not str(additional_url).startswith("/"):
            additional_url = f"/{additional_url}"

        if self.json_output:
            self.query_components.append("format=json")

        ret = f"{self.base_url}{self.API_URL}{additional_url}"

        if self.json_output:
            ret += "?format=json"
        return ret


class OCSRequester(Requester):
    """Requester for OCS API."""

    def rtn(self, resp):
        return OCSResponse(
            response=resp, json_output=self.json_output, success_code=self.SUCCESS_CODE
        )


class WebDAVRequester(Requester):
    """Requester for WebDAV API."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def rtn(self, resp, data=None):
        return WebDAVResponse(response=resp, data=data)

    @catch_connection_error
    def propfind(self, additional_url="", headers=None, data=None):
        url = self.get_full_url(additional_url=additional_url)
        res = requests.request(
            "PROPFIND",
            url,
            auth=self.auth_pk,
            headers=headers,
            data=data,
            verify=self.verify,
        )
        return self.rtn(res)

    @catch_connection_error
    def proppatch(self, additional_url="", data=None):
        url = self.get_full_url(additional_url=additional_url)
        res = requests.request("PROPPATCH", url, auth=self.auth_pk, data=data)
        return self.rtn(resp=res)

    @catch_connection_error
    def report(self, additional_url="", data=None):
        url = self.get_full_url(additional_url=additional_url)
        res = requests.request(
            "REPORT", url, auth=self.auth_pk, data=data, verify=self.verify
        )
        return self.rtn(resp=res)

    @catch_connection_error
    def download(self, url="", params=None):
        url = self.get_full_url(url)
        logger.debug(url)
        logger.debug(params)
        res = requests.get(
            url,
            auth=self.auth_pk,
            headers=self.h_get,
            params=params,
            verify=self.verify,
        )
        return self.rtn(resp=res, data=res.content)

    @catch_connection_error
    def make_collection(self, additional_url=""):
        url = self.get_full_url(additional_url=additional_url)
        res = requests.request("MKCOL", url=url, auth=self.auth_pk, verify=self.verify)
        return self.rtn(resp=res)

    @catch_connection_error
    def move(self, url, destination, overwrite=False):
        url = self.get_full_url(additional_url=url)
        destination_url = self.get_full_url(additional_url=destination)
        logger.debug(f"{url} -> {destination_url}")
        headers = {
            "Destination": destination_url.encode("utf-8"),
            "Overwrite": "T" if overwrite else "F",
        }
        res = requests.request(
            "MOVE", url=url, auth=self.auth_pk, headers=headers, verify=self.verify
        )
        return self.rtn(resp=res)

    @catch_connection_error
    def copy(self, url, destination, overwrite=False):
        url = self.get_full_url(additional_url=url)
        destination_url = self.get_full_url(additional_url=destination)
        logger.debug(f"{url} -> {destination_url}")
        headers = {
            "Destination": destination_url,
            "Overwrite": "T" if overwrite else "F",
        }
        res = requests.request(
            "COPY", url=url, auth=self.auth_pk, headers=headers, verify=self.verify
        )
        return self.rtn(resp=res)

from .api_wrappers import OCS_API_CLASSES, WEBDAV_CLASS
from .requester import OCSRequester, WebDAVRequester


class NextCloud:
    """NextCloud API class: allows OCS and WebDav requests."""

    def __init__(self, endpoint, user, password, json_output=True, verify=True):
        self.query_components = []

        ocs_requester = OCSRequester(endpoint, user, password, json_output, verify)
        webdav_requester = WebDAVRequester(endpoint, user, password, verify=verify)

        self.functionality_classes = [
            api_class(ocs_requester) for api_class in OCS_API_CLASSES
        ]
        self.functionality_classes.append(
            WEBDAV_CLASS(webdav_requester, json_output=json_output)
        )

        for functionality_class in self.functionality_classes:
            for potential_method in dir(functionality_class):
                if potential_method.startswith("_") or not callable(
                    getattr(functionality_class, potential_method)
                ):
                    continue
                setattr(
                    self,
                    potential_method,
                    getattr(functionality_class, potential_method),
                )

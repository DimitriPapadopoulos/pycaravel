from ..base import WithRequester


class Capabilities(WithRequester):
    API_URL = "/ocs/v1.php/cloud/capabilities"
    SUCCESS_CODE = 100

    def get_capabilities(self):
        """Obtain capabilities provided by the Nextcloud server and its apps."""
        return self.requester.get()

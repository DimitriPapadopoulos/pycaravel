from ..base import WithRequester


class Forms(WithRequester):
    API_URL = "/ocs/v2.php/apps/forms/api/v1"

    def get_forms(self):
        """Retrieve a list of forms from the Nextcloud server."""
        url = "forms"
        return self.requester.get(url)

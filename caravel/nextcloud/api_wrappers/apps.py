from ..base import WithRequester


class Apps(WithRequester):
    API_URL = "/ocs/v1.php/cloud/apps"
    SUCCESS_CODE = 100

    def get_apps(self, filter=None):
        """Get a list of apps installed on the Nextcloud server."""
        params = {"filter": filter}
        return self.requester.get(params=params)

    def get_app(self, app_id):
        """Provide information on a specific application."""
        return self.requester.get(app_id)

    def enable_app(self, app_id):
        """Enable an app."""
        return self.requester.post(app_id)

    def disable_app(self, app_id):
        """Disable the specified app."""
        return self.requester.delete(app_id)

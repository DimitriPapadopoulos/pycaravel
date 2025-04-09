from ..base import WithRequester


class Activity(WithRequester):
    API_URL = "/ocs/v2.php/apps/activity/api/v2/activity"
    SUCCESS_CODE = 200

    def get_activities(
        self, since=None, limit=None, object_type=None, object_id=None, sort=None
    ):
        """Get an activity feed showing your file changes and other
        interesting things going on in your Nextcloud
        """
        params = {
            "since": since,
            "limit": limit,
            "object_type": object_type,
            "object_id": object_id,
            "sort": sort,
        }
        if params["object_type"] and params["object_id"]:
            return self.requester.get(url="filter", params=params)
        return self.requester.get(params=params)

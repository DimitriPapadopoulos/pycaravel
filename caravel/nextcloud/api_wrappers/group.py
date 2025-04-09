from ..base import WithRequester


class Group(WithRequester):
    API_URL = "/ocs/v1.php/cloud/groups"
    SUCCESS_CODE = 100

    def get_groups(self, search=None, limit=None, offset=None):
        """Retrieve a list of groups from the Nextcloud server."""
        params = {"search": search, "limit": limit, "offset": offset}
        return self.requester.get(params=params)

    def add_group(self, gid):
        """Add a new group."""
        msg = {"groupid": gid}
        return self.requester.post("", msg)

    def get_group(self, gid):
        """Retrieve a list of group members."""
        return self.requester.get(f"{gid}")

    def get_subadmins(self, gid):
        """List subadmins of the group."""
        return self.requester.get(f"{gid}/subadmins")

    def delete_group(self, gid):
        """Remove a group."""
        return self.requester.delete(f"{gid}")

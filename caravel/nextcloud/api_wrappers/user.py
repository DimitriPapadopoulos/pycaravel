from ..base import WithRequester


class User(WithRequester):
    API_URL = "/ocs/v1.php/cloud/users"
    SUCCESS_CODE = 100

    def add_user(self, uid, passwd):
        """Create a new user on the Nextcloud server."""
        msg = {"userid": uid, "password": passwd}
        return self.requester.post("", msg)

    def get_users(self, search=None, limit=None, offset=None):
        """Retrieve a list of users from the Nextcloud server."""
        params = {"search": search, "limit": limit, "offset": offset}
        return self.requester.get(params=params)

    def get_user(self, uid):
        """Retrieve information about a single user."""
        return self.requester.get(f"{uid}")

    def edit_user(self, uid, what, value):
        """Edit attributes related to a user.

        Users are able to edit email, displayname and password; admins can
        also edit the quota value.
        """
        what_to_key_map = {
            "email": "email",
            "quota": "quota",
            "phone": "phone",
            "address": "address",
            "website": "website",
            "twitter": "twitter",
            "displayname": "displayname",
            "password": "password",
        }
        assert what in what_to_key_map, (
            "You have chosen to edit user's '{what}', but you can choose only"
            "from: {choices}".format(
                what=what, choices=", ".join(what_to_key_map.keys())
            )
        )
        url = f"{uid}"
        msg = {
            "key": what_to_key_map[what],
            "value": value,
        }
        return self.requester.put(url, msg)

    def disable_user(self, uid):
        """Disable a user on the Nextcloud server so that the user cannot
        login anymore.
        """
        return self.requester.put(f"{uid}/disable")

    def enable_user(self, uid):
        """Enable a user on the Nextcloud server so that the user can login
        again.
        """
        return self.requester.put(f"{uid}/enable")

    def delete_user(self, uid):
        """Delete a user from the Nextcloud server."""
        return self.requester.delete(f"{uid}")

    def add_to_group(self, uid, gid):
        """Add the specified user to the specified group."""
        url = f"{uid}/groups"
        msg = {"groupid": gid}
        return self.requester.post(url, msg)

    def remove_from_group(self, uid, gid):
        """Remove the specified user from the specified group."""
        url = f"{uid}/groups"
        msg = {"groupid": gid}
        return self.requester.delete(url, msg)

    def create_subadmin(self, uid, gid):
        """Make a user the subadmin of a group."""
        url = f"{uid}/subadmins"
        msg = {"groupid": gid}
        return self.requester.post(url, msg)

    def remove_subadmin(self, uid, gid):
        """Remove the subadmin rights for the user specified from the group
        specified.
        """
        url = f"{uid}/subadmins"
        msg = {"groupid": gid}
        return self.requester.delete(url, msg)

    def get_subadmin_groups(self, uid):
        """Get the groups in which the user is a subadmin."""
        url = f"{uid}/subadmins"
        return self.requester.get(url)

    def resend_welcome_mail(self, uid):
        """Trigger the welcome email for this user again."""
        url = f"{uid}/welcome"
        return self.requester.post(url)

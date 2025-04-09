from ..base import ShareType, WithRequester


class Share(WithRequester):
    API_URL = "/ocs/v2.php/apps/files_sharing/api/v1"
    LOCAL = "shares"
    SUCCESS_CODE = 200

    def get_local_url(self, additional_url=""):
        if additional_url:
            return f"{self.LOCAL}/{additional_url}"
        return self.LOCAL

    @staticmethod
    def validate_share_parameters(path, share_type, share_with):
        """Check if share parameters make sense."""
        return (
            path is not None
            and isinstance(share_type, int)
            and (
                share_with is not None
                or share_type
                not in {
                    ShareType.GROUP,
                    ShareType.USER,
                    ShareType.FEDERATED_CLOUD_SHARE,
                    ShareType.CIRCLE,
                }
            )
        )

    def get_shares(self):
        """Get all shares from the user."""
        return self.requester.get(self.get_local_url())

    def get_shares_from_path(self, path, reshares=None, subfiles=None):
        """Get all shares from a given file/folder."""
        url = self.get_local_url()
        params = {
            "path": path,
            # TODO: test reshares, subfiles
            "reshares": (None if reshares is None else str(bool(reshares)).lower()),
            "subfiles": (None if subfiles is None else str(bool(subfiles)).lower()),
        }
        return self.requester.get(url, params=params)

    def get_share_info(self, sid):
        """Get information about a given share."""
        return self.requester.get(self.get_local_url(sid))

    def create_share(
        self,
        path,
        share_type,
        share_with=None,
        public_upload=None,
        password=None,
        permissions=None,
    ):
        """Share a file/folder with a user/group or as public link.

        Mandatory fields: share_type, path and share_with for share_type USER
        (0) or GROUP (1).
        """
        if not self.validate_share_parameters(path, share_type, share_with):
            raise ValueError("Unexpected input parameters.")

        url = self.get_local_url()
        if public_upload:
            public_upload = "true"

        data = {"path": path, "shareType": share_type}
        if share_type in [
            ShareType.GROUP,
            ShareType.USER,
            ShareType.FEDERATED_CLOUD_SHARE,
        ]:
            data["shareWith"] = share_with
        if public_upload:
            data["publicUpload"] = public_upload
        if share_type == ShareType.PUBLIC_LINK and password is not None:
            data["password"] = str(password)
        if permissions is not None:
            data["permissions"] = permissions
        return self.requester.post(url, data)

    def delete_share(self, sid):
        """Remove the given share."""
        return self.requester.delete(self.get_local_url(sid))

    def update_share(
        self, sid, permissions=None, password=None, public_upload=None, expire_date=""
    ):
        """Update a given share, only one value can be updated per request."""
        if permissions is not None:
            permissions = int(permissions)
        params = {
            "permissions": permissions,
            "password": password,
            "expireDate": expire_date,
        }
        if public_upload:
            params["publicUpload"] = "true"
        if public_upload is False:
            params["publicUpload"] = "false"

        # check if only one param specified
        specified_params_count = sum(int(bool(each)) for each in params.values())
        if specified_params_count > 1:
            raise ValueError(
                "Only one parameter for update can be specified per request"
            )

        url = self.get_local_url(sid)
        return self.requester.put(url, data=params)

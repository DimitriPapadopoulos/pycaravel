from ..base import WithRequester


class GroupFolders(WithRequester):
    API_URL = "/apps/groupfolders/folders"
    SUCCESS_CODE = 100

    def get_group_folders(self):
        """Return a list of call configured folders and their settings."""
        return self.requester.get()

    def get_group_folder(self, fid):
        """Return a specific configured folder and it's settings."""
        return self.requester.get(fid)

    def create_group_folder(self, mountpoint):
        """Create a new group folder."""
        return self.requester.post(data={"mountpoint": mountpoint})

    def delete_group_folder(self, fid):
        """Delete a group folder."""
        return self.requester.delete(fid)

    def grant_access_to_group_folder(self, fid, gid):
        """Give a group access to a folder."""
        url = "/".join([str(fid), "groups"])
        return self.requester.post(url, data={"group": gid})

    def revoke_access_to_group_folder(self, fid, gid):
        """Remove access from a group to a folder."""
        url = "/".join([str(fid), "groups", gid])
        return self.requester.delete(url)

    def set_permissions_to_group_folder(self, fid, gid, permissions):
        """Set the permissions a group has in a folder."""
        url = "/".join([str(fid), "groups", gid])
        return self.requester.post(url=url, data={"permissions": permissions})

    def set_quota_of_group_folder(self, fid, quota):
        """Set the quota for a folder in bytes."""
        url = "/".join([str(fid), "quota"])
        return self.requester.post(url, {"quota": quota})

    def rename_group_folder(self, fid, mountpoint):
        """Change the name of a folder."""
        url = "/".join([str(fid), "mountpoint"])
        return self.requester.post(url=url, data={"mountpoint": mountpoint})

import re

from ..base import WithRequester


class UserLDAP(WithRequester):
    API_URL = "/ocs/v2.php/apps/user_ldap/api/v1/config"
    SUCCESS_CODE = 200

    CONFIG_KEYS = [
        "ldapHost",
        "ldapPort",
        "ldapBackupHost",
        "ldapBackupPort",
        "ldapBase",
        "ldapBaseUsers",
        "ldapBaseGroups",
        "ldapAgentName",
        "ldapAgentPassword",
        "ldapTLS",
        "turnOffCertCheck",
        "ldapUserDisplayName",
        "ldapGidNumber",
        "ldapUserFilterObjectclass",
        "ldapUserFilterGroups",
        "ldapUserFilter",
        "ldapUserFilterMode",
        "ldapGroupFilter",
        "ldapGroupFilterMode",
        "ldapGroupFilterObjectclass",
        "ldapGroupFilterGroups",
        "ldapGroupMemberAssocAttr",
        "ldapGroupDisplayName",
        "ldapLoginFilter",
        "ldapLoginFilterMode",
        "ldapLoginFilterEmail",
        "ldapLoginFilterUsername",
        "ldapLoginFilterAttributes",
        "ldapQuotaAttribute",
        "ldapQuotaDefault",
        "ldapEmailAttribute",
        "ldapCacheTTL",
        "ldapUuidUserAttribute",
        "ldapUuidGroupAttribute",
        "ldapOverrideMainServer",
        "ldapConfigurationActive",
        "ldapAttributesForUserSearch",
        "ldapAttributesForGroupSearch",
        "ldapExperiencedAdmin",
        "homeFolderNamingRule",
        "hasPagedResultSupport",
        "hasMemberOfFilterSupport",
        "useMemberOfToDetectMembership",
        "ldapExpertUsernameAttr",
        "ldapExpertUUIDUserAttr",
        "ldapExpertUUIDGroupAttr",
        "lastJpegPhotoLookup",
        "ldapNestedGroups",
        "ldapPagingSize",
        "turnOnPasswordChange",
        "ldapDynamicGroupMemberURL",
        "ldapDefaultPPolicyDN",
    ]

    def create_ldap_config(self):
        """Create a new and empty LDAP configuration."""
        return self.requester.post()

    def get_ldap_config(self, config_id, show_password=None):
        """Get all keys and values of the specified LDAP configuration."""
        params = {"showPassword": show_password}
        return self.requester.get(config_id, params=params)

    def edit_ldap_config(self, config_id, data):
        """Update a configuration with the provided values."""
        prepared_data = {f"configData[{key}]": value for key, value in data.items()}
        return self.requester.put(config_id, data=prepared_data)

    def delete_ldap_config(self, config_id):
        """Delete a given LDAP configuration."""
        return self.requester.delete(config_id)


for ldap_key in UserLDAP.CONFIG_KEYS:
    key_name = ldap_key.replace("ldap", "")

    # create and add getter method
    getter_name = f"get_ldap_{key_name}"

    def getter_method(param):
        def getter(self, config_id):
            res = self.get_ldap_config(config_id)
            data = res.data
            return data[param]

        getter.__name__ = getter_name
        return getter

    setattr(UserLDAP, getter_name, getter_method(ldap_key))

    # create and add setter method
    setter_name = f"set_ldap_{key_name}"

    def setter_method(param):
        def setter(self, config_id, value):
            res = self.edit_ldap_config(config_id, data={param: value})
            return res

        setter.__name__ = setter_name
        return setter

    setattr(UserLDAP, setter_name, setter_method(ldap_key))

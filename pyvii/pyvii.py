# -*- coding: utf-8 -*-
from suds import client
from suds import WebFault
import utils


class Error(Exception):
    """Base class for exceptions."""

    pass


class APIError(Error):
    """Exception raised when an error is received from api."""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


class CredentialCheckFailed(Error):
    def __init__(self, header):
        self.header = header
        print("""Credential check failed.
                 url=%s,
                 Domain=%s,
                 UserId=%s,
                 UserPassword=%s,
                 OemId=%s,
                 OemPassword=%s'''))= % (self.header['url'],
                                       self.header['domain'],
                                       self.header['userid'],
                                       self.header['userpassword'],
                                       self.header['oemid'],
                                       self.header['oempassword'])
                 OemPassword=%s""" % (self.header['url'],
                                      self.header['domain'],
                                      self.header['userid'],
                                      self.header['userpassword'],
                                      self.header['oemid'],
                                      self.header['oempassword']))

    def __str__(self):
        return repr("""Credential check failed. url=%s,
                                              Domain=%s,
                                              UserId=%s,
                                              UserPassword=%s,
                                              OemId=%s,
                                              OemPassword=%s""" % (self.header['url'],
                                                                   self.header['domain'],
                                                                   self.header['userid'],
                                                                   self.header['userpassword'],
                                                                   self.header['oemid'],
                                                                   self.header['oempassword']))


class Api(object):
    """ Consumes WSDL and Authentication header.

        Keyword arguments:
        auth_header -- Dictionary containing url and credentials
    """
    def __init__(self, auth_header):
        auth_header = dict((k.lower(), v) for k, v in auth_header.items())
        try:
            self.url = auth_header.get('url', None)
            self.client = client.Client(self.url)
            self.header = self.client.factory.create('AuthHeader')
            self.header.Domain = auth_header.get('domain', None)
            self.header.UserId = auth_header.get('userid', None)
            self.header.UserPassword = auth_header.get(
                'userpassword', None)
            self.header.OemId = auth_header.get('oemid', None)
            self.header.OemPassword = auth_header.get('oempassword', None)
            self.client.set_options(soapheaders=self.header)

            # Authenticating on initialization to make sure credentials are valid.
            self.client.service.OrganizationQueryRoot()

            service = self.client.service

            self.methods = {'organization_query_by_id': service.OrganizationQueryById,
                            'organization_event_type_query_by_organizationid': service.OrganizationEventTypeQueryByOrganizationId,
                            'escalation_create': service.OrganizationEventTypeQueryByOrganizationId,
                            'escalation_create': service.OrganizationEventTypeQueryByOrganizationId,
                            'escalation_delete_by_id': service.OrganizationEventTypeQueryByOrganizationId,
                            'escalation_query_by_id': service.EscalationQueryById,
                            'escalation_query_by_name': service.EscalationQueryByName,
                            'escalation_query_by_organizationid': service.EscalationQueryByOrganizationId,
                            'escalation_query_by_organizationid_length': service.EscalationQueryByOrganizationIdLength,
                            'escalation_type_query_by_id': service.EscalationTypeQueryById,
                            'escalation_type_query_by_name': service.EscalationTypeQueryByName,
                            'escalation_type_query_by_organizationid': service.EscalationTypeQueryByOrganizationId,
                            'escalation_type_query_by_organizationid_length': service.EscalationTypeQueryByOrganizationIdLength,
                            'escalation_update': service.EscalationUpdate,
                            'import_cancel': service.ImportCancel,
                            'import_confirm': service.ImportConfirm,
                            'import_create': service.ImportCreate,
                            'import_definition_create': service.ImportDefinitionCreate,
                            'import_definition_delete_by_id': service.ImportDefinitionDeleteById,
                            'import_definition_query_by_id': service.ImportDefinitionQueryById,
                            'import_definition_query_by_organizationid': service.ImportDefinitionQueryByOrganizationId,
                            'import_definition_query_by_organizationid_length': service.ImportDefinitionQueryByOrganizationIdLength,
                            'import_exception_query_by_importid': service.ImportExceptionQueryByImportId,
                            'import_exception_query_by_importid_length': service.ImportExceptionQueryByImportIdLength,
                            'import_query_by_id': service.ImportQueryById,
                            'import_query_by_organizationid': service.ImportQueryByOrganizationId,
                            'import_query_by_organizationid_length': service.ImportQueryByOrganizationIdLength,
                            'member_create': service.MemberCreate,
                            'member_delete_by_id': service.MemberDeleteById,
                            'member_dialin_credential_create': service.MemberDialinCredentialCreate,
                            'member_dialin_credential_delete_by_memberid': service.MemberDialinCredentialDeleteByMemberId,
                            'member_dialin_credential_query_by_memberid': service.MemberDialinCredentialQueryByMemberId,
                            'member_dialin_credential_update': service.MemberDialinCredentialUpdate,
                            'member_query_by_dialinid': service.MemberQueryByDialinId,
                            'member_query_by_emailaddress': service.MemberQueryByEmailAddress,
                            'member_query_by_emailaddress_length': service.MemberQueryByEmailAddressLength,
                            'member_query_by_id': service.MemberQueryById,
                            'member_query_by_lastname': service.MemberQueryByLastName,
                            'member_query_by_lastname_length': service.MemberQueryByLastNameLength,
                            'member_query_by_organizationid': service.MemberQueryByOrganizationId,
                            'member_query_by_organizationid_length': service.MemberQueryByOrganizationIdLength,
                            'member_query_by_roleid': service.MemberQueryByRoleId,
                            'member_query_by_roleid_length': service.MemberQueryByRoleIdLength,
                            'member_query_by_sourceidentifier': service.MemberQueryBySourceIdentifier,
                            'member_query_by_useridentifier': service.MemberQueryByUserIdentifier,
                            'member_query_by_username': service.MemberQueryByUsername,
                            'member_sourceidentifier_query_by_organizationid': service.MemberSourceIdentifierQueryByOrganizationId,
                            'member_update': service.MemberUpdate,
                            'timezone_query_all': service.TimeZoneQueryAll,
                            'timezone_query_by_id': service.TimeZoneQueryById,
                            'available_contact_method_query_by_organizationid': service.AvailableContactMethodQueryByOrganizationId,
                            'billing_plan_query_by_organizationid': service.BillingPlanQueryByOrganizationId,
                            'organization_custom_field_create': service.OrganizationCustomFieldCreate,
                            'organization_custom_field_delete_by_id': service.OrganizationCustomFieldDeleteById,
                            'organization_custom_field_query_by_id': service.OrganizationCustomFieldQueryById,
                            'organization_custom_field_query_by_organizationid': service.OrganizationCustomFieldQueryByOrganizationId,
                            'organization_custom_field_query_by_organizationid_length': service.OrganizationCustomFieldQueryByOrganizationIdLength,
                            'organization_custom_field_query_by_organizationid_name': service.OrganizationCustomFieldQueryByOrganizationIdName,
                            'organization_custom_field_query_by_organizationid_name_length': service.OrganizationCustomFieldQueryByOrganizationIdNameLength,
                            'organization_custom_field_query_by_organizationid_type': service.OrganizationCustomFieldQueryByOrganizationIdType,
                            'organization_custom_field_query_by_organizationid_type_length': service.OrganizationCustomFieldQueryByOrganizationIdTypeLength,
                            'organization_custom_field_update': service.OrganizationCustomFieldUpdate,
                            'organization_event_type_query_by_id': service.OrganizationEventTypeQueryById,
                            'organization_event_type_query_by_organizationid': service.OrganizationEventTypeQueryByOrganizationId,
                            'organization_event_type_query_by_organizationid_length': service.OrganizationEventTypeQueryByOrganizationIdLength,
                            'organization_query_by_id': service.OrganizationQueryById,
                            'organization_query_children': service.OrganizationQueryChildren,
                            'organization_query_children_length': service.OrganizationQueryChildrenLength,
                            'organization_query_root': service.OrganizationQueryRoot,
                            'role_query_by_id': service.RoleQueryById,
                            'report_create': service.ReportCreate,
                            'report_delete_by_id': service.ReportDeleteById,
                            'report_query_by_id': service.ReportQueryById,
                            'report_type_query_by_id': service.ReportTypeQueryById,
                            'report_type_query_by_organizationid': service.ReportTypeQueryByOrganizationId,
                            'report_type_query_by_organizationid_length': service.ReportTypeQueryByOrganizationIdLength,
                            'scenario_activate': service.ScenarioActivate,
                            'scenario_create': service.ScenarioCreate,
                            'scenario_delete_by_id': service.ScenarioDeleteById,
                            'scenario_query_by_accesscode': service.ScenarioQueryByAccessCode,
                            'scenario_query_by_id': service.ScenarioQueryById,
                            'scenario_query_by_name': service.ScenarioQueryByName,
                            'scenario_query_by_organizationid': service.ScenarioQueryByOrganizationId,
                            'scenario_query_by_organizationid_length': service.ScenarioQueryByOrganizationIdLength,
                            'team_create': service.TeamCreate,
                            'team_delete_by_id': service.TeamDeleteById,
                            'team_entry_create': service.TeamEntryCreate,
                            'team_entry_delete_by_id': service.TeamEntryDeleteById,
                            'team_entry_member_query_by_memberid': service.TeamEntryMemberQueryByMemberId,
                            'team_entry_member_query_by_memberid_length': service.TeamEntryMemberQueryByMemberIdLength,
                            'team_entry_query_by_id': service.TeamEntryQueryById,
                            'team_entry_query_by_organizationid': service.TeamEntryQueryByOrganizationId,
                            'team_entry_query_by_organizationid_length': service.TeamEntryQueryByOrganizationIdLength,
                            'team_entry_query_by_teamid': service.TeamEntryQueryByTeamId,
                            'team_entry_query_by_teamid_length': service.TeamEntryQueryByTeamIdLength,
                            'team_entry_update': service.TeamEntryUpdate,
                            'team_member_query_by_teamid': service.TeamMemberQueryByTeamId,
                            'team_query_by_accesscode': service.TeamQueryByAccessCode,
                            'team_query_by_id': service.TeamQueryById,
                            'team_query_by_name': service.TeamQueryByName,
                            'team_query_by_organizationid': service.TeamQueryByOrganizationId,
                            'team_query_by_organizationid_length': service.TeamQueryByOrganizationIdLength,
                            'team_query_by_sourceidentifier': service.TeamQueryBySourceIdentifier,
                            'team_query_by_subteamid': service.TeamQueryBySubTeamId,
                            'team_query_by_subteamid_length': service.TeamQueryBySubTeamIdLength,
                            'team_role_create': service.TeamRoleCreate,
                            'team_role_delete_by_id': service.TeamRoleDeleteById,
                            'team_role_query_by_id': service.TeamRoleQueryById,
                            'team_role_query_by_name': service.TeamRoleQueryByName,
                            'team_role_query_by_organizationid': service.TeamRoleQueryByOrganizationId,
                            'team_role_query_by_organizationid_length': service.TeamRoleQueryByOrganizationIdLength,
                            'team_role_update': service.TeamRoleUpdate,
                            'team_update': service.TeamUpdate,
                            # TODO:0 Add Security Methods
                            'team_update': service.TeamUpdate,
                            'administrator_create': service.AdministratorCreate,
                            'administrator_delete_by_id': service.AdministratorDeleteById,
                            'administrator_query_by_default_folder_id': service.AdministratorQueryByDefaultFolderId,
                            'administrator_query_by_default_folder_id_length': service.AdministratorQueryByDefaultFolderIdLength,
                            'administrator_query_by_id': service.AdministratorQueryById,
                            'administrator_query_by_member_id': service.AdministratorQueryByMemberId,
                            'administrator_query_by_organizationid': service.AdministratorQueryByOrganizationId,
                            'administrator_query_by_organizationid_length': service.AdministratorQueryByOrganizationIdLength,
                            'administrator_update': service.AdministratorUpdate,
                            'folder_content_create': service.FolderContentCreate,
                            'folder_content_delete_by_id': service.FolderContentDeleteById,
                            'folder_content_query_by_folder_id': service.FolderContentQueryByFolderId,
                            'folder_content_query_by_folder_id_length': service.FolderContentQueryByFolderIdLength,
                            'folder_content_query_by_id': service.FolderContentQueryById,
                            'folder_create': service.FolderCreate,
                            'folder_delete_by_id': service.FolderDeleteById,
                            'folder_owner_create': service.FolderOwnerCreate,
                            'folder_owner_delete_by_id': service.FolderOwnerDeleteById,
                            'folder_owner_query_by_folder_id': service.FolderOwnerQueryByFolderId,
                            'folder_owner_query_by_folder_id_length': service.FolderOwnerQueryByFolderIdLength,
                            'folder_owner_query_by_id': service.FolderOwnerQueryById,
                            'folder_owner_query_by_member_id': service.FolderOwnerQueryByMemberId,
                            'folder_owner_query_by_member_id_length': service.FolderOwnerQueryByMemberIdLength,
                            'folder_owner_update': service.FolderOwnerUpdate,
                            'folder_query_by_id': service.FolderQueryById,
                            'folder_query_by_name': service.FolderQueryByName,
                            'folder_query_by_name_length': service.FolderQueryByNameLength,
                            'folder_query_by_organizationid': service.FolderQueryByOrganizationId,
                            'folder_query_by_organizationid_length': service.FolderQueryByOrganizationIdLength,
                            'folder_share_create': service.FolderShareCreate,
                            'folder_share_delete_by_id': service.FolderShareDeleteById,
                            'folder_share_query_by_folder_id': service.FolderShareQueryByFolderId,
                            'folder_share_query_by_folder_id_length': service.FolderShareQueryByFolderIdLength,
                            'folder_share_query_by_id': service.FolderShareQueryById,
                            'folder_share_query_by_member_id': service.FolderShareQueryByMemberId,
                            'folder_share_query_by_member_id_length': service.FolderShareQueryByMemberIdLength,
                            'folder_share_query_by_security_group_id': service.FolderShareQueryBySecurityGroupId,
                            'folder_share_query_by_security_groupid_length': service.FolderShareQueryBySecurityGroupIdLength,
                            'folder_share_update': service.FolderShareUpdate,
                            'folder_update': service.FolderUpdate,
                            'member_group_create': service.MemberGroupCreate,
                            'member_group_delete_by_id': service.MemberGroupDeleteById,
                            'member_group_entry_create': service.MemberGroupEntryCreate,
                            'member_group_entry_delete_by_id': service.MemberGroupEntryDeleteById,
                            'member_group_entry_query_by_id': service.MemberGroupEntryQueryById,
                            'member_group_entry_query_by_member_groupid': service.MemberGroupEntryQueryByMemberGroupId,
                            'member_group_entry_query_by_member_groupid_length': service.MemberGroupEntryQueryByMemberGroupIdLength,
                            'member_group_query_by_id': service.MemberGroupQueryById,
                            'member_group_query_by_name': service.MemberGroupQueryByName,
                            'member_group_query_by_name_length': service.MemberGroupQueryByNameLength,
                            'member_group_query_by_organizationid': service.MemberGroupQueryByOrganizationId,
                            'member_group_query_by_organizationid_length': service.MemberGroupQueryByOrganizationIdLength,
                            'member_group_query_by_sourceidentifier': service.MemberGroupQueryBySourceIdentifier,
                            'member_group_query_by_sourceidentifier_length': service.MemberGroupQueryBySourceIdentifierLength,
                            'member_group_update': service.MemberGroupUpdate,
                            'permission_query_by_escalation_id': service.PermissionQueryByEscalationId,
                            'permission_query_by_event_id': service.PermissionQueryByEventId,
                            'permission_query_by_member_group_id': service.PermissionQueryByMemberGroupId,
                            'permission_query_by_organization_custom_field_id': service.PermissionQueryByOrganizationCustomFieldId,
                            'permission_query_by_organization_enabled_contact_method_id': service.PermissionQueryByOrganizationEnabledContactMethodId,
                            'permission_query_by_organization_event_type_id': service.PermissionQueryByOrganizationEventTypeId,
                            'permission_query_by_report_id': service.PermissionQueryByReportId,
                            'permission_query_by_report_type_id': service.PermissionQueryByReportTypeId,
                            'permission_query_by_scenario_id': service.PermissionQueryByScenarioId,
                            'permission_query_by_scheduled_event_id': service.PermissionQueryByScheduledEventId,
                            'permission_query_by_service_recording_id': service.PermissionQueryByServiceRecordingId,
                            'permission_query_by_team_id': service.PermissionQueryByTeamId,
                            'security_group_create': service.SecurityGroupCreate,
                            'security_group_delete_by_id': service.SecurityGroupDeleteById,
                            'security_group_entry_create': service.SecurityGroupEntryCreate,
                            'security_group_entry_delete_by_id': service.SecurityGroupEntryDeleteById,
                            'security_group_entry_query_by_id': service.SecurityGroupEntryQueryById,
                            'security_group_entry_query_by_member_id': service.SecurityGroupEntryQueryByMemberId,
                            'security_group_entry_query_by_member_id_length': service.SecurityGroupEntryQueryByMemberIdLength,
                            'security_group_entry_query_by_organizationid': service.SecurityGroupEntryQueryByOrganizationId,
                            'security_group_entry_query_by_organizationid_length': service.SecurityGroupEntryQueryByOrganizationIdLength,
                            'security_group_entry_query_by_security_group_id': service.SecurityGroupEntryQueryBySecurityGroupId,
                            'security_group_entry_query_by_security_group_id_length': service.SecurityGroupEntryQueryBySecurityGroupIdLength,
                            'security_group_query_by_id': service.SecurityGroupQueryById,
                            'security_group_query_by_name': service.SecurityGroupQueryByName,
                            'security_group_query_by_name_length': service.SecurityGroupQueryByNameLength,
                            'security_group_query_by_organizationid': service.SecurityGroupQueryByOrganizationId,
                            'security_group_query_by_organizationid_length': service.SecurityGroupQueryByOrganizationIdLength,
                            'security_group_query_by_sourceidentifier': service.SecurityGroupQueryBySourceIdentifier,
                            'security_group_query_by_sourceidentifier_length': service.SecurityGroupQueryBySourceIdentifierLength,
                            'security_group_update': service.SecurityGroupUpdate
                            }

        except WebFault:
            raise CredentialCheckFailed(auth_header)

    def request(self, method, *args):
        """ Handles all requests.

            Keyword arguments:
            method -- SOAP method called
            args   -- SOAP method args
        """
        # self.method = method
        self.args = args
        try:
            return self.methods[method](*self.args)
        except WebFault as error:
            raise APIError(error)

    # ===========================================================================
    # Begin Escalation Methods
    # ===========================================================================

    def escalation_create(self,
                          escalation_list):
        """ Creates Escalation Rules.
            Keyword arguments:
            escalation_list -- list of escalation dicts
        """
        array_of_escalation = self.client.factory.create('ArrayOfEscalation')
        for escalation in escalation_list:
            escalation_object = self.client.factory.create('Escalation')
            escalation_dict = dict((k.lower(), v) for k, v in escalation.items())
            for key, val in escalation_dict.items():
                array_of_escalation_action = self.client.factory.create('ArrayOfEscalationAction')
                array_of_escalation_contact = self.client.factory.create('ArrayOfEscalationContact')
                array_of_escalation_device = self.client.factory.create('ArrayOfEscalationDevice')
                escalation_object.Name = escalation_dict.get('name', None)
                escalation_object.OrganizationId = escalation_dict.get('organizationid', None)
                escalation_object.EscalationActions = escalation_dict.get('escalationactions', None)
                escalation_actions = escalation_dict.get('escalationactions', None)

            array_of_escalation.Escalation.append(escalation_object)
        return array_of_escalation

    def escalation_delete_by_id(self,
                                escalationid_list):
        """ Deletes Escalation Rules by Id.

            Keyword arguments:
            escalationid_list -- list of escalation ids
        """
        array_of_escalationids = self.client.factory.create('ArrayOfstring')
        for escalationid in escalationid_list:
            array_of_escalationids.string.append(escalationid)

        return self.request('escalation_delete_by_id', array_of_escalationids)

    def escalation_query_by_id(self,
                               escalationid_list):
        """ Query Escalation Rules by Id.

            Keyword arguments:
            escalationid_list -- list of escalation ids
        """
        array_of_escalationids = self.client.factory.create('ArrayOfstring')
        for escalationid in escalationid_list:
            array_of_escalationids.string.append(escalationid)

        return self.request('escalation_query_by_id', array_of_escalationids)

    def escalation_query_by_name(self,
                                 escalation_name_list):
        """ Query Escalation Rules by Name.

            Keyword arguments:
            escalation_name_list -- list of escalation names
        """
        array_of_escalation_names = self.client.factory.create('ArrayOfstring')
        for escalation_name in escalation_name_list:
            array_of_escalation_names.string.append(escalation_name)

        return self.request('escalation_query_by_name', array_of_escalation_names)

    def escalation_query_by_organizationid(self,
                                           orgid_list,
                                           index=0,
                                           length=300):
        """ Returns Escalation Rules by Organization Id

            Keyword arguments:
            orgid_list -- list of org ids
            index      -- starting index
            length     -- number of orgs to return

        """
        array_of_orgids = self.client.factory.create('ArrayOfstring')
        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('escalation_query_by_organizationid',
                            array_of_orgids,
                            index,
                            length)

    def escalation_query_by_organizationid_length(self,
                                                  orgid_list):
        """ Returns Length of  Escalation Rules

            Keyword arguments:
            orgid_list -- list of org ids
        """
        array_of_orgids = self.client.factory.create('ArrayOfstring')
        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('escalation_query_by_organizationid_length', array_of_orgids)

    def escalation_type_query_by_id(self,
                                    escalation_type_id_list):
        """ Query Escalation Rules by Id.

            Keyword arguments:
            escalationid_list -- list of escalation ids
        """

        array_of_escalation_type_ids = self.client.factory.create('ArrayOfstring')
        for escalation_type_id in escalation_type_id_list:
            array_of_escalation_type_ids.string.append(escalation_type_id)

        return self.request('escalation_type_query_by_id', array_of_escalation_type_ids)

    def escalation_type_query_by_name(self,
                                      escalation_type_name_list):
        """ Query Escalation Rules by Name.

            Keyword arguments:
            escalation_type_name_list -- list of escalation names
        """
        array_of_escalation_type_names = self.client.factory.create('ArrayOfstring')
        for escalation_type_name in escalation_type_name_list:
            array_of_escalation_type_names.string.append(escalation_type_name)

        return self.request('escalation_type_query_by_name', array_of_escalation_type_names)

    def escalation_type_query_by_organizationid(self,
                                                orgid_list,
                                                index=0,
                                                length=300):
        """ Returns Escalation Types by Organization Id

            Keyword arguments:
            orgid_list -- list of org ids
            index      -- starting index
            length     -- number of orgs to return
        """
        array_of_orgids = self.client.factory.create('ArrayOfstring')
        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('escalation_type_query_by_organizationid',
                            array_of_orgids,
                            index,
                            length)

    def escalation_type_query_by_organizationid_length(self,
                                                       orgid_list):
        """ Returns Length of Escalation Types

            Keyword arguments:
            orgid_list -- list of org ids
        """
        array_of_orgids = self.client.factory.create('ArrayOfstring')
        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('escalation_type_query_by_organizationid_length', array_of_orgids)

    def escalation_update(self):
        pass

    # ===========================================================================
    # End Escalation Methods
    # ===========================================================================

    # ===========================================================================
    # Begin Import Methods
    # ===========================================================================

    def import_cancel(self,
                      importid_list):
        """ Cancels Import by Import Id.

            Keyword arguments:
            importid_list -- list of import ids
        """
        array_of_importids = self.client.factory.create('ArrayOfstring')
        for importid in importid_list:
            array_of_importids.string.append(importid)

        return self.request('import_cancel', array_of_importids)

    def import_confirm(self,
                       importid_list):
        """ Confirms Import by Import Id.

            Keyword arguments:
            importid_list -- list of import ids
        """
        array_of_importids = self.client.factory.create('ArrayOfstring')
        for importid in importid_list:
            array_of_importids.string.append(importid)

        return self.request('import_confirm', array_of_importids)

    def import_create(self):
        pass

    def import_definition_create(self):
        pass

    def import_definition_delete_by_id(self, importdefid_list):
        """ Deletes Import Definition by Import Id.

            Keyword arguments:
            importdefid_list -- list of import definition ids
        """
        array_of_importdefids = self.client.factory.create('ArrayOfstring')
        for importdefid in importdefid_list:
            array_of_importdefids.string.append(importdefid)

        return self.request('import_definition_delete_by_id', array_of_importdefids)

    def import_definition_query_by_id(self, importdefid_list):
        """ Query Import Definition by Id.

            Keyword arguments:
            importdefid_list -- list of import definition ids
        """
        array_of_importdefids = self.client.factory.create('ArrayOfstring')
        for importdefid in importdefid_list:
            array_of_importdefids.string.append(importdefid)

        return self.request('import_definition_query_by_id', array_of_importdefids)

    def import_definition_query_by_organizationid(self, orgid_list, index=0, length=300):
        """ Import Definition Query by Organization Id

            Keyword arguments:
            orgid_list -- list of org ids
            index      -- starting index
            length     -- number of orgs to return
        """
        array_of_orgids = self.client.factory.create('ArrayOfstring')
        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('import_definition_query_by_organizationid',
                            array_of_orgids,
                            index,
                            length)

    def import_definition_query_by_organizationid_length(self, orgid_list):
        """ Returnes Length Of Import Definition Query by Organization Id

            Keyword arguments:
            orgid_list -- list of org ids
        """
        array_of_orgids = self.client.factory.create('ArrayOfstring')
        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('import_definition_query_by_organizationid_length',
                            array_of_orgids)

    def import_exception_query_by_importid(self, importid_list, index=0, length=300):
        """ Import Exception Query by Import Id

            Keyword arguments:
            importid_list -- list of import ids
            index         -- starting index
            length        -- number of import exceptions to return
        """
        array_of_importids = self.client.factory.create('ArrayOfstring')
        for importid in importid_list:
            array_of_importids.string.append(importid)

        return self.request('import_definition_query_by_organizationid',
                            array_of_importids,
                            index,
                            length)

    def import_exception_query_by_importid_length(self, importid_list):
        """ Returns Length Of Import Exception Query by Import Id

            Keyword arguments:
            importid_list -- list of import ids
        """
        array_of_importids = self.client.factory.create('ArrayOfstring')
        for importid in importid_list:
            array_of_importids.string.append(importid)

        return self.request('import_exception_query_by_importid_length',
                            array_of_importids)

    def import_query_by_id(self, orgid_list, include_files=False):
        """ Import Query by Id

            Keyword arguments:
            orgid_list    -- list of org ids
            index         -- starting index
            length        -- number of imports to return
        """
        array_of_orgids = self.client.factory.create('ArrayOfstring')
        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('import_query_by_id',
                            array_of_orgids,
                            include_files)

    def import_query_by_organizationid(self, orgid_list, include_files=False, index=0, length=300):
        """ Import Query by Organization Id

            Keyword arguments:
            orgid_list    -- list of org ids
            index         -- starting index
            length        -- number of imports to return
        """
        array_of_orgids = self.client.factory.create('ArrayOfstring')
        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('import_query_by_organizationid',
                            array_of_orgids,
                            include_files,
                            index,
                            length)

    def import_query_by_organizationid_length(self, orgid_list):
        """ Returns Length Of Import Query by Organization Id

            Keyword arguments:
            orgid_list    -- list of org ids
        """
        array_of_orgids = self.client.factory.create('ArrayOfstring')
        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('import_query_by_organizationid_length',
                            array_of_orgids)

    # ===========================================================================
    # End Import Methods
    # ===========================================================================

    # ===========================================================================
    # Begin Member Methods
    # ===========================================================================

    def member_create(self, member_list):
        """ Creates Members.

            Keyword arguments:
            member_list -- list of members
        """
        members = self.client.factory.create('ArrayOfMember')
        for member in member_list:
            member_object = self.client.factory.create('Member')
            contact_methods = self.client.factory.create('ArrayOfContactMethod')
            custom_fields = self.client.factory.create('ArrayOfMemberCustomField')
            member_dict = utils.lower_keys(member)
            member_object.Username = member_dict.get('username', None)
            member_object.Password = member_dict.get('password', None)
            member_object.Prefix = member_dict.get('prefix', None)
            member_object.FirstName = member_dict.get('firstname', None)
            member_object.MiddleName = member_dict.get('middlename', None)
            member_object.LastName = member_dict.get('lastname', None)
            member_object.Company = member_dict.get('company', None)
            member_object.Title = member_dict.get('title', None)
            member_object.Source = member_dict.get('source', None)
            member_object.SourceIdentifier = member_dict.get(
                'sourceidentifier', None)
            member_object.TimeZoneId = member_dict.get('timezoneid', None)
            member_object.RoleId = member_dict.get('roleid', None)
            member_object.OrganizationId = member_dict.get(
                'organizationid', None)
            member_object.AccountEnabled = member_dict.get(
                'accountenabled', None)
            member_object.Subscription = member_dict.get(
                'subscription', None)
            for contact_method_email in utils.find_key('contactmethodemail', member_dict):
                contact_method_object = self.client.factory.create('ContactMethod')
                contact_method_email_object = self.client.factory.create('ContactMethodEmail')
                contact_method_email_object._Label = contact_method_email.get('label', None)
                contact_method_email_object.Qualifier = contact_method_email.get('qualifier', None)
                contact_method_email_object.Ordinal = contact_method_email.get('ordinal', None)
                contact_method_email_object.EmailAddress = contact_method_email.get('emailaddress', None)
                contact_methods.ContactMethod.append(contact_method_object)
                contact_method_object.ContactMethodEmail = contact_method_email_object

            for contact_method_fax in utils.find_key('contactmethodfax', member_dict):
                contact_method_object = self.client.factory.create('ContactMethod')
                contact_method_fax_object = self.client.factory.create('ContactMethodFax')
                contact_method_fax_object._Label = contact_method_fax.get('label', None)
                contact_method_fax_object.Qualifier = contact_method_fax.get('qualifier', None)
                contact_method_fax_object.Ordinal = contact_method_fax.get('ordinal', None)
                contact_method_fax_object.PhoneNum = contact_method_fax.get('phonenum', None)
                contact_method_object.ContactMethodFax = contact_method_fax_object
                contact_methods.ContactMethod.append(contact_method_object)

            for contact_method_pager in utils.find_key('contactmethodpager', member_dict):
                contact_method_object = self.client.factory.create('ContactMethod')
                contact_method_pager_object = self.client.factory.create('ContactMethodPager')
                contact_method_pager_object._Label = contact_method_pager.get('label', None)
                contact_method_pager_object.Qualifier = contact_method_pager.get('qualifier', None)
                contact_method_pager_object.Ordinal = contact_method_pager.get('ordinal', None)
                contact_method_pager_object.PhoneNum = contact_method_pager.get('pagernum', None)
                contact_method_pager_object.PagerAccessCode = contact_method_pager.get('pageraccesscode', None)
                contact_method_object.ContactMethodPager = contact_method_pager_object
                contact_methods.ContactMethod.append(contact_method_object)

            for contact_method_phone in utils.find_key('contactmethodphone', member_dict):
                contact_method_object = self.client.factory.create('ContactMethod')
                contact_method_phone_object = self.client.factory.create('ContactMethodPhone')
                contact_method_phone_object._Label = contact_method_phone.get('label', None)
                contact_method_phone_object.Qualifier = contact_method_phone.get('qualifier', None)
                contact_method_phone_object.Ordinal = contact_method_phone.get('ordinal', None)
                contact_method_phone_object.PhoneNum = contact_method_phone.get('phonenum', None)
                contact_method_object.ContactMethodPhone = contact_method_phone_object
                contact_methods.ContactMethod.append(contact_method_object)

            for contact_method_sms in utils.find_key('contactmethodsms', member_dict):
                contact_method_object = self.client.factory.create('ContactMethod')
                contact_method_sms_object = self.client.factory.create('ContactMethodSMS')
                contact_method_sms_object._Label = contact_method_sms.get('label', None)
                contact_method_sms_object.Qualifier = contact_method_sms.get('qualifier', None)
                contact_method_sms_object.Ordinal = contact_method_sms.get('ordinal', None)
                contact_method_sms_object.PhoneNum = contact_method_sms.get('phonenum', None)
                contact_method_object.ContactMethodSMS = contact_method_sms_object
                contact_methods.ContactMethod.append(contact_method_object)

            for custom_field in utils.find_key('membercustomfield', member_dict):
                custom_field_object = self.client.factory.create('MemberCustomField')
                custom_field_object.Value = custom_field.get('value', None)
                custom_field_object.OrganizationCustomFieldId = custom_field.get('organizationcustomfieldid')
                custom_fields.MemberCustomField.append(custom_field_object)

            member_object.ContactMethods = contact_methods
            member_object.MemberCustomFields = custom_fields
            members.Member.append(member_object)

        return self.request('member_create', members)

    def member_delete_by_id(self, memberid_list):
        """ Deletes Member By Id

            Keyword arguments:
            memberid_list -- list of member ids
        """
        array_of_memberids = self.client.factory.create('ArrayOfstring')
        for memberid in memberid_list:
            array_of_memberids.string.append(memberid)

        return self.request('member_delete_by_id',
                            array_of_memberids)

    def member_dialin_credential_create(self, member_dialin_list):
        """ Creates Member Dialin Credentials

            Keyword arguments:
            member_dialin_list -- list of member dialin credentials
        """
        array_of_member_dialins = self.client.factory.create('ArrayOfMemberDialinCredential')

        for member_dialin in member_dialin_list:
            member_dialin_object = self.client.factory.create('MemberDialinCredential')
            member_dialin_dict = utils.lower_keys(member_dialin)
            member_dialin_object.DialinId = member_dialin_dict.get('dialinid', None)
            member_dialin_object.DialinPin = member_dialin_dict.get('dialinpin', None)
            member_dialin_object.MemberId = member_dialin_dict.get('memberid', None)
            array_of_member_dialins.MemberDialinCredential.append(member_dialin_object)

        return self.request('member_dialin_credential_create',
                            array_of_member_dialins)

    def member_dialin_credential_delete_by_memberid(self, memberid_list):
        """ Deletes Member Dialin Credentials By MemberId

            Keyword arguments:
            member_dialin_list -- list of member dialin credentials
        """
        array_of_memberids = self.client.factory.create('ArrayOfstring')
        for memberid in memberid_list:
            array_of_memberids.string.append(memberid)

        return self.request('member_dialin_credential_delete_by_memberid',
                            array_of_memberids)

    def member_dialin_credential_query_by_memberid(self, memberid_list):
        """  Member Dialin Credentials Query By MemberId

            Keyword arguments:
            memberid_list -- list of member ids
        """
        array_of_memberids = self.client.factory.create('ArrayOfstring')
        for memberid in memberid_list:
            array_of_memberids.string.append(memberid)

        return self.request('member_dialin_credential_query_by_memberid',
                            array_of_memberids)

    def member_dialin_credential_update(self, member_dialin_list):
        """ Updates Member Dialin Credentials

            Keyword arguments:
            member_dialin_list -- list of member dialin credentials
        """
        array_of_member_dialins = self.client.factory.create('ArrayOfMemberDialinCredential')

        for member_dialin in member_dialin_list:
            member_dialin_object = self.client.factory.create('MemberDialinCredential')
            member_dialin_dict = utils.lower_keys(member_dialin)
            member_dialin_object.DialinId = member_dialin_dict.get('dialinid', None)
            member_dialin_object.DialinPin = member_dialin_dict.get('dialinpin', None)
            member_dialin_object.MemberId = member_dialin_dict.get('memberid', None)
            array_of_member_dialins.MemberDialinCredential.append(member_dialin_object)

        return self.request('member_dialin_credential_update',
                            array_of_member_dialins)

    def member_query_by_dialinid(self, dialinid_list):
        """  Member Query By DialinId

            Keyword arguments:
            dialinid_list -- list of dialin ids
        """
        array_of_dialinids = self.client.factory.create('ArrayOfstring')
        for dialinid in dialinid_list:
            array_of_dialinids.string.append(dialinid)

        return self.request('member_query_by_dialinid',
                            array_of_dialinids)

    def member_query_by_emailaddress(self, orgid_list, email_list, index=0, length=300):
        """  Member Query By Email Address

            Keyword arguments:
            orgid_list -- list of org ids
            email_list -- list email addresses
            index      -- starting index
            length     -- number of members to return
        """
        array_of_orgids = self.client.factory.create('ArrayOfstring')
        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        array_of_emails = self.client.factory.create('ArrayOfstring')
        for email in email_list:
            array_of_emails.string.append(email)

        return self.request('member_query_by_emailaddress',
                            array_of_orgids,
                            array_of_emails,
                            index,
                            length)

    def member_query_by_emailaddress_length(self, orgid_list, email_list):
        """ Returns Length of Member Query By Email Address

            Keyword arguments:
            orgid_list -- list of org ids
            email_list -- list email addresses
        """
        array_of_orgids = self.client.factory.create('ArrayOfstring')
        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        array_of_emails = self.client.factory.create('ArrayOfstring')
        for email in email_list:
            array_of_emails.string.append(email)

        return self.request('member_query_by_emailaddress_length',
                            array_of_orgids,
                            array_of_emails)

    def member_query_by_id(self, memberid_list):
        """  Member Query By Id

            Keyword arguments:
            memberid_list -- list of member ids
        """
        array_of_memberids = self.client.factory.create('ArrayOfstring')
        for memberid in memberid_list:
            array_of_memberids.string.append(memberid)

        return self.request('member_query_by_id',
                            array_of_memberids)

    def member_query_by_lastname(self, orgid_list, lastname_list, index=0, length=300):
        """  Member Query By LastName

            Keyword arguments:
            orgid_list -- list of org ids
            lastname_list -- list of lastnames
            index      -- starting index
            length     -- number of members to return
        """
        array_of_orgids = self.client.factory.create('ArrayOfstring')
        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        array_of_lastnames = self.client.factory.create('ArrayOfstring')
        for lastname in lastname_list:
            array_of_lastnames.string.append(lastname)

        return self.request('member_query_by_lastname',
                            array_of_orgids,
                            array_of_lastnames,
                            index,
                            length)

    def member_query_by_lastname_length(self, orgid_list, lastname_list):
        """  Returns Length Of Member Query By LastName

            Keyword arguments:
            orgid_list -- list of org ids
            lastname_list -- list of lastnames
        """
        array_of_orgids = self.client.factory.create('ArrayOfstring')
        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        array_of_lastnames = self.client.factory.create('ArrayOfstring')
        for lastname in lastname_list:
            array_of_lastnames.string.append(lastname)

        return self.request('member_query_by_lastname_length',
                            array_of_orgids,
                            array_of_lastnames)

    def member_query_by_organizationid(self, orgid_list, index=0, length=300):
        """ Returns Members by Organization Id

            Keyword arguments:
            orgid_list -- list of org ids
            index      -- starting index
            length     -- number of orgs to return

        """
        array_of_orgids = self.client.factory.create('ArrayOfstring')
        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('member_query_by_organizationid',
                            array_of_orgids,
                            index,
                            length)

    def member_query_by_organizationid_length(self, orgid_list):
        """ Returns Length of Members by Organization Id

            Keyword arguments:
            orgid_list -- list of org ids
        """
        array_of_orgids = self.client.factory.create('ArrayOfstring')
        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('member_query_by_organizationid_length',
                            array_of_orgids)

    def member_query_by_roleid(self, orgid_list, roleid, index=0, length=300):
        """ Returns Members by Role Id

            Keyword arguments:
            orgid_list -- list of org ids
            roleid     -- role id
            index      -- starting index
            length     -- number of orgs to return

        """
        array_of_orgids = self.client.factory.create('ArrayOfstring')
        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('member_query_by_roleid',
                            array_of_orgids,
                            roleid,
                            index,
                            length)

    def member_query_by_roleid_length(self, orgid_list, roleid):
        """ Returns Length of Members by Role Id

            Keyword arguments:
            orgid_list -- list of org ids
            roleid     -- role id
        """
        array_of_orgids = self.client.factory.create('ArrayOfstring')
        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('member_query_by_roleid_length',
                            array_of_orgids,
                            roleid)

    def member_query_by_sourceidentifier(self, sourceid_list):
        """ Returns Members by Source Identifier

            Keyword arguments:
            sourceid_list -- list of source ids
        """
        array_of_sourceids = self.client.factory.create('ArrayOfstring')
        for sourceid in sourceid_list:
            array_of_sourceids.string.append(sourceid)

        return self.request('member_query_by_sourceidentifier',
                            array_of_sourceids)

    def member_query_by_useridentifier(self, userid_list):
        """ Returns Members by User Identifier

            Keyword arguments:
            userid_list -- list of user ids
        """
        array_of_userids = self.client.factory.create('ArrayOfstring')
        for userid in userid_list:
            array_of_userids.string.append(userid)

        return self.request('member_query_by_useridentifier',
                            array_of_userids)

    def member_query_by_username(self, member_username_list):
        """  Member Query By Username

            Keyword arguments:
            member_username_list -- list of member ids
        """
        array_of_member_usernames = self.client.factory.create('ArrayOfstring')
        for username in member_username_list:
            array_of_member_usernames.string.append(username)

        return self.request('member_query_by_username',
                            array_of_member_usernames)

    def member_sourceidentifier_query_by_organizationid(self, orgid_list, index=0, length=300):
        """ Returns Member Source Identifiers By Organization Id

            Keyword arguments:
            orgid_list -- list of org ids
            index      -- starting index
            length     -- number of orgs to return

        """
        array_of_orgids = self.client.factory.create('ArrayOfstring')
        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('member_sourceidentifier_query_by_organizationid',
                            array_of_orgids,
                            index,
                            length)

    def member_update(self, member_list, sync=False):
        """ Updates Members.

            Keyword arguments:
            member_list -- list of members
            sync        -- boolean (true/false)
        """
        members = self.client.factory.create('ArrayOfMember')
        for member in member_list:
            member_object = self.client.factory.create('Member')
            contact_methods = self.client.factory.create('ArrayOfContactMethod')
            custom_fields = self.client.factory.create('ArrayOfMemberCustomField')
            member_dict = utils.lower_keys(member)
            member_object.MemberId = member_dict.get('memberid', None)
            member_object.Username = member_dict.get('username', None)
            member_object.Password = member_dict.get('password', None)
            member_object.Prefix = member_dict.get('prefix', None)
            member_object.FirstName = member_dict.get('firstname', None)
            member_object.MiddleName = member_dict.get('middlename', None)
            member_object.LastName = member_dict.get('lastname', None)
            member_object.Company = member_dict.get('company', None)
            member_object.Title = member_dict.get('title', None)
            member_object.Source = member_dict.get('source', None)
            member_object.SourceIdentifier = member_dict.get(
                'sourceidentifier', None)
            member_object.TimeZoneId = member_dict.get('timezoneid', None)
            member_object.RoleId = member_dict.get('roleid', None)
            member_object.OrganizationId = member_dict.get(
                'organizationid', None)
            member_object.AccountEnabled = member_dict.get(
                'accountenabled', None)
            member_object.Subscription = member_dict.get(
                'subscription', None)
            for contact_method_email in utils.find_key('contactmethodemail', member_dict):
                contact_method_object = self.client.factory.create('ContactMethod')
                contact_method_email_object = self.client.factory.create('ContactMethodEmail')
                contact_method_email_object._Label = contact_method_email.get('label', None)
                contact_method_email_object.Qualifier = contact_method_email.get('qualifier', None)
                contact_method_email_object.Ordinal = contact_method_email.get('ordinal', None)
                contact_method_email_object.EmailAddress = contact_method_email.get('emailaddress', None)
                contact_methods.ContactMethod.append(contact_method_object)
                contact_method_object.ContactMethodEmail = contact_method_email_object

            for contact_method_fax in utils.find_key('contactmethodfax', member_dict):
                contact_method_object = self.client.factory.create('ContactMethod')
                contact_method_fax_object = self.client.factory.create('ContactMethodFax')
                contact_method_fax_object._Label = contact_method_fax.get('label', None)
                contact_method_fax_object.Qualifier = contact_method_fax.get('qualifier', None)
                contact_method_fax_object.Ordinal = contact_method_fax.get('ordinal', None)
                contact_method_fax_object.PhoneNum = contact_method_fax.get('phonenum', None)
                contact_method_object.ContactMethodFax = contact_method_fax_object
                contact_methods.ContactMethod.append(contact_method_object)

            for contact_method_pager in utils.find_key('contactmethodpager', member_dict):
                contact_method_object = self.client.factory.create('ContactMethod')
                contact_method_pager_object = self.client.factory.create('ContactMethodPager')
                contact_method_pager_object._Label = contact_method_pager.get('label', None)
                contact_method_pager_object.Qualifier = contact_method_pager.get('qualifier', None)
                contact_method_pager_object.Ordinal = contact_method_pager.get('ordinal', None)
                contact_method_pager_object.PhoneNum = contact_method_pager.get('pagernum', None)
                contact_method_pager_object.PagerAccessCode = contact_method_pager.get('pageraccesscode', None)
                contact_method_object.ContactMethodPager = contact_method_pager_object
                contact_methods.ContactMethod.append(contact_method_object)

            for contact_method_phone in utils.find_key('contactmethodphone', member_dict):
                contact_method_object = self.client.factory.create('ContactMethod')
                contact_method_phone_object = self.client.factory.create('ContactMethodPhone')
                contact_method_phone_object._Label = contact_method_phone.get('label', None)
                contact_method_phone_object.Qualifier = contact_method_phone.get('qualifier', None)
                contact_method_phone_object.Ordinal = contact_method_phone.get('ordinal', None)
                contact_method_phone_object.PhoneNum = contact_method_phone.get('phonenum', None)
                contact_method_object.ContactMethodPhone = contact_method_phone_object
                contact_methods.ContactMethod.append(contact_method_object)

            for contact_method_sms in utils.find_key('contactmethodsms', member_dict):
                contact_method_object = self.client.factory.create('ContactMethod')
                contact_method_sms_object = self.client.factory.create('ContactMethodSMS')
                contact_method_sms_object._Label = contact_method_sms.get('label', None)
                contact_method_sms_object.Qualifier = contact_method_sms.get('qualifier', None)
                contact_method_sms_object.Ordinal = contact_method_sms.get('ordinal', None)
                contact_method_sms_object.PhoneNum = contact_method_sms.get('phonenum', None)
                contact_method_object.ContactMethodSMS = contact_method_sms_object
                contact_methods.ContactMethod.append(contact_method_object)

            for custom_field in utils.find_key('membercustomfield', member_dict):
                custom_field_object = self.client.factory.create('MemberCustomField')
                custom_field_object.Value = custom_field.get('value', None)
                custom_field_object.OrganizationCustomFieldId = custom_field.get('organizationcustomfieldid')
                custom_fields.MemberCustomField.append(custom_field_object)

            member_object.ContactMethods = contact_methods
            member_object.MemberCustomFields = custom_fields
            members.Member.append(member_object)

        return self.request('member_update', members, sync)

    def timezone_query_all(self):
        """ Returns All Timezones
        """
        return self.request('timezone_query_all')

    def timezone_query_by_id(self, timezoneid_list):
        """  Timezone Query By Id

            Keyword arguments:
            timezoneid_list -- list of timezone ids
        """
        array_of_timezoneids = self.client.factory.create('ArrayOfstring')
        for timezoneid in timezoneid_list:
            array_of_timezoneids.string.append(timezoneid)

        return self.request('timezone_query_by_id',
                            array_of_timezoneids)

    # ===========================================================================
    # End Member Methods
    # ===========================================================================

    # ===========================================================================
    # Begin Organization Methods
    # ===========================================================================

    def available_contact_method_query_by_organizationid(self,
                                                         orgid_string):
        """ Returns Organization Contact Methods.

            Keyword arguments:
            orgid_string -- org id string

        """
        return self.request('available_contact_method_query_by_organizationid', orgid_string)

    def billing_plan_query_by_organizationid(self,
                                             orgid_string):
        """ Returns the Billing Plans available in the organization.

            Keyword arguments:
            orgid_string -- org id string
        """
        return self.request('billing_plan_query_by_organizationid', orgid_string)

    def organization_custom_field_create(self, org_customfield_list):
        """ Creates Organization Custom Field

            Keyword arguments:
            org_customfield_list -- list of org custom fields
        """
        array_of_org_customfields = self.client.factory.create('ArrayOfOrganizationCustomField')

        for org_custom_field in org_customfield_list:
            org_custom_field_object = self.client.factory.create('OrganizationCustomField')
            org_custom_field_dict = utils.lower_keys(org_custom_field)
            org_custom_field_object.Name = org_custom_field_dict.get('name', None)
            org_custom_field_object.SourceIdentifier = org_custom_field_dict.get('sourceidentifier', None)
            org_custom_field_object.Type = org_custom_field_dict.get('type', None)
            org_custom_field_object.AdminAccess = org_custom_field_dict.get('adminaccess', None)
            org_custom_field_object.UserAccess = org_custom_field_dict.get('useraccess', None)
            org_custom_field_object.Searchable = org_custom_field_dict.get('searchable', None)
            org_custom_field_object.SecurityEnabled = org_custom_field_dict.get('securityenabled', None)
            org_custom_field_object.OrganizationId = org_custom_field_dict.get('organizationid', None)
            array_of_org_customfields.OrganizationCustomField.append(org_custom_field_object)

        return self.request('organization_custom_field_create',
                            array_of_org_customfields)

    def organization_custom_field_delete_by_id(self, org_customfield_list):
        """ Deletes Custom Field By Id

            Keyword arguments:
            org_customfield_list -- list of org custom field ids
        """
        array_of_customfieldids = self.client.factory.create('ArrayOfstring')
        for org_customfieldid in org_customfield_list:
            array_of_customfieldids.string.append(org_customfieldid)

        return self.request('organization_custom_field_delete_by_id', array_of_customfieldids)

    def organization_custom_field_query_by_id(self, org_customfield_list):
        """ Query Organization Custom Field By Id

            Keyword arguments:
            org_customfield_list -- list of org custom field ids
        """
        array_of_customfieldids = self.client.factory.create('ArrayOfstring')
        for org_customfieldid in org_customfield_list:
            array_of_customfieldids.string.append(org_customfieldid)

        return self.request('organization_custom_field_query_by_id', array_of_customfieldids)

    def organization_custom_field_query_by_organizationid(self,
                                                          orgid_list,
                                                          index=0,
                                                          length=300):
        """ Returns Custom Fields

            Keyword arguments:
            orgid_list -- list of org ids
            index      -- starting index
            length     -- number of orgs to return

        """
        array_of_orgids = self.client.factory.create('ArrayOfstring')
        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('organization_custom_field_query_by_organizationid',
                            array_of_orgids,
                            index,
                            length)

    def organization_custom_field_query_by_organizationid_length(self,
                                                                 orgid_list):
        """ Returns Length of Custom Fields

            Keyword arguments:
            orgid_list -- list of org ids
        """
        array_of_orgids = self.client.factory.create('ArrayOfstring')
        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('organization_custom_field_query_by_organizationid_length', array_of_orgids)

    def organization_custom_field_query_by_organizationid_name(self,
                                                               orgid_list,
                                                               name,
                                                               index=0,
                                                               length=300):
        """ Returns Organization Custom Fields by Name

            Keyword arguments:
            orgid_list -- list of org ids
            name       -- custom field name
            index      -- starting index
            length     -- number of orgs to return
        """
        array_of_orgids = self.client.factory.create('ArrayOfstring')

        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('organization_custom_field_query_by_organizationid_name',
                            array_of_orgids,
                            name,
                            index,
                            length)

    def organization_custom_field_query_by_organizationid_name_length(self,
                                                                      orgid_list,
                                                                      custom_field_name):
        """ Returns Length of Custom Fields by Org Id and Custom Field Name

            Keyword arguments:
            orgid_list -- list of org ids
        """
        array_of_orgids = self.client.factory.create('ArrayOfstring')
        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('organization_custom_field_query_by_organizationid_name_length',
                            array_of_orgids,
                            custom_field_name)

    def organization_custom_field_query_by_organizationid_type(self,
                                                               orgid_list,
                                                               custom_field_type,
                                                               index=0,
                                                               length=300):
        """ Returns Custom Fields by Org Id and Custom Field Type

            Keyword arguments:
            orgid_list        -- list of org ids
            custom_field_type -- custom field type
            index             -- starting index
            length            -- number of custom fields to return
        """
        array_of_orgids = self.client.factory.create('ArrayOfstring')
        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('organization_custom_field_query_by_organizationid_type',
                            array_of_orgids,
                            custom_field_type,
                            index,
                            length)

    def organization_custom_field_query_by_organizationid_type_length(self,
                                                                      orgid_list,
                                                                      custom_field_type):
        """ Returns Length of Custom Fields by Org Id and Custom Field Type

            Keyword arguments:
            orgid_list        -- list of org ids
            custom_field_type -- custom field type
        """
        array_of_orgids = self.client.factory.create('ArrayOfstring')
        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('organization_custom_field_query_by_organizationid_type_length',
                            array_of_orgids,
                            custom_field_type)

    def organization_custom_field_update(self, org_customfield_list, sync):
        """ Updates Organization Custom Field

            Keyword arguments:
            org_customfield_list -- list of org custom fields
            sync        -- boolean (true/false)
        """
        array_of_org_customfields = self.client.factory.create('ArrayOfOrganizationCustomField')

        for org_custom_field in org_customfield_list:
            org_custom_field_object = self.client.factory.create('OrganizationCustomField')
            org_custom_field_dict = utils.lower_keys(org_custom_field)
            org_custom_field_object.OrganizationCustomFieldId = org_custom_field_dict.get('organizationcustomfieldid', None)
            org_custom_field_object.Name = org_custom_field_dict.get('name', None)
            org_custom_field_object.SourceIdentifier = org_custom_field_dict.get('sourceidentifier', None)
            org_custom_field_object.Type = org_custom_field_dict.get('type', None)
            org_custom_field_object.AdminAccess = org_custom_field_dict.get('adminaccess', None)
            org_custom_field_object.UserAccess = org_custom_field_dict.get('useraccess', None)
            org_custom_field_object.Searchable = org_custom_field_dict.get('searchable', None)
            org_custom_field_object.SecurityEnabled = org_custom_field_dict.get('securityenabled', None)
            org_custom_field_object.OrganizationId = org_custom_field_dict.get('organizationid', None)
            array_of_org_customfields.OrganizationCustomField.append(org_custom_field_object)

        return self.request('organization_custom_field_update',
                            array_of_org_customfields,
                            sync)

    def organization_event_type_query_by_id(self,
                                            eventid_list):

        """ Returns Organization Event Type by Id

            Keyword arguments:
            eventid_list -- list of event ids
        """
        array_of_eventids = self.client.factory.create('ArrayOfstring')

        for eventid in eventid_list:
            array_of_eventids.string.append(eventid)

        return self.request('organization_event_type_query_by_id',
                            array_of_eventids)

    def organization_event_type_query_by_organizationid(self,
                                                        orgid_list,
                                                        index=0,
                                                        length=300):
        """ Returns Organization Event Types by Org Id

            Keyword arguments:
            orgid_list -- list of org ids
            index      -- starting index
            length     -- number of orgs to return
        """
        array_of_orgids = self.client.factory.create('ArrayOfstring')

        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('organization_event_type_query_by_organizationid',
                            array_of_orgids,
                            index,
                            length)

    def organization_event_type_query_by_organizationid_length(self,
                                                               orgid_list):
        """ Returns Length of Organization Event Types

            Keyword arguments:
            orgid_list -- list of org ids
        """
        array_of_orgids = self.client.factory.create('ArrayOfstring')

        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('organization_event_type_query_by_organizationid_length',
                            array_of_orgids)

    def organization_query_by_id(self,
                                 orgid_list):
        """ Returns Organization

            Keyword arguments:
            orgid_list -- list of org ids
        """
        array_of_orgids = self.client.factory.create('ArrayOfstring')

        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('organization_query_by_id',
                            array_of_orgids)

    def organization_query_children(self,
                                    orgid_string,
                                    index=0,
                                    length=300):
        """ Returns Organization Sub-Orgs

            Keyword arguments:
            orgid_list -- list of org ids
            index      -- starting index
            length     -- number of orgs to return
        """
        return self.request('organization_query_children',
                            orgid_string,
                            index,
                            length)

    def organization_query_children_length(self,
                                           orgid_string):

        """ Returns Length of Organization Sub-Orgs

            Keyword arguments:
            orgid_list -- list of org ids
        """
        return self.request('organization_query_children_length',
                            orgid_string)

    def organization_query_root(self):
        """Returns OrganizationId, Events and Roles."""

        return self.request('organization_query_root')

    def role_query_by_id(self,
                         roleid_list):
        """ Returns Organization Role by RoleId

            Keyword arguments:
            roleid_list -- list of role idsx
        """
        array_of_roleids = self.client.factory.create('ArrayOfstring')

        for roleid in roleid_list:
            array_of_roleids.string.append(roleid)

        return self.request('organization_query_children_length',
                            array_of_roleids)

    # ===========================================================================
    # End Organization Methods
    # ===========================================================================

    # ===========================================================================
    # Begin Report Methods
    # ===========================================================================

    def report_create(self, report_list):
        """ Create Report

            Keyword arguments:
            report_list -- list of reports
        """
        array_of_reports = self.client.factory.create('ArrayOfReport')
        for report in report_list:
            array_of_report_parameters = self.client.factory.create('ArrayOfReportParameter')
            report_param_object = self.client.factory.create('ReportParameter')
            report_object = self.client.factory.create('Report')
            report_dict = utils.lower_keys(report)
            report_object.OutputFormat = report_dict.get('outputformat', None)
            report_object.Name = report_dict.get('name', None)
            report_object.ZipOutput = report_dict.get('zipoutput', None)
            report_object.ReportTypeName = report_dict.get('reporttypename', None)
            report_object.DeliveryEvent = report_dict.get('deliveryevent', None)
            report_object.OrganizationId = report_dict.get('organizationid', None)
            report_object.ReportTypeId = report_dict.get('reporttypeid', None)
            report_object.TimeZoneId = report_dict.get('timezoneid', None)

            for report_param in utils.find_key('reportparameter', report_dict):
                report_param_object.Name = report_param.get('name', None)
                report_param_object.Value = report_param.get('value', None)
                array_of_report_parameters.ReportParameter.append(report_param_object)

            report_object.ReportParameters = array_of_report_parameters
            array_of_reports.Report.append(report_object)

        return self.request('report_create',
                            array_of_reports)

    def report_delete_by_id(self):
        pass

    def report_query_by_id(self, reportid_list):
        """ Query Report By Id

            Keyword arguments:
            orgid_list -- list of org ids
        """
        array_of_reportids = self.client.factory.create('ArrayOfstring')

        for reportid in reportid_list:
            array_of_reportids.string.append(reportid)

        return self.request('report_query_by_id',
                            array_of_reportids)

    def report_type_query_by_id(self, reporttypeid_list):
        """ Query Report Type By Id

            Keyword arguments:
            reporttypeid_list -- list of report type ids
        """
        array_of_reporttypeids = self.client.factory.create('ArrayOfstring')

        for reporttypeid in reporttypeid_list:
            array_of_reporttypeids.string.append(reporttypeid)

        return self.request('report_type_query_by_id',
                            array_of_reporttypeids)

    def report_type_query_by_organizationid(self, orgid_list, index=0, length=300):
        """ Query Report Types By Organization Id

            Keyword arguments:
            orgid_list -- list of org ids
            index      -- starting index
            length     -- number of report types to return
        """
        array_of_orgids = self.client.factory.create('ArrayOfstring')

        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('report_type_query_by_organizationid',
                            array_of_orgids,
                            index,
                            length)

    def report_type_query_by_organizationid_length(self, orgid_list):
        """ Returns Length Of Query Report Types By Organization Id

            Keyword arguments:
            orgid_list -- list of org ids
        """
        array_of_orgids = self.client.factory.create('ArrayOfstring')

        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('report_type_query_by_organizationid_length',
                            array_of_orgids)

    # ===========================================================================
    # End Report Methods
    # ===========================================================================

    # ===========================================================================
    # Begin Scenario Methods
    # ===========================================================================

    def scenario_activate(self):
        pass

    def scenario_create(self):
        pass

    def scenario_delete_by_id(self, scenarioid_list):
        """ Delete Scenario By Id

            Keyword arguments:
            scenarioid_list -- list of scenario ids
        """
        array_of_scenarioids = self.client.factory.create('ArrayOfstring')

        for scenarioid in scenarioid_list:
            array_of_scenarioids.string.append(scenarioid)

        return self.request('scenario_delete_by_id',
                            array_of_scenarioids)

    def scenario_query_by_accesscode(self, accesscode_list):
        """ Query Scenario By Access Code

            Keyword arguments:
            scenarioid_list -- list of scenario ids
        """
        array_of_access_codes = self.client.factory.create('ArrayOfstring')

        for access_code in accesscode_list:
            array_of_access_codes.string.append(access_code)

        return self.request('scenario_query_by_accesscode',
                            array_of_access_codes)

    def scenario_query_by_id(self, scenarioid_list):
        """ Query Scenario By Id

            Keyword arguments:
            scenarioid_list -- list of scenario ids
        """
        array_of_scenarioids = self.client.factory.create('ArrayOfstring')

        for scenarioid in scenarioid_list:
            array_of_scenarioids.string.append(scenarioid)

        return self.request('scenario_query_by_id',
                            array_of_scenarioids)

    def scenario_query_by_name(self, scenario_name_list):
        """ Query Scenario By Name

            Keyword arguments:
            scenario_name_list -- list of scenario names
        """
        array_of_scenario_names = self.client.factory.create('ArrayOfstring')

        for scenario_name in scenario_name_list:
            array_of_scenario_names.string.append(scenario_name)

        return self.request('scenario_query_by_name',
                            array_of_scenario_names)

    def scenario_query_by_organizationid(self, orgid_list, index=0, length=300):
        """ Query Scenarios By Organization Id

            Keyword arguments:
            orgid_list -- list of org ids
            index      -- starting index
            length     -- number of scenarios to return
        """
        array_of_orgids = self.client.factory.create('ArrayOfstring')

        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('scenario_query_by_organizationid',
                            array_of_orgids,
                            index,
                            length)

    def scenario_query_by_organizationid_length(self, orgid_list):
        """ Returns Length Of Query Scenarios By Organization Id

            Keyword arguments:
            orgid_list -- list of org ids
        """
        array_of_orgids = self.client.factory.create('ArrayOfstring')

        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('scenario_query_by_organizationid_length',
                            array_of_orgids)

    # ===========================================================================
    # End Scenario Methods
    # ===========================================================================

    # ===========================================================================
    # Begin ScheduledEvent Methods
    # ===========================================================================

    # Will create methods as needed.

    # ===========================================================================
    # End ScheduledEvent Methods
    # ===========================================================================

    # ===========================================================================
    # Begin Security Methods
    # ===========================================================================

    def administrator_create(self, administrator_list):
        """ Creates Administrators

            Keyword arguments:
            administrator_list -- list of administrators
        """
        array_of_administrators = self.client.factory.create('ArrayOfAdministrator')

        for administrator in administrator_list:
            administrator_object = self.client.factory.create('Administrator')
            administrator_dict = utils.lower_keys(administrator)
            administrator_object.Active = administrator_dict.get('active', None)
            administrator_object.MemberId = administrator_dict.get('memberid', None)
            administrator_object.DefaultFolderId = administrator_dict.get('defaultfolderid', None)
            array_of_administrators.Administrator.append(administrator_object)

        return self.request('administrator_create', array_of_administrators)

    def folder_delete_by_id(self, folderid_list):
        """ Delete Folder By Id

            Keyword arguments:
            folderid_list -- list of folder ids
        """
        array_of_folderids = self.client.factory.create('ArrayOfstring')

        for folderid in folderid_list:
            array_of_folderids.string.append(folderid)

        return self.request('folder_delete_by_id',
                            array_of_folderids)

    def folder_query_by_organizationid(self, orgid_list, index=0, length=300):
        """ Query Folders By Organization Id

            Keyword arguments:
            orgid_list -- list of org ids
            index      -- starting index
            length     -- number of scenarios to return
        """
        array_of_orgids = self.client.factory.create('ArrayOfstring')

        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('folder_query_by_organizationid',
                            array_of_orgids,
                            index,
                            length)
    # Will create methods as needed.

    # ===========================================================================
    # End Security Methods
    # ===========================================================================

    # ===========================================================================
    # Begin Team Methods
    # ===========================================================================

    def team_create(self, team_list):
        """ Creates Teams

            Keyword arguments:
            team_list -- list of teams
        """
        array_of_teams = self.client.factory.create('ArrayOfTeam')

        for team in team_list:
            team_object = self.client.factory.create('Team')
            team_admins = self.client.factory.create('ArrayOfTeamAdministrator')
            team_dict = utils.lower_keys(team)
            team_object.TeamId = team_dict.get('teamid', None)
            team_object.Name = team_dict.get('name', None)
            team_object.EscalationId = team_dict.get('escalationid', None)
            team_object.Source = team_dict.get('source', None)
            team_object.Type = team_dict.get('type', None)
            team_object.SourceIdentifier = team_dict.get('sourceidentifier', None)
            team_object.ReadOnlyInUserInterface = team_dict.get('readonlyinuserinterface', None)
            team_object.AccessCode = team_dict.get('accesscode', None)
            team_object.OrganizationId = team_dict.get('organizationid', None)

            for team_admin in utils.find_key('teamadministrator', team_dict):
                team_admin_member_object = self.client.factory.create('TeamAdministratorMember')
                team_admin_member_object.TeamId = team_admin.get('teamid', None)
                team_admin_member_object.TeamRoleId = team_admin.get('teamroleid', None)
                team_admin_member_object.MemberId = team_admin.get('memberid', None)
                team_admins.TeamAdministrator.append(team_admin)

            team_object.TeamAdministrators = team_admins
            array_of_teams.Team.append(team_object)

        return self.request('team_create',
                            array_of_teams)

    def team_delete_by_id(self, teamid_list):
        """ Delete Team By TeamId

            Keyword arguments:
            teamid_list -- list of team ids
        """
        array_of_teamids = self.client.factory.create('ArrayOfstring')

        for teamid in teamid_list:
            array_of_teamids.string.append(teamid)

        return self.request('team_delete_by_id',
                            array_of_teamids)

    def team_entry_create(self):
        pass

    def team_entry_delete_by_id(self, team_entry_id_list):
        """ Delete Team Entry By TeamEntryId

            Keyword arguments:
            team_entry_id_list -- list of team entry ids
        """
        array_of_team_entry_ids = self.client.factory.create('ArrayOfstring')

        for team_entry_id in team_entry_id_list:
            array_of_team_entry_ids.string.append(team_entry_id)

        return self.request('team_entry_delete_by_id',
                            array_of_team_entry_ids)

    def team_entry_member_query_by_memberid(self, memberid_list, index=0, length=300):
        """ Query Team Entries By Member Id

            Keyword arguments:
            memberid_list -- list of member ids
            index      -- starting index
            length     -- number of team entries to return
        """
        array_of_memberids = self.client.factory.create('ArrayOfstring')

        for memberid in memberid_list:
            array_of_memberids.string.append(memberid)

        return self.request('team_entry_member_query_by_memberid',
                            array_of_memberids,
                            index,
                            length)

    def team_entry_member_query_by_memberid_length(self, memberid_list):
        """ Returns Length Of Query Team Entries By Member Id

            Keyword arguments:
            memberid_list -- list of member ids
            index      -- starting index
            length     -- number of team entries to return
        """
        array_of_memberids = self.client.factory.create('ArrayOfstring')

        for memberid in memberid_list:
            array_of_memberids.string.append(memberid)

        return self.request('team_entry_member_query_by_memberid_length',
                            array_of_memberids)

    def team_entry_query_by_id(self, team_entryid_list):
        """ Query Team Entries By Id

            Keyword arguments:
            teamid_list -- list of team ids
        """
        array_of_team_entryids = self.client.factory.create('ArrayOfstring')

        for team_entryid in team_entryid_list:
            array_of_team_entryids.string.append(team_entryid)

        return self.request('team_entry_query_by_id',
                            array_of_team_entryids)

    def team_entry_query_by_organizationid(self, teamid_list, index=0, length=300):
        """ Query Team Entries By Organization Id

            Keyword arguments:
            teamid_list -- list of team ids
            index      -- starting index
            length     -- number of team entries to return
        """
        array_of_teamids = self.client.factory.create('ArrayOfstring')

        for teamid in teamid_list:
            array_of_teamids.string.append(teamid)

        return self.request('team_entry_query_by_organizationid',
                            array_of_teamids,
                            index,
                            length)

    def team_entry_query_by_organizationid_length(self, teamid_list):
        """ Returns Length Of Query Team Entries By Organization Id

            Keyword arguments:
            teamid_list -- list of team ids
        """
        array_of_teamids = self.client.factory.create('ArrayOfstring')

        for teamid in teamid_list:
            array_of_teamids.string.append(teamid)

        return self.request('team_entry_query_by_organizationid_length',
                            array_of_teamids)

    def team_entry_query_by_teamid(self, teamid_list, index=0, length=300):
        """ Query Team Entries By Team Id

            Keyword arguments:
            teamid_list -- list of team ids
            index      -- starting index
            length     -- number of team entries to return
        """
        array_of_teamids = self.client.factory.create('ArrayOfstring')

        for teamid in teamid_list:
            array_of_teamids.string.append(teamid)

        return self.request('team_entry_query_by_teamid',
                            array_of_teamids,
                            index,
                            length)

    def team_entry_query_by_teamid_length(self, teamid_list):
        """ Returns Length Of Query Team Entries By Team Id

            Keyword arguments:
            teamid_list -- list of team ids
        """
        array_of_teamids = self.client.factory.create('ArrayOfstring')

        for teamid in teamid_list:
            array_of_teamids.string.append(teamid)

        return self.request('team_entry_query_by_teamid_length',
                            array_of_teamids)

    def team_entry_update(self):
        pass

    def team_member_query_by_teamid(self, teamid):
        """ Query Team Members By Team Id

            Keyword arguments:
            teamid -- team id
        """

        return self.request('team_member_query_by_teamid',
                            teamid)

    def team_query_by_accesscode(self, accesscode_list):
        """ Query Teams By Access Code

            Keyword arguments:
            accesscode_list -- list of access codes
        """
        array_of_access_codes = self.client.factory.create('ArrayOfstring')

        for accesscode in accesscode_list:
            array_of_access_codes.string.append(accesscode)

        return self.request('team_query_by_accesscode',
                            array_of_access_codes)

    def team_query_by_id(self, teamids_list):
        """ Query Teams By Id

            Keyword arguments:
            teamids_list -- list of team ids
        """
        array_of_teamids = self.client.factory.create('ArrayOfstring')

        for teamid in teamids_list:
            array_of_teamids.string.append(teamid)

        return self.request('team_query_by_id',
                            array_of_teamids)

    def team_query_by_name(self, teamname_list):
        """ Query Teams By Name

            Keyword arguments:
            teamname_list -- list of team names
        """
        array_of_teamnames = self.client.factory.create('ArrayOfstring')

        for teamname in teamname_list:
            array_of_teamnames.string.append(teamname)

        return self.request('team_query_by_name',
                            array_of_teamnames)

    def team_query_by_organizationid(self,
                                     orgid_list,
                                     index=0,
                                     length=300):
        """ Query Teams By Organization Id

            Keyword arguments:
            orgid_list -- list of org ids
            index      -- starting index
            length     -- number of teams to return
        """
        array_of_orgids = self.client.factory.create('ArrayOfstring')

        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('team_query_by_organizationid',
                            array_of_orgids,
                            index,
                            length)

    def team_query_by_organizationid_length(self, orgid_list):
        """ Query Teams By Organization Id

            Keyword arguments:
            orgid_list -- list of org ids
        """
        array_of_orgids = self.client.factory.create('ArrayOfstring')

        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('team_query_by_organizationid_length',
                            array_of_orgids)

    def team_query_by_sourceidentifier(self, sourceids_list):
        """ Query Teams By Source Identifiers

            Keyword arguments:
            sourceids_list -- list of source ids
        """
        array_of_sourceids = self.client.factory.create('ArrayOfstring')

        for sourceid in sourceids_list:
            array_of_sourceids.string.append(sourceid)

        return self.request('team_query_by_sourceidentifier',
                            array_of_sourceids)

    def team_query_by_subteamid(self, subteamid_list, index=0, length=300):
        """ Query Teams By Sub Team Id

            Keyword arguments:
            subteamid_list -- list of sub team ids
            index      -- starting index
            length     -- number of teams to return

        """
        array_of_subteamids = self.client.factory.create('ArrayOfstring')

        for subteamid in subteamid_list:
            array_of_subteamids.string.append(subteamid)

        return self.request('team_query_by_subteamid',
                            array_of_subteamids,
                            index,
                            length)

    def team_query_by_subteamid_length(self, subteamid_list):
        """ Returns Length Of Query Teams By Sub Team Id

            Keyword arguments:
            subteamid_list -- list of sub team ids
        """
        array_of_subteamids = self.client.factory.create('ArrayOfstring')

        for subteamid in subteamid_list:
            array_of_subteamids.string.append(subteamid)

        return self.request('team_query_by_subteamid_length',
                            array_of_subteamids)

    def team_role_create(self,
                         team_role_list):
        """ Creates Team Roles

            Keyword arguments:
            team_role_list -- list of team roles
        """
        array_of_team_roles = self.client.factory.create('ArrayOfTeamRole')

        for team_role in team_role_list:
            team_role_object = self.client.factory.create('TeamRole')
            team_role_dict = utils.lower_keys(team_role)
            team_role_object.TeamRoleId = team_role_dict.get('teamroleid', None)
            team_role_object.Name = team_role_dict.get('name', None)
            team_role_object.CanManage = team_role_dict.get('canmanage', False)
            team_role_object.CanActivate = team_role_dict.get('canactivate', False)
            team_role_object.CanView = team_role_dict.get('canview', False)
            team_role_object.OrganizationId = team_role_dict.get('organizationid', None)
            array_of_team_roles.TeamRole.append(team_role_object)

        return self.request('team_role_create',
                            array_of_team_roles)

    def team_role_delete_by_id(self,
                               team_role_id_list):
        """ Delete Team Roles By Id

            Keyword arguments:
            team_role_id_list -- list of team role ids
        """
        array_of_team_role_ids = self.client.factory.create('ArrayOfstring')

        for team_role_id in team_role_id_list:
            array_of_team_role_ids.string.append(team_role_id)

        return self.request('team_role_delete_by_id',
                            array_of_team_role_ids)

    def team_role_query_by_id(self,
                              team_role_id_list):
        """ Query Team Roles By Id

            Keyword arguments:
            team_role_id_list -- list of team role ids
        """
        array_of_team_role_ids = self.client.factory.create('ArrayOfstring')

        for team_role_id in team_role_id_list:
            array_of_team_role_ids.string.append(team_role_id)

        return self.request('team_role_query_by_id',
                            array_of_team_role_ids)

    def team_role_query_by_name(self,
                                team_role_name_list):
        """ Query Team Roles By Name

            Keyword arguments:
            team_role_name_list -- list of team role names
        """
        array_of_team_role_names = self.client.factory.create('ArrayOfstring')

        for team_role_name in team_role_name_list:
            array_of_team_role_names.string.append(team_role_name)

        return self.request('team_role_query_by_name',
                            array_of_team_role_names)

    def team_role_query_by_organizationid(self,
                                          orgid_list,
                                          index=0,
                                          length=300):
        """ Query Team Roles By Organization Id

            Keyword arguments:
            orgid_list -- list of org ids
            index      -- starting index
            length     -- number of team roles to return
        """
        array_of_orgids = self.client.factory.create('ArrayOfstring')

        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('team_role_query_by_organizationid',
                            array_of_orgids,
                            index,
                            length)

    def team_role_query_by_organizationid_length(self,
                                                 orgid_list):
        """ Query Team Roles By Organization Id

            Keyword arguments:
            orgid_list -- list of org ids
        """
        array_of_orgids = self.client.factory.create('ArrayOfstring')

        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('team_role_query_by_organizationid_length',
                            array_of_orgids)

    def team_role_update(self):
        pass

    def team_update(self):
        pass

    # ===========================================================================
    # End Team Methods
    # ===========================================================================

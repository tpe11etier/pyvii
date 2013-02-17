# -*- coding: utf-8 -*-
import suds
import utils


class Error(Exception):
    '''Base class for exceptions'''
    pass


class APIError(Error):
    '''Exception raised when an error is received from api'''
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


class CredentialCheckFailed(Error):
    def __init__(self, header):
        self.header = header
        print '''Credential check failed.
                 url=%s,
                 Domain=%s,
                 UserId=%s,
                 UserPassword=%s,
                 OemId=%s,
                 OemPassword=%s''' % (self.header['url'],
                                      self.header['domain'],
                                      self.header['userid'],
                                      self.header['userpassword'],
                                      self.header['oemid'],
                                      self.header['oempassword'])

    def __str__(self):
        return repr('''Credential check failed. url=%s,
                                              Domain=%s,
                                              UserId=%s,
                                              UserPassword=%s,
                                              OemId=%s,
                                              OemPassword=%s''' % (self.header['url'],
                                                                   self.header['domain'],
                                                                   self.header['userid'],
                                                                   self.header['userpassword'],
                                                                   self.header['oemid'],
                                                                   self.header['oempassword']))


class Api(object):
    ''' Consumes WSDL and Authentication header.

        Keyword arguments:
        auth_header -- Dictionary containing url and credentials
    '''
    def __init__(self, auth_header):
        auth_header = dict((k.lower(), v) for k, v in auth_header.items())
        try:
            self.url = auth_header.get('url', None)
            self.client = suds.client.Client(self.url)
            self.header = self.client.factory.create('AuthHeader')
            self.header.Domain = auth_header.get('domain', None)
            self.header.UserId = auth_header.get('userid', None)
            self.header.UserPassword = auth_header.get(
                'userpassword', None)
            self.header.OemId = auth_header.get('oemid', None)
            self.header.OemPassword = auth_header.get('oempassword', None)
            self.client.set_options(soapheaders=self.header)

            #Authenticating on initialization to make sure credentials are valid.
            self.client.service.OrganizationQueryRoot()

            service = self.client.service

            self.methods = {'organization_query_by_id': service.OrganizationQueryById,
                            'organization_event_type_query_by_organizationid': service.OrganizationEventTypeQueryByOrganizationId,
                            'escalation_create': service.OrganizationEventTypeQueryByOrganizationId,
                            'escalation_create': service.OrganizationEventTypeQueryByOrganizationId,
                            'escalation_delete_by_id': service.OrganizationEventTypeQueryByOrganizationId,
                            'escalation_query_by_id': service.EscalationQueryById,
                            'escalation_query_by_memberid_permission': service.EscalationQueryByMemberIdPermission,
                            'escalation_query_by_memberid_permission_length': service.EscalationQueryByMemberIdPermissionLength,
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
                            'import_definition_delet_by_id': service.ImportDefinitionDeleteById,
                            'import_definition_query_by_id': service.ImportDefinitionQueryById,
                            'import_definition_query_by_oganizationid': service.ImportDefinitionQueryByOrganizationId,
                            'import_definition_query_by_organizationi_length': service.ImportDefinitionQueryByOrganizationIdLength,
                            'import_exception_query_by_importid': service.ImportExceptionQueryByImportId,
                            'import_exception_query_by_importid_length': service.ImportExceptionQueryByImportIdLength,
                            'import_query_by_id': service.ImportQueryById,
                            'import_query_by_organizationid': service.ImportQueryByOrganizationId,
                            'import_query_by_organizationid_length': service.ImportQueryByOrganizationIdLength,
                            'member_create': service.MemberCreate,
                            'member_custom_field_simpleset': service.MemberCustomFieldSimpleSet,
                            'member_delete_by_id': service.MemberDeleteById,
                            'member_dialin_credential_create': service.MemberDialinCredentialCreate,
                            'member_dialin_credential_delete_by_memberid': service.MemberDialinCredentialDeleteByMemberId,
                            'member_dialin_credential_query_by_memberid': service.MemberDialinCredentialQueryByMemberId,
                            'member_dialin_credential_update': service.MemberDialinCredentialUpdate,
                            'member_group_query_by_memberidpermission': service.MemberGroupQueryByMemberIdPermission,
                            'member_group_query_by_memberid_permission_length': service.MemberGroupQueryByMemberIdPermissionLength,
                            'member_query_by_dialinid': service.MemberQueryByDialinId,
                            'member_query_by_emailaddress': service.MemberQueryByEmailAddress,
                            'member_query_by_emailaddresslength': service.MemberQueryByEmailAddressLength,
                            'member_query_by_event_subscription': service.MemberQueryByEventSubscription,
                            'member_query_by_event_subscription_daterange': service.MemberQueryByEventSubscriptionDateRange,
                            'member_query_by_event_subscription_daterange_length': service.MemberQueryByEventSubscriptionDateRangeLength,
                            'member_query_by_event_subscription_length': service.MemberQueryByEventSubscriptionLength,
                            'member_query_by_id': service.MemberQueryById,
                            'member_query_by_lastname': service.MemberQueryByLastName,
                            'member_query_by_lastname_length': service.MemberQueryByLastNameLength,
                            'member_query_by_memberid_permission': service.MemberQueryByMemberIdPermission,
                            'member_query_by_memberid_permission_length': service.MemberQueryByMemberIdPermissionLength,
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
                            'organization_create': service.OrganizationCreate,
                            'organization_custom_field_create': service.OrganizationCustomFieldCreate,
                            'organization_custom_field_delete_by_id': service.OrganizationCustomFieldDeleteById,
                            'organization_custom_field_query_by_id': service.OrganizationCustomFieldQueryById,
                            'organization_custom_field_query_by_memberid_permission': service.OrganizationCustomFieldQueryByMemberIdPermission,
                            'organization_custom_field_query_by_memberid_permission_length': service.OrganizationCustomFieldQueryByMemberIdPermissionLength,
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
                            'report_query_by_memberid_permission': service.ReportQueryByMemberIdPermission,
                            'report_query_by_memberid_permissionlength': service.ReportQueryByMemberIdPermissionLength,
                            'report_type_query_by_id': service.ReportTypeQueryById,
                            'report_type_query_by_memberid_permission': service.ReportTypeQueryByMemberIdPermission,
                            'report_type_query_by_memberid_permission_length': service.ReportTypeQueryByMemberIdPermissionLength,
                            'report_type_query_by_organizationid': service.ReportTypeQueryByOrganizationId,
                            'report_type_query_by_organizationid_length': service.ReportTypeQueryByOrganizationIdLength,
                            'scenario_activate': service.ScenarioActivate,
                            'scenario_create': service.ScenarioCreate,
                            'scenario_delete_by_id': service.ScenarioDeleteById,
                            'scenario_query_by_accesscode': service.ScenarioQueryByAccessCode,
                            'scenario_query_by_id': service.ScenarioQueryById,
                            'scenario_query_by_memberid_permission': service.ScenarioQueryByMemberIdPermission,
                            'scenario_query_by_memberid_permission_length': service.ScenarioQueryByMemberIdPermissionLength,
                            'scenario_query_by_name': service.ScenarioQueryByName,
                            'scenario_query_by_organizationid': service.ScenarioQueryByOrganizationId,
                            'scenario_query_by_organizationid_length': service.ScenarioQueryByOrganizationIdLength,
                            'team_create': service.TeamCreate,
                            'team_delete_by_id': service.TeamDeleteById,
                            'team_entry_create': service.TeamEntryCreate,
                            'team_entry_delete_by_id': service.TeamEntryDeleteById,
                            'team_entry_member_query_by_memberid': service.TeamEntryMemberQueryByMemberId,
                            'team_entry_member_query_by_memberid_length': service.TeamEntryMemberQueryByMemberIdLength,
                            'team_entry_member_query_by_memberid_teamid': service.TeamEntryMemberQueryByMemberIdTeamId,
                            'team_entry_query_by_id': service.TeamEntryQueryById,
                            'team_entry_query_by_organizationid': service.TeamEntryQueryByOrganizationId,
                            'team_entry_query_by_organizationid_length': service.TeamEntryQueryByOrganizationIdLength,
                            'team_entry_query_by_teamid': service.TeamEntryQueryByTeamId,
                            'team_entry_query_by_teamid_length': service.TeamEntryQueryByTeamIdLength,
                            'team_entry_subteam_query_by_subteamid': service.TeamEntrySubTeamQueryBySubTeamId,
                            'team_entry_subteam_query_by_subteamid_length': service.TeamEntrySubTeamQueryBySubTeamIdLength,
                            'team_entry_subteam_query_by_subteamid_teamid': service.TeamEntrySubTeamQueryBySubTeamIdTeamId,
                            'team_entry_update': service.TeamEntryUpdate,
                            'team_member_query_by_teamid': service.TeamMemberQueryByTeamId,
                            'team_query_by_accesscode': service.TeamQueryByAccessCode,
                            'team_query_by_id': service.TeamQueryById,
                            'team_query_by_memberid_permission': service.TeamQueryByMemberIdPermission,
                            'team_query_by_memberid_permission_length': service.TeamQueryByMemberIdPermissionLength,
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
                            'team_role_query_by_organizationidlength': service.TeamRoleQueryByOrganizationIdLength,
                            'team_role_update': service.TeamRoleUpdate,
                            'team_update': service.TeamUpdate
                            }

        except suds.WebFault:
            raise CredentialCheckFailed(auth_header)

    def request(self, method, *args):
        self.method = method
        self.args = args
        ''' Handles all requests.

            Keyword arguments:
            method -- SOAP method called
            args   -- SOAP method args
        '''
        try:
            return self.methods[self.method](*self.args)
        except suds.WebFault as error:
            raise APIError(error)

    # ===========================================================================
    # Begin Escalation Methods
    # ===========================================================================

    def escalation_create(self,
                          escalation_list):
        ''' Creates Escalation Rules.

            Keyword arguments:
            escalation_list -- list of escalation dicts
        '''

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
        ''' Deletes Escalation Rules by Id.

            Keyword arguments:
            escalationid_list -- list of escalation ids
        '''
        array_of_escalationids = self.client.factory.create('ArrayOfstring')
        for escalationid in escalationid_list:
            array_of_escalationids.string.append(escalationid)

        return self.request('escalation_delete_by_id', array_of_escalationids)

    def escalation_query_by_id(self,
                               escalationid_list):
        ''' Query Escalation Rules by Id.

            Keyword arguments:
            escalationid_list -- list of escalation ids
        '''
        array_of_escalationids = self.client.factory.create('ArrayOfstring')
        for escalationid in escalationid_list:
            array_of_escalationids.string.append(escalationid)

        return self.request('escalation_query_by_id', array_of_escalationids)

    def escalation_query_by_memberid_permission(self):
        pass

    def escalation_query_by_memberid_permission_length(self):
        pass

    def escalation_query_by_name(self,
                                 escalation_name_list):
        ''' Query Escalation Rules by Name.

            Keyword arguments:
            escalation_name_list -- list of escalation names
        '''
        array_of_escalation_names = self.client.factory.create('ArrayOfstring')
        for escalation_name in escalation_name_list:
            array_of_escalation_names.string.append(escalation_name)

        return self.request('escalation_query_by_name', array_of_escalation_names)

    def escalation_query_by_organizationid(self,
                                           orgid_list,
                                           index=0,
                                           length=300):
        ''' Returns Escalation Rules by Organization Id

            Keyword arguments:
            orgid_list -- list of org ids
            index      -- starting index
            length     -- number of orgs to return

        '''
        array_of_orgids = self.client.factory.create('ArrayOfstring')
        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('escalation_query_by_organizationid',
                            array_of_orgids,
                            index,
                            length)

    def escalation_query_by_organizationid_length(self,
                                                  orgid_list):
        ''' Returns Length of  Escalation Rules

            Keyword arguments:
            orgid_list -- list of org ids
        '''
        array_of_orgids = self.client.factory.create('ArrayOfstring')
        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('escalation_query_by_organizationid_length', array_of_orgids)

    def escalation_type_query_by_id(self,
                                    escalation_type_id_list):
        ''' Query Escalation Rules by Id.

            Keyword arguments:
            escalationid_list -- list of escalation ids
        '''
        array_of_escalation_type_ids = self.client.factory.create('ArrayOfstring')
        for escalation_type_id in escalation_type_id_list:
            array_of_escalation_type_ids.string.append(escalation_type_id)

        return self.request('escalation_type_query_by_id', array_of_escalation_type_ids)

    def escalation_type_query_by_name(self,
                                      escalation_type_name_list):
        ''' Query Escalation Rules by Name.

            Keyword arguments:
            escalation_type_name_list -- list of escalation names
        '''
        array_of_escalation_type_names = self.client.factory.create('ArrayOfstring')
        for escalation_type_name in escalation_type_name_list:
            array_of_escalation_type_names.string.append(escalation_type_name)

        return self.request('escalation_type_query_by_name', array_of_escalation_type_names)

    def escalation_type_query_by_organizationid(self,
                                                orgid_list,
                                                index=0,
                                                length=300):
        ''' Returns Escalation Types by Organization Id

            Keyword arguments:
            orgid_list -- list of org ids
            index      -- starting index
            length     -- number of orgs to return
        '''
        array_of_orgids = self.client.factory.create('ArrayOfstring')
        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('escalation_type_query_by_organizationid',
                            array_of_orgids,
                            index,
                            length)

    def escalation_type_query_by_organizationid_length(self,
                                                       orgid_list):
        ''' Returns Length of Escalation Types

            Keyword arguments:
            orgid_list -- list of org ids
        '''
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
        ''' Cancels Import by Import Id.

            Keyword arguments:
            importid_list -- list of import ids
        '''
        array_of_importids = self.client.factory.create('ArrayOfstring')
        for importid in importid_list:
            array_of_importids.string.append(importid)

        return self.request('import_cancel', array_of_importids)

    def import_confirm(self,
                       importid_list):
        ''' Confirms Import by Import Id.

            Keyword arguments:
            importid_list -- list of import ids
        '''
        array_of_importids = self.client.factory.create('ArrayOfstring')
        for importid in importid_list:
            array_of_importids.string.append(importid)

        return self.request('import_confirm', array_of_importids)

    def import_create(self):
        pass

    def import_definition_create(self):
        pass

    def import_definition_delete_by_id(self):
        pass

    def import_definition_query_by_id(self):
        pass

    def import_definition_query_by_organizationid(self):
        pass

    def import_definition_query_by_organizationid_length(self):
        pass

    def import_exception_query_by_importid(self):
        pass

    def import_exception_query_by_importid_length(self):
        pass

    def import_query_by_id(self):
        pass

    def import_query_by_organizationid(self):
        pass

    def import_query_by_organizationid_length(self):
        pass

    # ===========================================================================
    # End Import Methods
    # ===========================================================================

    # ===========================================================================
    # Begin Member Methods
    # ===========================================================================

    def member_create(self, member_list):
        '''Creates members.'''
        members = self.client.factory.create('ArrayOfMember')
        for member in member_list:
            member_object = self.client.factory.create('Member')
            contact_methods = self.client.factory.create('ArrayOfContactMethod')
            custom_fields = self.client.factory.create('ArrayOfMemberCustomField')
            member_dict = utils.lower_keys(member)
            for k, v in member_dict.items():
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

    def member_custom_field_simpleset(self):
        pass

    def member_delete_by_id(self):
        pass

    def member_dialin_credential_create(self):
        pass

    def member_dialin_credential_delete_by_memberid(self):
        pass

    def member_dialin_credential_query_by_memberid(self):
        pass

    def member_dialin_credential_update(self):
        pass

    def member_group_query_by_memberidpermission(self):
        pass

    def member_group_query_by_memberid_permission_length(self):
        pass

    def member_query_by_dialinid(self):
        pass

    def member_query_by_emailaddress(self):
        pass

    def member_query_by_emailaddresslength(self):
        pass

    def member_query_by_event_subscription(self):
        pass

    def member_query_by_event_subscription_daterange(self):
        pass

    def member_query_by_event_subscription_daterange_length(self):
        pass

    def member_query_by_event_subscription_length(self):
        pass

    def member_query_by_id(self):
        pass

    def member_query_by_lastname(self):
        pass

    def member_query_by_lastname_length(self):
        pass

    def member_query_by_memberid_permission(self):
        pass

    def member_query_by_memberid_permission_length(self):
        pass

    def member_query_by_organizationid(self):
        pass

    def member_query_by_organizationid_length(self):
        pass

    def member_query_by_roleid(self):
        pass

    def member_query_by_roleid_length(self):
        pass

    def member_query_by_sourceidentifier(self):
        pass

    def member_query_by_useridentifier(self):
        pass

    def member_query_by_username(self):
        pass

    def member_sourceidentifier_query_by_organizationid(self):
        pass

    def member_update(self):
        pass

    def timezone_query_all(self):
        pass

    def timezone_query_by_id(self):
        pass

    # ===========================================================================
    # End Member Methods
    # ===========================================================================

    # ===========================================================================
    # Begin Organization Methods
    # ===========================================================================

    def available_contact_method_query_by_organizationid(self,
                                                         orgid_string):
        ''' Returns Organization Contact Methods.

            Keyword arguments:
            orgid_string -- org id string

        '''
        return self.request('available_contact_method_query_by_organizationid', orgid_string)

    def billing_plan_query_by_organizationid(self,
                                             orgid_string):
        ''' Returns the Billing Plans available in the organization.

            Keyword arguments:
            orgid_string -- org id string
        '''
        return self.request('billing_plan_query_by_organizationid', orgid_string)

    def organization_create(self):
        pass

    def organization_custom_field_create(self):
        pass

    def organization_custom_field_delete_by_id(self):
        pass

    def organization_custom_field_query_by_id(self):
        pass

    def organization_custom_field_query_by_memberid_permission(self):
        pass

    def organization_custom_field_query_by_memberid_permission_length(self):
        pass

    def organization_custom_field_query_by_organizationid(self,
                                                          orgid_list,
                                                          index=0,
                                                          length=300):
        ''' Returns Custom Fields

            Keyword arguments:
            orgid_list -- list of org ids
            index      -- starting index
            length     -- number of orgs to return

        '''
        array_of_orgids = self.client.factory.create('ArrayOfstring')
        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('organization_custom_field_query_by_organizationid',
                            array_of_orgids,
                            index,
                            length)

    def organization_custom_field_query_by_organizationid_length(self,
                                                                 orgid_list):
        ''' Returns Length of Custom Fields

            Keyword arguments:
            orgid_list -- list of org ids
        '''
        array_of_orgids = self.client.factory.create('ArrayOfstring')
        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('organization_custom_field_query_by_organizationid_length', array_of_orgids)

    def organization_custom_field_query_by_organizationid_name(self,
                                                               orgid_list,
                                                               name,
                                                               index=0,
                                                               length=300):
        ''' Returns Organization Custom Fields by Name

            Keyword arguments:
            orgid_list -- list of org ids
            name       -- custom field name
            index      -- starting index
            length     -- number of orgs to return
        '''
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
        ''' Returns Length of Custom Fields by Org Id and Custom Field Name

            Keyword arguments:
            orgid_list -- list of org ids
        '''
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
        ''' Returns Custom Fields by Org Id and Custom Field Type

            Keyword arguments:
            orgid_list        -- list of org ids
            custom_field_type -- custom field type
            index             -- starting index
            length            -- number of custom fields to return
        '''
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
        ''' Returns Length of Custom Fields by Org Id and Custom Field Type

            Keyword arguments:
            orgid_list        -- list of org ids
            custom_field_type -- custom field type
        '''
        array_of_orgids = self.client.factory.create('ArrayOfstring')
        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('organization_custom_field_query_by_organizationid_type_length',
                            array_of_orgids,
                            custom_field_type)

    def organization_custom_field_update(self):
        pass

    def organization_event_type_query_by_id(self,
                                            eventid_list):

        ''' Returns Organization Event Type by Id

            Keyword arguments:
            eventid_list -- list of event ids
        '''
        array_of_eventids = self.client.factory.create('ArrayOfstring')

        for eventid in eventid_list:
            array_of_eventids.string.append(eventid)

        return self.request('organization_event_type_query_by_id',
                            array_of_eventids)

    def organization_event_type_query_by_organizationid(self,
                                                        orgid_list,
                                                        index=0,
                                                        length=300):
        ''' Returns Organization Event Types by Org Id

            Keyword arguments:
            orgid_list -- list of org ids
            index      -- starting index
            length     -- number of orgs to return
        '''
        array_of_orgids = self.client.factory.create('ArrayOfstring')

        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('organization_event_type_query_by_organizationid',
                            array_of_orgids,
                            index,
                            length)

    def organization_event_type_query_by_organizationid_length(self,
                                                               orgid_list):
        ''' Returns Length of Organization Event Types

            Keyword arguments:
            orgid_list -- list of org ids
        '''
        array_of_orgids = self.client.factory.create('ArrayOfstring')

        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('organization_event_type_query_by_organizationid_length',
                            array_of_orgids)

    def organization_query_by_id(self,
                                 orgid_list):
        ''' Returns Organization

            Keyword arguments:
            orgid_list -- list of org ids
        '''
        array_of_orgids = self.client.factory.create('ArrayOfstring')

        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.request('organization_query_by_id', array_of_orgids)

    def organization_query_children(self,
                                    orgid_string,
                                    index=0,
                                    length=300):
        ''' Returns Organization Sub-Orgs

            Keyword arguments:
            orgid_list -- list of org ids
            index      -- starting index
            length     -- number of orgs to return
        '''
        return self.request('organization_query_children',
                            orgid_string,
                            index,
                            length)

    def organization_query_children_length(self,
                                           orgid_string,
                                           index=0,
                                           length=300):
        ''' Returns Length of Organization Sub-Orgs

            Keyword arguments:
            orgid_list -- list of org ids
            index      -- starting index
            length     -- number of orgs to return
        '''
        return self.request('organization_query_children_length',
                            orgid_string,
                            index,
                            length)

    def organization_query_root(self):
        '''Returns OrganizationId, Events and Roles.'''

        return self.request('organization_query_root')

    def role_query_by_id(self,
                         roleid_list):
        ''' Returns Organization Role by RoleId

            Keyword arguments:
            roleid_list -- list of role idsx
        '''
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

    def report_create(self):
        pass

    def report_delete_by_id(self):
        pass

    def report_query_by_id(self):
        pass

    def report_query_by_memberid_permission(self):
        pass

    def report_query_by_memberid_permissionlength(self):
        pass

    def report_type_query_by_id(self):
        pass

    def report_type_query_by_memberid_permission(self):
        pass

    def report_type_query_by_memberid_permission_length(self):
        pass

    def report_type_query_by_organizationid(self):
        pass

    def report_type_query_by_organizationid_length(self):
        pass

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

    def scenario_delete_by_id(self):
        pass

    def scenario_query_by_accesscode(self):
        pass

    def scenario_query_by_id(self):
        pass

    def scenario_query_by_memberid_permission(self):
        pass

    def scenario_query_by_memberid_permission_length(self):
        pass

    def scenario_query_by_name(self):
        pass

    def scenario_query_by_organizationid(self):
        pass

    def scenario_query_by_organizationid_length(self):
        pass

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

                    # Will create methods as needed.

    # ===========================================================================
    # End Security Methods
    # ===========================================================================

    # ===========================================================================
    # Begin Team Methods
    # ===========================================================================

    def team_create(self):
        pass

    def team_delete_by_id(self):
        pass

    def team_entry_create(self):
        pass

    def team_entry_delete_by_id(self):
        pass

    def team_entry_member_query_by_memberid(self):
        pass

    def team_entry_member_query_by_memberid_length(self):
        pass

    def team_entry_member_query_by_memberid_teamid(self):
        pass

    def team_entry_query_by_id(self):
        pass

    def team_entry_query_by_organizationid(self):
        pass

    def team_entry_query_by_organizationid_length(self):
        pass

    def team_entry_query_by_teamid(self):
        pass

    def team_entry_query_by_teamid_length(self):
        pass

    def team_entry_subteam_query_by_subteamid(self):
        pass

    def team_entry_subteam_query_by_subteamid_length(self):
        pass

    def team_entry_subteam_query_by_subteamid_teamid(self):
        pass

    def team_entry_update(self):
        pass

    def team_member_query_by_teamid(self):
        pass

    def team_query_by_accesscode(self):
        pass

    def team_query_by_id(self):
        pass

    def team_query_by_memberid_permission(self):
        pass

    def team_query_by_memberid_permission_length(self):
        pass

    def team_query_by_name(self):
        pass

    def team_query_by_organizationid(self):
        pass

    def team_query_by_organizationid_length(self):
        pass

    def team_query_by_sourceidentifier(self):
        pass

    def team_query_by_subteamid(self):
        pass

    def team_query_by_subteamid_length(self):
        pass

    def team_role_create(self):
        pass

    def team_role_delete_by_id(self):
        pass

    def team_role_query_by_id(self):
        pass

    def team_role_query_by_name(self):
        pass

    def team_role_query_by_organizationid(self):
        pass

    def team_role_query_by_organizationidlength(self):
        pass

    def team_role_update(self):
        pass

    def team_update(self):
        pass

    # ===========================================================================
    # End Team Methods
    # ===========================================================================

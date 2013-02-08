# -*- coding: utf-8 -*-
import suds


class Api(object):
    ''' Consumes WSDL and Authentication header.

        Keyword arguments:
        auth_header -- Dictionary of credentials
    '''
    def __init__(self, auth_header):
        auth_header = dict((k.lower(), v) for k, v in auth_header.items())
        try:
            self.url = auth_header.get('url', None)
            if self.url is None:
                print 'url required'
            else:
                self.client = suds.client.Client(self.url)
                self.header = self.client.factory.create('AuthHeader')
                self.header.Domain = auth_header.get('domain', None)
                self.header.UserId = auth_header.get('userid', None)
                self.header.UserPassword = auth_header.get(
                    'userpassword', None)
                self.header.OemId = auth_header.get('oemid', None)
                self.header.OemPassword = auth_header.get('oempassword', None)
                self.client.set_options(soapheaders=self.header)
        except Exception as e:
            print e

    # ===========================================================================
    # Begin Escalation Methods
    # ===========================================================================

    def escalation_create(self,
                          escalation_list):
        #TODO - Come back to this
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
        if isinstance(escalationid_list, list):
            for escalationid in escalationid_list:
                array_of_escalationids.string.append(escalationid)
        else:
            # Do nothing.
            pass

        return self.client.service.EscalationDeleteById(array_of_escalationids)

    def escalation_query_by_id(self,
                               escalationid_list):
        ''' Query Escalation Rules by Id.

            Keyword arguments:
            escalationid_list -- list of escalation ids
        '''
        array_of_escalationids = self.client.factory.create('ArrayOfstring')
        if isinstance(escalationid_list, list):
            for escalationid in escalationid_list:
                array_of_escalationids.string.append(escalationid)
        else:
            # Do nothing.
            pass

        return self.client.service.EscalationQueryById(array_of_escalationids)

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
        if isinstance(escalation_name_list, list):
            for escalation_name in escalation_name_list:
                array_of_escalation_names.string.append(escalation_name)
        else:
            # Do nothing.
            pass

        return self.client.service.EscalationQueryByName(array_of_escalation_names)

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
        if isinstance(orgid_list, list):
            for orgid in orgid_list:
                array_of_orgids.string.append(orgid)
        else:
            # Do nothing.
            pass

        return self.client.service.EscalationQueryByOrganizationId(array_of_orgids,
                                                                   index,
                                                                   length)

    def escalation_query_by_organizationid_length(self,
                                                  orgid_list):
        ''' Returns Length of  Escalation Rules

            Keyword arguments:
            orgid_list -- list of org ids
        '''
        array_of_orgids = self.client.factory.create('ArrayOfstring')
        if isinstance(orgid_list, list):
            for orgid in orgid_list:
                array_of_orgids.string.append(orgid)
        else:
            # Do nothing.
            pass

        return self.client.service.EscalationQueryByOrganizationIdLength(array_of_orgids)

    def escalation_type_query_by_id(self,
                                    escalation_type_id_list):
        ''' Query Escalation Rules by Id.

            Keyword arguments:
            escalationid_list -- list of escalation ids
        '''
        array_of_escalation_type_ids = self.client.factory.create('ArrayOfstring')
        if isinstance(escalation_type_id_list, list):
            for escalation_type_id in escalation_type_id_list:
                array_of_escalation_type_ids.string.append(escalation_type_id)
        else:
            # Do nothing.
            pass

        return self.client.service.EscalationTypeQueryById(array_of_escalation_type_ids)

    def escalation_type_query_by_name(self,
                                      escalation_type_name_list):
        ''' Query Escalation Rules by Name.

            Keyword arguments:
            escalation_type_name_list -- list of escalation names
        '''
        array_of_escalation_type_names = self.client.factory.create('ArrayOfstring')
        if isinstance(escalation_type_name_list, list):
            for escalation_type_name in escalation_type_name_list:
                array_of_escalation_type_names.string.append(escalation_type_name)
        else:
            # Do nothing.
            pass

        return self.client.service.EscalationTypeQueryByName(array_of_escalation_type_names)

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
        if isinstance(orgid_list, list):
            for orgid in orgid_list:
                array_of_orgids.string.append(orgid)
        else:
            # Do nothing.
            pass

        return self.client.service.EscalationTypeQueryByOrganizationId(array_of_orgids,
                                                                       index,
                                                                       length)

    def escalation_type_query_by_organizationid_length(self,
                                                       orgid_list):
        ''' Returns Length of Escalation Types

            Keyword arguments:
            orgid_list -- list of org ids
        '''
        array_of_orgids = self.client.factory.create('ArrayOfstring')
        if isinstance(orgid_list, list):
            for orgid in orgid_list:
                array_of_orgids.string.append(orgid)
        else:
            # Do nothing.
            pass

        return self.client.service.EscalationTypeQueryByOrganizationIdLength(array_of_orgids)

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
        #TODO - Test
        ''' Cancels Import by Import Id.

            Keyword arguments:
            importid_list -- list of import ids
        '''
        array_of_importids = self.client.factory.create('ArrayOfstring')
        if isinstance(importid_list, list):
            for importid in importid_list:
                array_of_importids.string.append(importid)
        else:
            # Do nothing.
            pass

        return self.client.service.ImportCancel(array_of_importids)

    def import_confirm(self,
                       importid_list):
        #TODO - Test
        ''' Confirms Import by Import Id.

            Keyword arguments:
            importid_list -- list of import ids
        '''
        array_of_importids = self.client.factory.create('ArrayOfstring')
        if isinstance(importid_list, list):
            for importid in importid_list:
                array_of_importids.string.append(importid)
        else:
            # Do nothing.
            pass

        return self.client.service.ImportConfirm(array_of_importids)

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
            member_dict = dict((k.lower(), v) for k, v in member.items())
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
                member_object.ContactMethods = member_dict.get(
                    'contactmethods', None)
                member_object.MemberCustomFields = member_dict.get(
                    'membercustomfields', None)
            members.Member.append(member_object)

        try:
            return self.client.service.MemberCreate(members)
        except suds.WebFault as e:
            return e.fault.detail

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
        return self.client.service.AvailableContactMethodQueryByOrganizationId(orgid_string)

    def billing_plan_query_by_organizationid(self,
                                             orgid_string):
        ''' Returns the Billing Plans available in the organization.

            Keyword arguments:
            orgid_string -- org id string
        '''
        return self.client.service.BillingPlanQueryByOrganizationId(orgid_string)

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
        #TODO Deal with length - 300 limit
        ''' Returns Custom Fields

            Keyword arguments:
            orgid_list -- list of org ids
            index      -- starting index
            length     -- number of orgs to return

        '''
        array_of_orgids = self.client.factory.create('ArrayOfstring')
        if isinstance(orgid_list, list):
            for orgid in orgid_list:
                array_of_orgids.string.append(orgid)
        else:
            # Do nothing.
            pass

        return self.client.service.OrganizationCustomFieldQueryByOrganizationId(array_of_orgids,
                                                                                index,
                                                                                length)

    def organization_custom_field_query_by_organizationid_length(self,
                                                                 orgid_list):
        ''' Returns Length of Custom Fields

            Keyword arguments:
            orgid_list -- list of org ids
        '''
        array_of_orgids = self.client.factory.create('ArrayOfstring')
        if isinstance(orgid_list, list):
            for orgid in orgid_list:
                array_of_orgids.string.append(orgid)
        else:
            # Do nothing.
            pass

        return self.client.service.OrganizationCustomFieldQueryByOrganizationIdLength(array_of_orgids)

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

        return self.client.service.OrganizationCustomFieldQueryByOrganizationIdName(array_of_orgids,
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
        if isinstance(orgid_list, list):
            for orgid in orgid_list:
                array_of_orgids.string.append(orgid)
        else:
            # Do nothing.
            pass

        return self.client.service.OrganizationCustomFieldQueryByOrganizationIdNameLength(array_of_orgids,
                                                                                          custom_field_name)

    def organization_query_root(self):
        '''Returns OrganizationId, Events and Roles.'''
        org = self.client.service.OrganizationQueryRoot()

        return org

    def organization_event_type_query_by_id(self,
                                            eventid_list):

        ''' Returns Organization Event Type by Id

            Keyword arguments:
            eventid_list -- list of event ids
        '''
        array_of_eventids = self.client.factory.create('ArrayOfstring')

        for eventid in eventid_list:
            array_of_eventids.string.append(eventid)

        return self.client.service.OrganizationEventTypeQueryById(array_of_eventids)

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

        return self.client.service.OrganizationEventTypeQueryByOrganizationId(array_of_orgids,
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

        return self.client.service.OrganizationEventTypeQueryByOrganizationIdLength(array_of_orgids)

    def organization_query_by_id(self,
                                 orgid_list):
        ''' Returns Organization

            Keyword arguments:
            orgid_list -- list of org ids
        '''
        array_of_orgids = self.client.factory.create('ArrayOfstring')

        for orgid in orgid_list:
            array_of_orgids.string.append(orgid)

        return self.client.service.OrganizationQueryById(array_of_orgids)

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
        return self.client.service.OrganizationQueryChildren(orgid_string,
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
        return self.client.service.OrganizationQueryChildrenLength(orgid_string,
                                                                   index,
                                                                   length)

    def role_query_by_id(self,
                         roleid_list):
        ''' Returns Organization Role by RoleId

            Keyword arguments:
            roleid_list -- list of role idsx
        '''
        array_of_roleids = self.client.factory.create('ArrayOfstring')

        for roleid in roleid_list:
            array_of_roleids.string.append(roleid)

        return self.client.service.RoleQueryById(array_of_roleids)


    # ===========================================================================
    # End Organization Methods
    # ===========================================================================

    # ===========================================================================
    # Begin Report Methods
    # ===========================================================================

    # ===========================================================================
    # End Report Methods
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

    # ===========================================================================
    # End Team Methods
    # ===========================================================================

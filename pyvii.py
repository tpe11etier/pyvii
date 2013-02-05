import suds
import simplejson as json


def suds_to_json(suds_object):
    # Work in progress and may ditch it.
    json_dict = {}
    suds_object = suds_object
    for suds_object in suds_object:
        if isinstance(suds_object, tuple):
            key, value = suds_object
            if value and isinstance(key, str):
                for inner_key in value:
                    if isinstance(inner_key, tuple):
                        inner_key, inner_value = inner_key
                        json_dict[key] = inner_value
                    else:
                        json_dict[key] = value
    return json.dumps(json_dict, indent=4)


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
    # Begin Organization Methods
    # ===========================================================================

    def organization_query_root(self):
        '''Returns OrganizationId, Events and Roles.'''
        org = self.client.service.OrganizationQueryRoot()

        return org

    def billing_plan_query_by_organizationid(self, orgid_string):
        ''' Returns the Billing Plans available in the organization.


            Keyword arguments:
            orgid_string -- org id string
        '''
        if isinstance(orgid_string, str):
            self.orgid_string = orgid_string
            return self.client.service.BillingPlanQueryByOrganizationId(self.orgid_string)
        else:
            # Do nothing.
            pass

    def organization_custom_field_query_by_organizationid(self, orgid_list, index=0, length=300):
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

        return self.client.service.OrganizationCustomFieldQueryByOrganizationId(array_of_orgids, index, length)

    def organization_custom_field_query_by_organizationid_length(self, orgid_list):
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

    def available_contact_method_query_by_organizationid(self, orgid_string):
        ''' Returns Organization Contact Methods.

            Keyword arguments:
            orgid_string -- org id string

        '''
        if isinstance(orgid_string, str):
            return self.client.service.AvailableContactMethodQueryByOrganizationId(orgid_string)
        else:
            # Do nothing.
            pass

    def organization_custom_field_query_by_organizationid_name(self, orgid_list, name, index=0, length=300):
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

        return self.client.service.OrganizationCustomFieldQueryByOrganizationIdName(array_of_orgids, name, index, length)

    # ===========================================================================
    # End Organization Methods
    # ===========================================================================

    def member_create(self, member_array):
        '''Creates members.'''
        members = self.client.factory.create('ArrayOfMember')
        for member in member_array:
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


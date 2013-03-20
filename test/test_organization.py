import unittest

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pyvii')))

import pyvii

ORGID = ['10201']

AUTHHEADER = {
              'url': 'http://developer4.envoyww.com/WebService/EPAPI_1.0/wsdl.wsdl',
              'Domain': 'TPELLETIER',
              'userid': 'psadmin',
              'userpassword': 'W!sc0nsin',
              'oemid': 'TPELLETIERoem',
              'oempassword': 'TPELLETIER$1oem'
             }

class TestOrganizations(unittest.TestCase):

    def setUp(self):
        self.api = pyvii.Api(AUTHHEADER)


    # ===========================================================================
    # Begin Organization Methods
    # ===========================================================================

    def test_available_contact_method_query_by_organizationid(self):
        org_contact_methods = self.api.available_contact_method_query_by_organizationid(ORGID)
        self.assertIn('AvailableContactMethod', org_contact_methods)

    def test_billing_plan_query_by_organizationid(self):
        billing_plan = self.api.billing_plan_query_by_organizationid(ORGID)
        self.assertIn('BillingPlan', billing_plan)

    def test_organization_custom_field_create(self):
        self.org_custom_field_create = self.api.organization_custom_field_create([{'Name': 'xUNITTESTx',
                                                                       'Type': 'Field',
                                                                       'AdminAccEss': 'Read-Write',
                                                                       'useraccess': 'Read-Write',
                                                                       'organizationid': ORGID,
                                                                       'SEARCHABLE': 'True'}]
                                                                    )
        global org_custom_field_id
        org_custom_field_id =  self.org_custom_field_create.ResponseEntry[0]['Id']
        self.assertIn('ResponseEntry', self.org_custom_field_create)

    def test_organization_custom_field_query_by_id(self):
        org_custom_field_query = self.api.organization_custom_field_query_by_id([org_custom_field_id])
        self.assertIn('OrganizationCustomField', org_custom_field_query)

    # def test_organization_custom_field_delete_by_id(self):
    #     org_custom_field_delete = self.api.organization_custom_field_delete_by_id([org_custom_field_id])
    #     self.assertIn('boolean', org_custom_field_delete)

    def test_organization_custom_field_query_by_organizationid(self):
        pass

    def test_organization_custom_field_query_by_organizationid_length(self):
        pass

    def test_organization_custom_field_query_by_organizationid_name(self):
        pass

    def test_organization_custom_field_query_by_organizationid_name_length(self):
        pass

    def test_organization_custom_field_query_by_organizationid_type(self):
        pass

    def test_organization_custom_field_query_by_organizationid_type_length(self):
        pass

    def test_organization_custom_field_update(self):
        pass

    def test_organization_event_type_query_by_id(self):
        pass

    def test_organization_event_type_query_by_organizationid(self):
        pass

    def test_organization_event_type_query_by_organizationid_length(self):
        pass

    def test_organization_query_by_id(self):
        pass

    def test_organization_query_children(self):
        pass

    def test_organization_query_children_length(self):
        pass

    def test_organization_query_root(self):
        organization = self.api.organization_query_root()

        self.assertIn('EventTypes', organization)


    def test_role_query_by_id(self):
        pass

    # ===========================================================================
    # End Organization Methods
    # ===========================================================================


if __name__ == '__main__':
    unittest.main()
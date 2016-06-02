#!/usr/bin/env python

# Imports
import suds
import ConfigParser

CONF = ConfigParser.ConfigParser()
try:
    CONF.read("soap.props")
except IOError as e:
    print 'File %s not found!' % e

# WSDL Url
url = 'http://dev4web.iceng.nuancedev.local/WebService/EPAPI_1.3/wsdl.wsdl'
# url = 'https://ws.envoyprofiles.com/WebService/EPAPI_1.0/wsdl.wsdl'


class Service(object):
    def __init__(self):
        """
        Creates header information required for any SOAP request.
        """
        self.client = suds.client.Client(url)
        header = self.client.factory.create('AuthHeader')
        header.Domain = CONF.get("Auth Header", "domain")
        header.UserId = CONF.get("Auth Header", "userid")
        header.UserPassword = CONF.get("Auth Header", "userpassword")
        header.OemId = CONF.get("Auth Header", "oemid")
        header.OemPassword = CONF.get("Auth Header", "oempassword")
        self.client.set_options(soapheaders=header)
        self.orgid = self.client.service.OrganizationQueryRoot()[0]


def team_entry_create_selection_criteria(service):
    '''
    Creates a simple Selection Criteria Team Entry for a given TeamId
    Location(CustomField) = String('Boston')
    '''
    # kwhudkuqb
    # Create Team Objects
    team_entry = service.client.factory.create('TeamEntry')
    array_team_entry = service.client.factory.create('ArrayOfTeamEntry')

    # Create Selection Criteria Objects
    team_entry_selection_criteria = service.client.factory.create('TeamEntrySelectionCriteria')
    selection_criteria = service.client.factory.create('SelectionCriteria')
    selection_criteria_relationship = service.client.factory.create('SelectionCriteriaRelationship')
    selection_criteria_LHSvalue = service.client.factory.create('SelectionCriteriaValue')
    selection_criteria_RHSvalue = service.client.factory.create('SelectionCriteriaValue')
    selection_criteria_LHSvalue_custom_field = service.client.factory.create('SelectionCriteriaValueCustomField')
    selection_criteria_RHSvalue_string = service.client.factory.create('SelectionCriteriaValueString')

    # Specify the Organization Custom Field ID to use and the ValueString
    selection_criteria_LHSvalue_custom_field.ValueOrganizationCustomFieldId = 'kitn3ku8k'
    selection_criteria_RHSvalue_string.ValueString = 'Boston'
    selection_criteria_LHSvalue.SelectionCriteriaValueCustomField = selection_criteria_LHSvalue_custom_field
    selection_criteria_RHSvalue.SelectionCriteriaValueString = selection_criteria_RHSvalue_string

    # Set the relationship type. Type is 'Equal'
    # This reads as Location = 'Boston'
    selection_criteria_relationship.Type = 'Equal'
    selection_criteria_relationship.LHSSelectionCriteriaValue = selection_criteria_LHSvalue
    selection_criteria_relationship.RHSSelectionCriteriaValue = selection_criteria_RHSvalue

    # The selection criteria name is 'JPMC_ONE' and the TeamId where it will be created is specified.
    # 'kpdwhk4mb' is a Team named 'JPMC'
    selection_criteria.Name = 'JPMC_ONE'
    selection_criteria.SelectionCriteriaRelationship = selection_criteria_relationship
    team_entry_selection_criteria.Status = 'Active'
    team_entry_selection_criteria.Order = 0
    team_entry_selection_criteria.TeamId = 'kpdwhk4mb'
    team_entry_selection_criteria.SelectionCriteria = selection_criteria
    team_entry.TeamEntrySelectionCriteria = team_entry_selection_criteria

    # Append the Team Entry to the Team Entry Array
    array_team_entry.TeamEntry.append(team_entry)

    # Send the request
    print service.client.service.TeamEntryCreate(array_team_entry)


def main():
    service = Service()
    team_entry_create_selection_criteria(service)


if __name__ == '__main__':
    main()

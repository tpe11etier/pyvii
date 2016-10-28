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
url = 'http://profiles.beta.vrli.com/WebService/EPAPI_1.3/wsdl.wsdl'


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


def addMemberToTeam(service):
    # TeamId = kwhudkuqb - DupeTeamTest
    # MemberId = kk5s3kx5h - hsimpson
    team = service.client.factory.create('TeamEntryMember')
    teamentry = service.client.factory.create('TeamEntry')
    teamentries = service.client.factory.create('ArrayOfTeamEntry')
    team.Status = 'Active'
    team.Order = 1
    team.TeamId = 'kwhudkuqb'
    team.MemberId = 'kk5s3kx5h'
    teamentry.TeamEntryMember = team
    teamentries.TeamEntry.append(teamentry)
    print teamentry
    print teamentries
    try:
        print service.client.service.TeamEntryCreate(teamentries)
    except suds.WebFault as e:
        print e.fault.details


def main():
    service = Service()
    addMemberToTeam(service)


if __name__ == '__main__':
    main()

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
# url = 'http://dev4web.iceng.nuancedev.local/WebService/EPAPI_1.3/wsdl.wsdl'
url = 'http://profiles.beta.vrli.com/WebService/EPAPI_1.3/wsdl.wsdl'
# url = 'https://developer4.envoyww.com/WebService/EPAPI_1.0/wsdl.wsdl'
# Test commit


class Service(object):
    def __init__(self):
        """
        Creates header information required for any SOAP request.
        """
        self.client = suds.client.Client(url)
        header = self.client.factory.create('AuthHeader')
        header.Domain = CONF.get("Auth Header", "domain")
        # header.UserId = CONF.get("Auth Header", "userid")
        header.UserPassword = CONF.get("Auth Header", "userpassword")
        header.OemId = CONF.get("Auth Header", "oemid")
        header.OemPassword = CONF.get("Auth Header", "oempassword")
        self.client.set_options(soapheaders=header)
        self.orgid = self.client.service.OrganizationQueryRoot()[0]


def createTeam(service):
    team = service.client.factory.create('Team')
    teams = service.client.factory.create('ArrayOfTeam')
    team.Name = 'DupeTeamTest'
    team.OrganizationId = service.orgid
    team.Type = 'Custom'
    team.SourceIdentifier = 'MySourceId'
    teams.Team.append(team)
    try:
        print service.client.service.TeamCreate(teams)
    except suds.WebFault as e:
        print e.fault.detail

def main():
    service = Service()
    createTeam(service)


if __name__ == '__main__':
    main()

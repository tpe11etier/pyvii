#!/usr/bin/env python

import pyvii
import pprint
pp = pprint.PrettyPrinter(indent=4)

def main():
    authheader = {
        'url': 'http://developer4.envoyww.com/WebService/EPAPI_1.0/wsdl.wsdl',
        'Domain': 'TPELLETIER',
        'userid': 'psadmin',

        'userpassword': 'W!sc0nsin',
        'oemid': 'TPELLETIERoem',
        'oempassword': 'TPELLETIER$1oem'
    }

    tpelletier = {'timezoneid': '123', 'Company': 'ACME Inc.', 'Username': 'thpelletier', 'LastName':
                  'Pelletier', 'FirstName': 'Tony', 'Password': 'W!sc0nsin', 'AccountEnabled': 'True'}
    bjones = {'Username': 'bhjones', 'LastName': 'Jones', 'FirstName':
              'Bob', 'Password': 'W!sc0nsin', 'AccountEnabled': 'True'}

    escalation_object = {'name': 'pyvii',
                         'OrganizationId': '10201',
                         'escalationactions': [{'escalationtypeid': '1736',
                                                'escalationcontacts':[{'AllowRedundantContacts': False,
                                                                       'escalationtypeid': '1736',
                                                                       'escalationdevices': [{'escalationtypeid': '1736',
                                                                                              'order': 1
                                                                                            }]}]},
                                               {'escalationtypeid': '1736',
                                                'escalationcontacts':[{'AllowRedundantContacts': False,
                                                                       'escalationtypeid': '1736',
                                                                       'escalationdevices': [{'escalationtypeid': '1736',
                                                                                              'order': 2
                                                                                            }]}]}

                                                                                            ]

                        }

    escalation_list = []
    escalation_list.append(escalation_object)

    # print escalation_object

    member_list = []
    member_list.append(tpelletier)
    member_list.append(bjones)
    api = pyvii.Api(authheader)
    # result = api.member_create(member_list)

    # org = api.organization_query_root()  #kftphkk4k
    # escalations = api.escalation_query_by_organizationid(['10201'])
    result = api.organization_custom_field_query_by_organizationid_name(['10201'], 'boolean')



    print result




if __name__ == '__main__':
    main()

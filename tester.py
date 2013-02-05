#!/usr/bin/env python

import pyvii


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

    listofmembers = []
    listofmembers.append(tpelletier)
    listofmembers.append(bjones)
    api = pyvii.Api(authheader)
    # result = api.member_create(listofmembers)

    # org = api.organization_query_root()
    org = api.organization_custom_field_query_by_organizationid_name(['10201'], 'boolean', 0, 3)

    print org



if __name__ == '__main__':
    main()

#!/usr/bin/env python3

# Imports

import pyvii
import suds
import pprint
import sys
pp = pprint.PrettyPrinter(indent=4)


authheader = {
    'url': 'http://profiles.beta.vrli.com/WebService/EPAPI_1.3/wsdl.wsdl',
    'Domain': 'TPELLETIER',
    'userid': 'psadmin',
    'userpassword': 'N3Br@ska!',
    'oemid': 'TPELLETIERoem',
    'oempassword': 'TPELLETIER$1oem'
}


def main():
    api = pyvii.Api(authheader)

    try:
        print(api.organization_query_root())
    except suds.WebFault as e:
        print(e.fault.detail)

if __name__ == '__main__':
    print(sys.version)
    main()



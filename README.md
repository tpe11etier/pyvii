# PyVii - Wrapper to Varolii SOAP API

## About

Pythonic Wrapper to Varlii SOAP API - http://developer4.envoyww.com/WebService/EPAPI_1.0/intro.htm
This is *not* supported or maintained by Varolii at all.  It's simply something I wrote to make my job easier and it's *constantly* changing.
A large portion of the available methods in the SOAP API are not in this simply because I've only added what I feel are the most commonly used ones.
As time goes on, I will continue to add to the list.

##Installation
Note - PyVii requires suds.  [SUDS](https://fedorahosted.org/suds/)

    pip install suds
    git clone https://github.com/tpe11etier/pyvii.git

## Simple Usage
    In [1]: import pyvii

    In [2]: authheader = {
                          'url': 'http://developer4.envoyww.com/WebService/EPAPI_1.0/wsdl.wsdl',
                          'Domain': 'DomainName',
                          'userid': 'UserId',
                          'userpassword': 'UserPassword',
                          'oemid': 'OEMId',
                          'oempassword': 'OEMPassword'
                         }

    In [3]: api = pyvii.Api(authheader)

    In [4]: api.organization_query_by_id(['10201'])

    Out[4]:
    (ArrayOfOrganization){
       Organization[] =
          (Organization){
             OrganizationId = "kftphkk4k"
             Name = "TPELLETIER"
             ParentOrganizationId = None
             EventTypes =
                (ArrayOfstring){
                   string[] =
                      "k2ts3kkbk",
                      "k25ebkkbk",
                      "k25z5kkbk",
                      "k2t75kkbk",
                      "k2tgbkkbk",
                      "km5tbkkbk",
                      "kibk3kk5k",
                }
             Roles =
                (ArrayOfstring){
                   string[] =
                      "kk3bkkkkk",
                      "kibq5kkbk",
                      "ki56bkkbk",
                      "ki5r5kkbk",
                      "ki583kkbk",
                      "k8t1tkkbk",
                }
          },
     }


##More Detail

If you've worked with the Varolii SOAP API, you're aware that everything is an Array of an object.
To create a Member you create a Member object, append it to an ArrayOfMember then call MemberCreate and pass in the Array.
I've stayed true to that...Objects are Dicts and Arrays are Lists.  Sticking with Members, here's an example of creating a Member.

    In [1]: import pyvii

    In [2]: authheader = {
                          'url': 'http://developer4.envoyww.com/WebService/EPAPI_1.0/wsdl.wsdl',
                          'Domain': 'DomainName',
                          'userid': 'UserId',
                          'userpassword': 'UserPassword',
                          'oemid': 'OEMId',
                          'oempassword': 'OEMPassword'
                         }

    In [3]: api = pyvii.Api(authheader)

    In [4]: members = [{'timezoneid': '123',
                        'Company': 'API Example',
                        'Username': 'apiexample',
                        'Password': 'Api$1Example',
                        'LastName': 'Example',
                        'FirstName': 'Api',
                        'AccountEnabled': 'True',
                        'ContactMethods': [
                                           {'ContactMethodEmail': {'Qualifier': 'office', 'EmailAddress': 'api.example@office.com'}},
                                           {'ContactMethodPhone': {'Qualifier': 'office', 'PhoneNum': '6174282113'}}
                                          ]
                       }
                      ]

    In [5]: api.member_create(members)

    Out[5]:
            (ArrayOfResponseEntry){
               ResponseEntry[] =
                  (ResponseEntry){
                     Id = "kqd5bktgi"
                     Warnings = ""
                  },
             }


## That's all folks!

If anyone finds this and decides to use it or has questions, I'll gladly update it and add more documentation.

** Note ** only python 2.7 has been tested.






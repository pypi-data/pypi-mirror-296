# coding: utf-8

"""
    Notehub API

    The OpenAPI definition for the Notehub.io API. 

    The version of the OpenAPI document: 1.1.0
    Contact: engineering@blues.io
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from notehub_py.models.twilio import Twilio

class TestTwilio(unittest.TestCase):
    """Twilio unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> Twilio:
        """Test Twilio
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `Twilio`
        """
        model = Twilio()
        if include_optional:
            return Twilio(
                fleets = [
                    ''
                    ],
                filter = notehub_py.models.http_filter.http_filter(
                    type = 'all', 
                    system_notefiles = True, 
                    files = [
                        ''
                        ], ),
                timeout = 56,
                account_sid = '',
                auth_token = '',
                to = '',
                var_from = '',
                message = '',
                throttle_ms = 56
            )
        else:
            return Twilio(
        )
        """

    def testTwilio(self):
        """Test Twilio"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()

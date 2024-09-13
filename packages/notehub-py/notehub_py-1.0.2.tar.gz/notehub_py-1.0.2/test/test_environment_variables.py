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

from notehub_py.models.environment_variables import EnvironmentVariables

class TestEnvironmentVariables(unittest.TestCase):
    """EnvironmentVariables unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> EnvironmentVariables:
        """Test EnvironmentVariables
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `EnvironmentVariables`
        """
        model = EnvironmentVariables()
        if include_optional:
            return EnvironmentVariables(
                environment_variables = {
                    'key' : ''
                    }
            )
        else:
            return EnvironmentVariables(
                environment_variables = {
                    'key' : ''
                    },
        )
        """

    def testEnvironmentVariables(self):
        """Test EnvironmentVariables"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()

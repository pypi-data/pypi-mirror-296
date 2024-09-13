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

from notehub_py.models.http_filter import HttpFilter

class TestHttpFilter(unittest.TestCase):
    """HttpFilter unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> HttpFilter:
        """Test HttpFilter
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `HttpFilter`
        """
        model = HttpFilter()
        if include_optional:
            return HttpFilter(
                type = 'all',
                system_notefiles = True,
                files = [
                    ''
                    ]
            )
        else:
            return HttpFilter(
        )
        """

    def testHttpFilter(self):
        """Test HttpFilter"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()

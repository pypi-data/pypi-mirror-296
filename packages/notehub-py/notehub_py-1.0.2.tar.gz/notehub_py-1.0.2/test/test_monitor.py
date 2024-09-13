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

from notehub_py.models.monitor import Monitor

class TestMonitor(unittest.TestCase):
    """Monitor unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> Monitor:
        """Test Monitor
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `Monitor`
        """
        model = Monitor()
        if include_optional:
            return Monitor(
                uid = '',
                name = '',
                description = '',
                source_type = 'event',
                disabled = True,
                alert = True,
                notefile_filter = [
                    ''
                    ],
                fleet_filter = [
                    ''
                    ],
                source_selector = 'body.temperature',
                condition_type = 'greater_than',
                threshold = 56,
                alert_routes = [
                    null
                    ],
                last_routed_at = '',
                silenced = True,
                routing_cooldown_period = '10m or 5h30m40s',
                aggregate_function = 'none',
                aggregate_window = '10m or 5h30m40s',
                per_device = True
            )
        else:
            return Monitor(
        )
        """

    def testMonitor(self):
        """Test Monitor"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()

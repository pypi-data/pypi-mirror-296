# coding: utf-8

"""
    Skyfire API

    The Skyfire API is designed to allow agents to interact with the Skyfire platform to enable autonomous payments.

    The version of the OpenAPI document: 1.0.0
    Contact: support@skyfire.xyz
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from skyfire_sdk.models.cash_flow_statement import CashFlowStatement

class TestCashFlowStatement(unittest.TestCase):
    """CashFlowStatement unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> CashFlowStatement:
        """Test CashFlowStatement
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `CashFlowStatement`
        """
        model = CashFlowStatement()
        if include_optional:
            return CashFlowStatement(
                ticker = 'AAPL',
                calendar_date = 'Sun Dec 24 19:00:00 EST 2023',
                report_period = 'Sun Dec 24 19:00:00 EST 2023',
                period = 'quarterly',
                net_cash_flow_from_operations = 123,
                depreciation_and_amortization = 123,
                share_based_compensation = 123,
                net_cash_flow_from_investing = 123,
                capital_expenditure = 123,
                business_acquisitions_and_disposals = 123,
                investment_acquisitions_and_disposals = 123,
                net_cash_flow_from_financing = 123,
                issuance_or_repayment_of_debt_securities = 123,
                issuance_or_purchase_of_equity_shares = 123,
                dividends_and_other_cash_distributions = 123,
                change_in_cash_and_equivalents = 123,
                effect_of_exchange_rate_changes = 123
            )
        else:
            return CashFlowStatement(
        )
        """

    def testCashFlowStatement(self):
        """Test CashFlowStatement"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()

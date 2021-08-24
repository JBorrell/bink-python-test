import unittest
import datetime

from analyse_data import (
    sort_by_current_rent,
    filter_by_lease_length,
    is_within_range,
    get_lease_start_date_within_range,
    readable_date,
    run_data_extraction
)

class TestDataAnalysisMethods(unittest.TestCase):
    def setUp(self):
        self.tenant_data = [
            {
                'Property Name': 'Test property name 1',
                'Unit Name': 'Test unit name 1',
                'Tenant Name': 'John Doe',
                'Lease Start Date': '26 Jul 2007',
                'Lease End Date': '25 Jul 2032',
                'Lease Years': '25',
                'Current Rent': '9050.34'
            },
            {
                'Property Name': 'Test property name 2',
                'Unit Name': 'Test unit name 2',
                'Tenant Name': 'Sam Johnson',
                'Lease Start Date': '14 May 2010',
                'Lease End Date': '13 May 2035',
                'Lease Years': '25',
                'Current Rent': '3600.50'
            },
            {
                'Property Name': 'Test property name 3',
                'Unit Name': 'Test unit name 3',
                'Tenant Name': 'Jim Smith',
                'Lease Start Date': '20 Oct 2018',
                'Lease End Date': '19 Oct 2028',
                'Lease Years': '10',
                'Current Rent': '15300.00'
            },
        ]

    def test_sort_by_current_rent(self):
        tenant_list = sort_by_current_rent(self.tenant_data)
        self.assertEqual(len(tenant_list), 3)
        self.assertEqual(tenant_list[0]['Property Name'], 'Test property name 3')
        self.assertEqual(tenant_list[0]['Current Rent'], '15300.00')
        self.assertEqual(tenant_list[2]['Property Name'], 'Test property name 2')
        self.assertEqual(tenant_list[2]['Current Rent'], '3600.50')

    def test_sort_by_current_rent_limit(self):
        tenant_list = sort_by_current_rent(self.tenant_data, limit=1)
        self.assertEqual(len(tenant_list), 1)
        self.assertEqual(tenant_list[0]['Property Name'], 'Test property name 3')
        tenant_list2 = sort_by_current_rent(self.tenant_data, limit=2)
        self.assertEqual(len(tenant_list2), 2)
        self.assertEqual(tenant_list2[1]['Property Name'], 'Test property name 1')

    def test_filter_by_lease_length(self):
        tenant_list = filter_by_lease_length(self.tenant_data)
        self.assertEqual(len(tenant_list), 2)
        self.assertEqual(tenant_list[0]['Property Name'], 'Test property name 1')
        self.assertEqual(tenant_list[0]['Lease Years'], '25')
        tenant_list2 = filter_by_lease_length(self.tenant_data, years=10)
        self.assertEqual(len(tenant_list2), 1)
        self.assertEqual(tenant_list2[0]['Property Name'], 'Test property name 3')
        self.assertEqual(tenant_list2[0]['Lease Years'], '10')

    def test_date_within_range(self):
        date = '10 Jun 2005'
        start = datetime.datetime(1999, 8, 15)
        end = datetime.datetime(2006, 3, 10)
        self.assertTrue(is_within_range(date, start, end))
        end = datetime.datetime(2004, 3, 10)
        self.assertFalse(is_within_range(date, start, end))

    def test_filter_by_lease_start(self):
        tenant_list = get_lease_start_date_within_range(
            self.tenant_data,
            datetime.datetime(1999, 6, 1),
            datetime.datetime(2007, 8, 31),
        )
        self.assertEqual(len(tenant_list), 1)
        self.assertEqual(tenant_list[0]['Property Name'], 'Test property name 1')

    def test_readable_date_format(self):
        date = '10 Jun 2005'
        formatted_date = readable_date(date)
        self.assertEqual(formatted_date, '10/06/2005')

    def test_data_extraction(self):
        tenant_data = run_data_extraction()
        self.assertEqual(len(tenant_data), 42)
        self.assertIsInstance(tenant_data, list)
        expected_keys = [
            'Tenant Name',
            'Lease Start Date',
            'Lease End Date',
            'Current Rent',
            'Unit Name',
            'Property Name',
            'Lease Years'
        ]
        for key in expected_keys:
            self.assertIn(key, tenant_data[0].keys())


if __name__ == '__main__':
    unittest.main()

import csv
import datetime

def sort_by_current_rent(tenant_data, limit=None):
    return sorted(tenant_data, key=lambda k: float(k['Current Rent']), reverse=True)[:limit]

def filter_by_lease_length(tenant_data, years=25):
    return [tenant for tenant in tenant_data if float(tenant['Lease Years']) == years]

def is_within_range(date, start_date, end_date):
    datetime_date = datetime.datetime.strptime(date, '%d %b %Y')
    return datetime_date > start_date and datetime_date < end_date

def get_lease_start_date_within_range(tenant_data, start_date, end_date):
    return [tenant for tenant in tenant_data if is_within_range(
        tenant['Lease Start Date'],
        start_date,
        end_date,
        )]

def readable_date(date):
    datetime_date = datetime.datetime.strptime(date, '%d %b %Y')
    return datetime_date.strftime('%d/%m/%Y')

def run_data_extraction():
    with open('./test_dataset.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        headings = []
        tenants = []
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                for item in row:
                    headings.append(item)
            else:
                tenant_data = dict(zip(headings, row))
                tenants.append(tenant_data)
                line_count += 1

        return tenants

if __name__ == '__main__':
    tenant_data = run_data_extraction()
    print("What data do you need?")
    print("Options are: 1a, 1b, 2a, 2b, 4a")
    print("Type 'exit' to exit")

    while 1:
        user_input = input('>>')
        if user_input == 'exit':
            break

        if user_input == '1a':
            tenants_sorted_by_rent = sort_by_current_rent(tenant_data)
            for tenant in tenants_sorted_by_rent:
                print(tenant)
                print(' ')
        elif user_input == '1b':
            # If needed can obtain any amount of items from list
            tenants_sorted_by_rent = sort_by_current_rent(tenant_data, limit=5)
            for tenant in tenants_sorted_by_rent:
                print(tenant)
                print(' ')
        elif user_input == '2a':
            # If needed can filter 'Lease Years' of any value
            lease_years_25 = filter_by_lease_length(tenant_data)
            for tenant in tenants_sorted_by_rent:
                print(tenant)
                print(' ')
        elif user_input == '2b':
            lease_years_25 = filter_by_lease_length(tenant_data)
            total_rent = sum(float(tenant['Current Rent']) for tenant in lease_years_25)
            print('Total rent:', total_rent)
        # elif user_input == '3a':
        #     "I'm not sure what 'a count of all masts' means as a spec"
        elif user_input == '4a':
            # If needed can adjust time frame for lease start date range
            lease_start_date = datetime.datetime(1999, 6, 1)
            lease_end_date = datetime.datetime(2007, 8, 31)
            leases_within_range = get_lease_start_date_within_range(
                tenant_data,
                lease_start_date,
                lease_end_date
            )
            for tenant in leases_within_range:
                print(
                    tenant['Unit Name'],
                    tenant['Tenant Name'],
                    '-- Start:',
                    readable_date(tenant['Lease Start Date']),
                    'End:',
                    readable_date(tenant['Lease End Date'])
                )
        print("What data do you need?")
        print("Options are: 1a, 1b, 2a, 2b, 4a")
        print("Type 'exit' to exit")

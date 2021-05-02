#!/usr/bin/env python3
import boto3

# Organizations currently uses the us-east-1 region for all API and CLI calls.
endpoint_url = "https://organizations.us-east-1.amazonaws.com"
endpoint_short = "us-east-1"

org_client = boto3.client('organizations')

# Create a paginator for the organizations.list_accounts method.
account_paginator = org_client.get_paginator('list_accounts')

# Paginate list_accounts operation, returning results in a PageIterator.
# Note: This is where required information for the list_accounts operation is needed.
# The list_accounts() action has several parameters, we're using the `Max Results` one here
# to limit the amount of return items for the page.
account_page_iterator = account_paginator.paginate(MaxResults=10)

# Print out specifics of the account
for page in account_page_iterator:
    for item in page['Accounts']:
        print("Account ID:" + item['Id'])
        print("Account Email:" + item['Email'] + '\n')

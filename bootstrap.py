#!/usr/bin/env python3
# Terraform bootstrapping
# Creates proper S3 bucket for remote storage and locking tables in DynamoDB

# TODO: Tagging

import boto3
import uuid
import argparse
import time

# global clients for AWS
g_s3_client = boto3.client("s3")
g_dynamo_client = boto3.client("dynamodb")

# global argparser
# takes one required argument, region
# additionally takes a flag that will toggle tagging on resources created by this script. (default false)
parser = argparse.ArgumentParser(description='Bootstrap Terraform Remote Backends')
parser.add_argument("region")
parser.add_argument("-t", "--tag", help="Tags bootstrapped resources as being managed by Bootstrap", action="store_false")
args = parser.parse_args()

def create_bucket(region):
    response = g_s3_client.create_bucket(
        ACL='private',
        Bucket='bootstrap-{}'.format(uuid.uuid4()),
        CreateBucketConfiguration={
            'LocationConstraint': '{}'.format(region)
        }
    )
    return response

def create_table(region):
    print("Creating DynamoDB Lock Table...")
    response = g_dynamo_client.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'LockID',
                'AttributeType': 'S'
            },
        ],
        TableName='terraform',
        KeySchema=[
            { 
                'AttributeName': 'LockID',
                'KeyType': 'HASH'
            },
        ],
        BillingMode='PAY_PER_REQUEST'
    )
    check = g_dynamo_client.describe_table(TableName='terraform')
    '''
    CreateTable is an asynchronous operation. Upon receiving a CreateTable request, DynamoDB immediately returns a response with a TableStatus of CREATING . 
    After the table is created, DynamoDB sets the TableStatus to ACTIVE . You can perform read and write operations only on an ACTIVE table.
    '''
    # Check for ACTIVE status table after creation.
    while True:
        print("Polling for table creation status to go to Active...\n")
        check = g_dynamo_client.describe_table(TableName='terraform')
        if check['Table']['TableStatus'] == 'ACTIVE':
            break
        time.sleep(3) 
    print('Table created!\n')
    return response


# Logic here:
# 1. Create S3 Bucket
# 2. in S3 response, grab bucket name (since it's randomized)
# 3. if -t/--tag is passed into script, tag S3 bucket with "Managed:Bootstrap"

table = create_table(args.region)
bucket = create_bucket(args.region)
print("S3 Bucket: " + bucket["Location"])
print("\nDynamoDB Table: " + table['TableDescription']['TableName'])

#!/usr/bin/env python3
# Terraform bootstrapping
# Creates proper S3 bucket for remote storage and locking tables in DynamoDB

import boto3
import uuid
import argparse

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

# Logic here:
# 1. Create S3 Bucket
# 2. in S3 response, grab bucket name (since it's randomized)
# 3. if -t/--tag is passed into script, tag S3 bucket with "Managed:Bootstrap"
#def tag_bucket(tags):

bucket = create_bucket(args.region)

print("S3 Bucket: " + bucket["Location"])

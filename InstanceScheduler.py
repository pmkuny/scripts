#!/usr/bin/env python3

import json
import boto3
import boto3.session

'''
Session: Creates a new boto3 session based on the session configuration
requirements.

elligible_instances_tag: Dictionary for defining what tag this Lambda can
operate on. NOTE that by default and IAM policy, this is currently limited to
"scheduler": "true"
'''

session = boto3.session.Session(region_name='us-west-2')
eligible_instances_tag = {"scheduler": "true"}

'''
We need to retrieve a list of the instances with this specific tag applied, by ID.
CLI: aws ec2 describe-instances --filters Name=tag:scheduler,Values='true' --query Reservations[*].Instances[*].InstanceId --output text
'''

def get_instance_ids():
    ec2_client = session.client("ec2")
    paginator = ec2_client.get_paginator('describe_instances')
    iterator = paginator.paginate(
        Filters=[
            {
                'Name': 'tag:scheduler',
                'Values': [
                    'true',
                ]
            }
         ],
            MaxResults=10
    )
    for page in iterator:
        for item in page['Reservations']:
            for Instance in item['Instances']:
                print(Instance['InstanceId'])

get_instance_ids()
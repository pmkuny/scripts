#!/usr/bin/env python3

import json
import boto3
import boto3.session


# We use CloudWatch Event Bridge to control the times that fire off a stop_instances() and start_instances()


# Session: Creates a new boto3 session based on the session configuration
# requirements.

# elligible_instances_tag: Dictionary for defining what tag this Lambda can
# operate on. NOTE that by default and IAM policy, this is currently limited to
# "scheduler": "true"


session = boto3.session.Session(region_name='us-west-2')
eligible_instances_tag = {"scheduler": "true"}

# We need to retrieve a list of the instances with this specific tag applied, by ID.
# CLI: aws ec2 describe-instances --filters Name=tag:scheduler,Values='true' --query Reservations[*].Instances[*].InstanceId --output text


def get_instance_ids():
    instance_ids = []
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
                instance_ids.append(Instance['InstanceId'])
                print(Instance['InstanceId'] + " added to list")
    
    return instance_ids

def stop_instances(instance_ids):
    for instance in instance_ids:
        ec2 = session.client("ec2")
        response = ec2.stop_instances(InstanceIds=[instance])
        print(instance + " stopping response: " + response['StoppingInstances']['CurrentState']['Name'] )
    




instance_ids = get_instance_ids()
stop_instances(instance_ids)

#!/usr/bin/env python3

import boto3

# define service endpoints, they should be defined as constants 
REGION = "us-west-2"
EC2_ENDPOINT_URL = f"ec2.{REGION}.amazonaws.com"

# Define our boto3 EC2 Client for low-level operations
client = boto3.client("ec2")

# Define our EC2 Resource for interacting with instances
resource = boto3.resource("ec2")

# Filter on key. They will return only instances that have this tag key applied, regardless of its value
def get_instances():
    has_tags_dict = client.describe_instances(
        Filters=[
            {
                'Name': 'tag-key',
                'Values': ['mykey']
            }
        ]
    )

    # Sort through our response, parsing out the Instance IDs
    for reservations in has_tags_dict['Reservations']:
        for instance in reservations['Instances']:
            print(instance['InstanceId'])

    return 

get_instances()




import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import json
from datetime import datetime
from datetime import datetime, timedelta

from fastapi import FastAPI
from fastapi.routing import APIRoute
from api import *
from models import *
from fastapi import *

def get_aws_details(profile_name, region):
    try:
        # Create a session using the specified profile
        session = boto3.Session(profile_name=profile_name)

        # Create an EC2 client using the specified region
        ec2_client = session.client('ec2', region_name=region)

        # Example: Get information about EC2 instances
        response = ec2_client.describe_instances()

        # Convert response to JSON format
        result = json.dumps(response, default=APIRoute.convert_datetime, indent=2)

        # Process and return the response
        return result

    except NoCredentialsError:
        return "Credentials not available or not valid. Please configure AWS credentials."
    except PartialCredentialsError:
        return "Incomplete credentials provided. Please provide valid AWS credentials."
    except Exception as e:
        return f"An error occurred: {str(e)}"



def create_ami(profile_name, region, instance_id):
    try:
        # Create a session using the specified profile
        session = boto3.Session(profile_name=profile_name)

        # Create an EC2 client using the specified region
        ec2_client = session.client('ec2', region_name=region)

        # Create an AMI from the specified EC2 instance
        response = ec2_client.create_image(
            InstanceId=instance_id,
            Name=f"AMI for {instance_id}",
            Description=f"AMI created for EC2 instance {instance_id}",
            NoReboot=True  # Set to True if you want to stop the instance during AMI creation
        )

        # Extract the AMI ID from the response
        ami_id = response.get('ImageId', '')

        return ami_id

    except NoCredentialsError:
        raise ValueError("Credentials not available or not valid. Please configure AWS credentials.")
    except PartialCredentialsError:
        raise ValueError("Incomplete credentials provided. Please provide valid AWS credentials.")
    except Exception as e:
        raise ValueError(f"An error occurred: {str(e)}")
    


def deregister_ami(profile_name, region, ami_id):
    try:
        # Create a session using the specified profile
        session = boto3.Session(profile_name=profile_name)

        # Create an EC2 client using the specified region
        ec2_client = session.client('ec2', region_name=region)

        # Deregister the specified AMI
        ec2_client.deregister_image(ImageId=ami_id)

    except NoCredentialsError:
        raise ValueError("Credentials not available or not valid. Please configure AWS credentials.")
    except PartialCredentialsError:
        raise ValueError("Incomplete credentials provided. Please provide valid AWS credentials.")
    except Exception as e:
        raise ValueError(f"An error occurred: {str(e)}")



def get_amis(profile_name, region):
    try:
        # Create a session using the specified profile
        session = boto3.Session(profile_name=profile_name)

        # Create an EC2 client using the specified region
        ec2_client = session.client('ec2', region_name=region)

        # Get a list of AMIs in the specified region
        response = ec2_client.describe_images(Owners=['self'])
        amis = response.get('Images', [])

        # Extract relevant information from AMIs
        ami_list = [
            {
                'ami_id': ami['ImageId'],
                'name': ami.get('Name', 'N/A'),
                'creation_date': ami['CreationDate'],
                'description': ami.get('Description', 'N/A'),
            }
            for ami in amis
        ]

        return ami_list

    except NoCredentialsError:
        raise ValueError("Credentials not available or not valid. Please configure AWS credentials.")
    except PartialCredentialsError:
        raise ValueError("Incomplete credentials provided. Please provide valid AWS credentials.")
    except Exception as e:
        raise ValueError(f"An error occurred: {str(e)}")


    
def get_s3_details(profile_name, bucket_name):
    try:
        # Create a session using the specified profile
        session = boto3.Session(profile_name=profile_name)

        # Create an S3 client
        s3_client = session.client('s3')

        # Example: Get information about S3 bucket
        response = s3_client.list_objects(Bucket=bucket_name)
        
        # Convert response to JSON format
        result = json.dumps(response, default=api.convert_datetime, indent=2)

        # Process and return the response
        return result

    except NoCredentialsError:
        return "Credentials not available or not valid. Please configure AWS credentials."
    except PartialCredentialsError:
        return "Incomplete credentials provided. Please provide valid AWS credentials."
    except Exception as e:
        return f"An error occurred: {str(e)}"
    



def get_s3_buckets(profile_name):
    try:
        # Create a session using the specified profile
        session = boto3.Session(profile_name=profile_name)

        # Create an S3 client
        s3_client = session.client('s3')

        # List all S3 buckets
        response = s3_client.list_buckets()

        # Extract bucket names from the response
        bucket_names = [bucket['Name'] for bucket in response.get('Buckets', [])]

        return bucket_names

    except NoCredentialsError:
        return "Credentials not available or not valid. Please configure AWS credentials."
    except PartialCredentialsError:
        return "Incomplete credentials provided. Please provide valid AWS credentials."
    except Exception as e:
        return f"An error occurred: {str(e)}"
    

    
def get_ecs_details(profile_name, region):
    try:
        # Create a session using the specified profile
        session = boto3.Session(profile_name=profile_name)

        # Create an ECS client using the specified region
        ecs_client = session.client('ecs', region_name=region)

        # List all ECS clusters
        response = ecs_client.list_clusters()

        # Extract cluster details from the response
        clusters = []

        for cluster_arn in response.get('clusterArns', []):
            cluster_details = ecs_client.describe_clusters(clusters=[cluster_arn])
            clusters.append(cluster_details['clusters'][0])

        return clusters

    except NoCredentialsError:
        return "Credentials not available or not valid. Please configure AWS credentials."
    except PartialCredentialsError:
        return "Incomplete credentials provided. Please provide valid AWS credentials."
    except Exception as e:
        return f"An error occurred: {str(e)}"



def get_ecs_services(profile_name, region, cluster_name):
    try:
        # Create a session using the specified profile
        session = boto3.Session(profile_name=profile_name)

        # Create an ECS client using the specified region
        ecs_client = session.client('ecs', region_name=region)

        # Example: Get information about ECS services
        response = ecs_client.list_services(cluster=cluster_name)
        service_arns = response.get('serviceArns', [])

        # Retrieve details for each service
        services = []

        for service_arn in service_arns:
            service_details = ecs_client.describe_services(
                cluster=cluster_name,
                services=[service_arn]
            )
            services.append(service_details['services'][0])

        return services

    except NoCredentialsError:
        return "Credentials not available or not valid. Please configure AWS credentials."
    except PartialCredentialsError:
        return "Incomplete credentials provided. Please provide valid AWS credentials."
    except Exception as e:
        return f"An error occurred: {str(e)}"
    


def get_ecs_tasks(profile_name, region, cluster_name, service_name):
    try:
        # Create a session using the specified profile
        session = boto3.Session(profile_name=profile_name)

        # Create an ECS client using the specified region
        ecs_client = session.client('ecs', region_name=region)

        # Example: Get information about ECS tasks for a service
        response = ecs_client.list_tasks(
            cluster=cluster_name,
            serviceName=service_name
        )
        task_arns = response.get('taskArns', [])

        # Retrieve details for each task
        tasks = []

        for task_arn in task_arns:
            task_details = ecs_client.describe_tasks(
                cluster=cluster_name,
                tasks=[task_arn]
            )
            tasks.append(task_details['tasks'][0])

        return tasks

    except NoCredentialsError:
        return "Credentials not available or not valid. Please configure AWS credentials."
    except PartialCredentialsError:
        return "Incomplete credentials provided. Please provide valid AWS credentials."
    except Exception as e:
        return f"An error occurred: {str(e)}"



def get_ecs_cpu_metrics(profile_name, region, cluster_name, service_name, duration_hours):
    try:
        # Create a session using the specified profile
        session = boto3.Session(profile_name=profile_name)

        # Create a CloudWatch client using the specified region
        cloudwatch_client = session.client('cloudwatch', region_name=region)

        # Calculate the start and end time based on the specified duration
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=duration_hours)

        # Fetch CPU utilization metrics for the ECS service
        response = cloudwatch_client.get_metric_data(
            MetricDataQueries=[
                {
                    'Id': 'm1',
                    'MetricStat': {
                        'Metric': {
                            'Namespace': 'AWS/ECS',
                            'MetricName': 'CPUUtilization',
                            'Dimensions': [
                                {
                                    'Name': 'ClusterName',
                                    'Value': cluster_name
                                },
                                {
                                    'Name': 'ServiceName',
                                    'Value': service_name
                                }
                            ]
                        },
                        'Period': 60 * 5,  # 5 minutes interval
                        'Stat': 'Average'
                    },
                    'ReturnData': True
                },
            ],
            StartTime=start_time,
            EndTime=end_time,
        )

        # Extract CPU utilization data from the response
        timestamps = response.get('Timestamps', [])
        cpu_utilization_values = response.get('MetricDataResults', [])[0].get('Values', [])

        # Create a list of CPU utilization metrics with timestamp and value
        cpu_metrics = [
            {'timestamp': timestamp.isoformat(), 'value': value}
            for timestamp, value in zip(timestamps, cpu_utilization_values)
        ]

        return cpu_metrics

    except NoCredentialsError:
        return "Credentials not available or not valid. Please configure AWS credentials."
    except PartialCredentialsError:
        return "Incomplete credentials provided. Please provide valid AWS credentials."
    except Exception as e:
        return f"An error occurred: {str(e)}"



def get_ecs_memory_metrics(profile_name, region, cluster_name, service_name, duration_hours):
    try:
        # Create a session using the specified profile
        session = boto3.Session(profile_name=profile_name)

        # Create a CloudWatch client using the specified region
        cloudwatch_client = session.client('cloudwatch', region_name=region)

        # Calculate the start and end time based on the specified duration
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=duration_hours)

        # Fetch memory utilization metrics for the ECS service
        response = cloudwatch_client.get_metric_data(
            MetricDataQueries=[
                {
                    'Id': 'm1',
                    'MetricStat': {
                        'Metric': {
                            'Namespace': 'AWS/ECS',
                            'MetricName': 'MemoryUtilization',
                            'Dimensions': [
                                {
                                    'Name': 'ClusterName',
                                    'Value': cluster_name
                                },
                                {
                                    'Name': 'ServiceName',
                                    'Value': service_name
                                }
                            ]
                        },
                        'Period': 60 * 5,  # 5 minutes interval
                        'Stat': 'Average'
                    },
                    'ReturnData': True
                },
            ],
            StartTime=start_time,
            EndTime=end_time,
        )

        # Extract memory utilization data from the response
        timestamps = response.get('Timestamps', [])
        memory_utilization_values = response.get('MetricDataResults', [])[0].get('Values', [])

        # Create a list of memory utilization metrics with timestamp and value
        memory_metrics = [
            {'timestamp': timestamp.isoformat(), 'value': value}
            for timestamp, value in zip(timestamps, memory_utilization_values)
        ]

        return memory_metrics

    except NoCredentialsError:
        return "Credentials not available or not valid. Please configure AWS credentials."
    except PartialCredentialsError:
        return "Incomplete credentials provided. Please provide valid AWS credentials."
    except Exception as e:
        return f"An error occurred: {str(e)}"
    


def get_sqs_details(profile_name, region):
    try:
        # Create a session using the specified profile
        session = boto3.Session(profile_name=profile_name)

        # Create an SQS client using the specified region
        sqs_client = session.client('sqs', region_name=region)

        # List all SQS queues
        response = sqs_client.list_queues()

        # Extract queue details from the response
        queues = response.get('QueueUrls', [])

        return queues

    except NoCredentialsError:
        return "Credentials not available or not valid. Please configure AWS credentials."
    except PartialCredentialsError:
        return "Incomplete credentials provided. Please provide valid AWS credentials."
    except Exception as e:
        return f"An error occurred: {str(e)}"
    


def get_rds_details(profile_name, region):
    try:
        # Create a session using the specified profile
        session = boto3.Session(profile_name=profile_name)

        # Create an RDS client using the specified region
        rds_client = session.client('rds', region_name=region)

        # Example: Get information about RDS instances
        response = rds_client.describe_db_instances()
        instances = response.get('DBInstances', [])

        return instances

    except NoCredentialsError:
        return "Credentials not available or not valid. Please configure AWS credentials."
    except PartialCredentialsError:
        return "Incomplete credentials provided. Please provide valid AWS credentials."
    except Exception as e:
        return f"An error occurred: {str(e)}"
    


def get_elasticache_details(profile_name, region):
    try:
        # Create a session using the specified profile
        session = boto3.Session(profile_name=profile_name)

        # Create an ElastiCache client using the specified region
        elasticache_client = session.client('elasticache', region_name=region)

        # Example: Get information about ElastiCache clusters
        response = elasticache_client.describe_cache_clusters()
        clusters = response.get('CacheClusters', [])

        return clusters

    except NoCredentialsError:
        return "Credentials not available or not valid. Please configure AWS credentials."
    except PartialCredentialsError:
        return "Incomplete credentials provided. Please provide valid AWS credentials."
    except Exception as e:
        return f"An error occurred: {str(e)}"
    



def get_vpc_details(profile_name, region):
    try:
        # Create a session using the specified profile
        session = boto3.Session(profile_name=profile_name)

        # Create a VPC client using the specified region
        ec2_client = session.client('ec2', region_name=region)

        # Example: Get information about VPCs
        response = ec2_client.describe_vpcs()
        vpcs = response.get('Vpcs', [])

        return vpcs

    except NoCredentialsError:
        return "Credentials not available or not valid. Please configure AWS credentials."
    except PartialCredentialsError:
        return "Incomplete credentials provided. Please provide valid AWS credentials."
    except Exception as e:
        return f"An error occurred: {str(e)}"



def get_iam_details(profile_name):
    try:
        # Create a session using the specified profile
        session = boto3.Session(profile_name=profile_name)

        # Create an IAM client
        iam_client = session.client('iam')

        # Get IAM users
        users_response = iam_client.list_users()
        users = users_response.get('Users', [])

        # Get IAM groups
        groups_response = iam_client.list_groups()
        groups = groups_response.get('Groups', [])

        # Get IAM roles
        roles_response = iam_client.list_roles()
        roles = roles_response.get('Roles', [])

        # Get IAM policies
        policies_response = iam_client.list_policies()
        policies = policies_response.get('Policies', [])

        return {
            'users': users,
            'groups': groups,
            'roles': roles,
            'policies': policies
        }

    except NoCredentialsError:
        return "Credentials not available or not valid. Please configure AWS credentials."
    except PartialCredentialsError:
        return "Incomplete credentials provided. Please provide valid AWS credentials."
    except Exception as e:
        return f"An error occurred: {str(e)}"




def get_cloudwatch_logs(profile_name, region):
    try:
        # Create a session using the specified profile
        session = boto3.Session(profile_name=profile_name)

        # Create a CloudWatch Logs client using the specified region
        logs_client = session.client('logs', region_name=region)

        # Get a list of log groups
        log_groups_response = logs_client.describe_log_groups()
        log_groups = log_groups_response.get('logGroups', [])

        # Extract relevant information from log groups
        log_group_list = [{'log_group_name': log_group['logGroupName']} for log_group in log_groups]

        # Get a list of log streams for each log group
        log_streams_list = []
        for log_group in log_groups:
            log_streams_response = logs_client.describe_log_streams(logGroupName=log_group['logGroupName'])
            log_streams = log_streams_response.get('logStreams', [])
            log_streams_list.extend([{'log_group_name': log_group['logGroupName'], 'log_stream_name': log_stream['logStreamName']} for log_stream in log_streams])

        return log_group_list, log_streams_list

    except NoCredentialsError:
        raise ValueError("Credentials not available or not valid. Please configure AWS credentials.")
    except PartialCredentialsError:
        raise ValueError("Incomplete credentials provided. Please provide valid AWS credentials.")
    except Exception as e:
        raise ValueError(f"An error occurred: {str(e)}")
    

def get_cloudwatch_alarms(profile_name, region):
    try:
        # Create a session using the specified profile
        session = boto3.Session(profile_name=profile_name)

        # Create a CloudWatch client using the specified region
        cloudwatch_client = session.client('cloudwatch', region_name=region)

        # Get a list of CloudWatch alarms
        alarms_response = cloudwatch_client.describe_alarms()
        alarms = alarms_response.get('MetricAlarms', [])

        # Extract relevant information from alarms
        alarm_list = [
            {
                'alarm_name': alarm['AlarmName'],
                'alarm_description': alarm.get('AlarmDescription', 'N/A'),
                'state_value': alarm['StateValue'],
                'state_reason': alarm['StateReason'],
            }
            for alarm in alarms
        ]

        return alarm_list

    except NoCredentialsError:
        raise ValueError("Credentials not available or not valid. Please configure AWS credentials.")
    except PartialCredentialsError:
        raise ValueError("Incomplete credentials provided. Please provide valid AWS credentials.")
    except Exception as e:
        raise ValueError(f"An error occurred: {str(e)}")



import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import json
from datetime import datetime
from fastapi import FastAPI
from datetime import datetime, timedelta
from functions import get_cloudwatch_logs
from models import *
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import json
from functions import get_aws_details

app = FastAPI()


@app.post("/get_aws_details", response_model=AWSDetailsResponse)
async def fetch_aws_details(request: AWSDetailsRequest):
    profile_name = request.profile_name
    region = request.region

    try:
        response = get_aws_details(profile_name, region)
        return AWSDetailsResponse(message=json.loads(response))

    except Exception as e:
        return AWSDetailsResponse(message=f"Error: {str(e)}")

@app.post("/deregister_ami", response_model=AMIDeregistrationResponse)
async def deregister_ami(request: AMIDeregistrationRequest):
    profile_name = request.profile_name
    region = request.region
    ami_id = request.ami_id

    try:
        deregister_ami(profile_name, region, ami_id)
        return AMIDeregistrationResponse(message=f"AMI deregistration initiated. AMI ID: {ami_id}")

    except Exception as e:
        return AMIDeregistrationResponse(message=f"Error: {str(e)}")
    
@app.post("/list_amis", response_model=AMIListResponse)
async def list_amis(request: AMIListRequest):
    profile_name = request.profile_name
    region = request.region

    try:
        amis = get_amis(profile_name, region)
        return AMIListResponse(amis=amis)

    except Exception as e:
        return AMIListResponse(amis=[], message=f"Error: {str(e)}")

@app.post("/get_s3_details", response_model=S3DetailsResponse)
async def fetch_s3_details(request: S3DetailsRequest):
    profile_name = request.profile_name
    bucket_name = request.bucket_name

    try:
        response = get_s3_details(profile_name, bucket_name)
        return S3DetailsResponse(message=json.loads(response))

    except Exception as e:
        return S3DetailsResponse(message=f"Error: {str(e)}")

@app.post("/list_s3_buckets", response_model=S3ListBucketsResponse)
async def list_s3_buckets(request: S3ListBucketsRequest):
    profile_name = request.profile_name

    try:
        buckets = get_s3_buckets(profile_name)
        return S3ListBucketsResponse(buckets=buckets)

    except Exception as e:
        return S3ListBucketsResponse(buckets=[], message=f"Error: {str(e)}")
    
@app.post("/get_ecs_details", response_model=ECSDetailsResponse)
async def fetch_ecs_details(request: ECSDetailsRequest):
    profile_name = request.profile_name
    region = request.region

    try:
        clusters = get_ecs_details(profile_name, region)
        return ECSDetailsResponse(clusters=clusters)

    except Exception as e:
        return ECSDetailsResponse(clusters=[], message=f"Error: {str(e)}")

@app.post("/get_ecs_services", response_model=ECSServicesResponse)
async def fetch_ecs_services(request: ECSServicesRequest):
    profile_name = request.profile_name
    region = request.region
    cluster_name = request.cluster_name

    try:
        services = get_ecs_services(profile_name, region, cluster_name)
        return ECSServicesResponse(services=services)

    except Exception as e:
        return ECSServicesResponse(services=[], message=f"Error: {str(e)}")

@app.post("/get_ecs_tasks", response_model=ECSTasksResponse)
async def fetch_ecs_tasks(request: ECSTasksRequest):
    profile_name = request.profile_name
    region = request.region
    cluster_name = request.cluster_name
    service_name = request.service_name

    try:
        tasks = get_ecs_tasks(profile_name, region, cluster_name, service_name)
        return ECSTasksResponse(tasks=tasks)

    except Exception as e:
        return ECSTasksResponse(tasks=[], message=f"Error: {str(e)}")
    
@app.post("/get_ecs_cpu_metrics", response_model=ECSCpuMetricsResponse)
async def fetch_ecs_cpu_metrics(request: ECSCpuMetricsRequest):
    profile_name = request.profile_name
    region = request.region
    cluster_name = request.cluster_name
    service_name = request.service_name
    duration_hours = request.duration_hours

    try:
        cpu_metrics = get_ecs_cpu_metrics(profile_name, region, cluster_name, service_name, duration_hours)
        return ECSCpuMetricsResponse(cpu_metrics=cpu_metrics)

    except Exception as e:
        return ECSCpuMetricsResponse(cpu_metrics=[], message=f"Error: {str(e)}")

@app.post("/get_ecs_memory_metrics", response_model=ECSMemoryMetricsResponse)
async def fetch_ecs_memory_metrics(request: ECSMemoryMetricsRequest):
    profile_name = request.profile_name
    region = request.region
    cluster_name = request.cluster_name
    service_name = request.service_name
    duration_hours = request.duration_hours

    try:
        memory_metrics = get_ecs_memory_metrics(profile_name, region, cluster_name, service_name, duration_hours)
        return ECSMemoryMetricsResponse(memory_metrics=memory_metrics)

    except Exception as e:
        return ECSMemoryMetricsResponse(memory_metrics=[], message=f"Error: {str(e)}")

@app.post("/list_cloudwatch_alarms", response_model=CloudWatchAlarmsResponse)
async def list_cloudwatch_alarms(request: CloudWatchAlarmsRequest):
    profile_name = request.profile_name
    region = request.region

    try:
        alarms = get_cloudwatch_alarms(profile_name, region)
        return CloudWatchAlarmsResponse(alarms=alarms)

    except Exception as e:
        return CloudWatchAlarmsResponse(alarms=[], message=f"Error: {str(e)}")

@app.post("/get_sqs_details", response_model=SQSDetailsResponse)
async def fetch_sqs_details(request: SQSDetailsRequest):
    profile_name = request.profile_name
    region = request.region

    try:
        queues = get_sqs_details(profile_name, region)
        return SQSDetailsResponse(queues=queues)

    except Exception as e:
        return SQSDetailsResponse(queues=[], message=f"Error: {str(e)}")

@app.post("/get_rds_details", response_model=RDSDetailsResponse)
async def fetch_rds_details(request: RDSDetailsRequest):
    profile_name = request.profile_name
    region = request.region

    try:
        instances = get_rds_details(profile_name, region)
        return RDSDetailsResponse(instances=instances)

    except Exception as e:
        return RDSDetailsResponse(instances=[], message=f"Error: {str(e)}")
    
@app.post("/get_elasticache_details", response_model=ElastiCacheDetailsResponse)
async def fetch_elasticache_details(request: ElastiCacheDetailsRequest):
    profile_name = request.profile_name
    region = request.region

    try:
        clusters = get_elasticache_details(profile_name, region)
        return ElastiCacheDetailsResponse(clusters=clusters)

    except Exception as e:
        return ElastiCacheDetailsResponse(clusters=[], message=f"Error: {str(e)}")

@app.post("/get_vpc_details", response_model=VPCDetailsResponse)
async def fetch_vpc_details(request: VPCDetailsRequest):
    profile_name = request.profile_name
    region = request.region

    try:
        vpcs = get_vpc_details(profile_name, region)
        return VPCDetailsResponse(vpcs=vpcs)

    except Exception as e:
        return VPCDetailsResponse(vpcs=[], message=f"Error: {str(e)}")

@app.post("/get_iam_details", response_model=IAMDetailsResponse)
async def fetch_iam_details(request: IAMDetailsRequest):
    profile_name = request.profile_name

    try:
        iam_details = get_iam_details(profile_name)
        return IAMDetailsResponse(**iam_details)

    except Exception as e:
        return IAMDetailsResponse(users=[], groups=[], roles=[], policies=[], message=f"Error: {str(e)}")
    
@app.post("/list_cloudwatch_logs", response_model=CloudWatchLogsResponse)
async def list_cloudwatch_logs(request: CloudWatchLogsRequest):
    profile_name = request.profile_name
    region = request.region

    try:
        log_groups, log_streams = get_cloudwatch_logs(profile_name, region)
        return CloudWatchLogsResponse(log_groups=log_groups, log_streams=log_streams)

    except Exception as e:
        return CloudWatchLogsResponse(log_groups=[], log_streams=[], message=f"Error: {str(e)}")
    
def convert_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    


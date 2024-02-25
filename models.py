from pydantic import BaseModel
from typing import Any, List, Dict

class AWSDetailsRequest(BaseModel):
    profile_name: str
    region: str

class AWSDetailsResponse(BaseModel):
    message: dict

class AMICreationRequest(BaseModel):
    profile_name: str
    region: str
    instance_id: str

class AMICreationResponse(BaseModel):
    message: str
class AMIDeregistrationRequest(BaseModel):
    profile_name: str
    region: str
    ami_id: str

class AMIDeregistrationResponse(BaseModel):
    message: str

class AMIListRequest(BaseModel):
    profile_name: str
    region: str

class AMIListResponse(BaseModel):
    amis: list

class S3DetailsRequest(BaseModel):
    profile_name: str
    bucket_name: str

class S3DetailsResponse(BaseModel):
    message: dict

class S3ListBucketsRequest(BaseModel):
    profile_name: str

class S3ListBucketsResponse(BaseModel):
    buckets: list

class ECSDetailsRequest(BaseModel):
    profile_name: str
    region: str

class ECSDetailsResponse(BaseModel):
    clusters: list

class ECSServicesRequest(BaseModel):
    profile_name: str
    region: str
    cluster_name: str

class ECSServicesResponse(BaseModel):
    services: list

class ECSTasksRequest(BaseModel):
    profile_name: str
    region: str
    cluster_name: str
    service_name: str

class ECSTasksResponse(BaseModel):
    tasks: list

class ECSCpuMetricsRequest(BaseModel):
    profile_name: str
    region: str
    cluster_name: str
    service_name: str
    duration_hours: int = 1

class ECSCpuMetricsResponse(BaseModel):
    cpu_metrics: list

class ECSMemoryMetricsRequest(BaseModel):
    profile_name: str
    region: str
    cluster_name: str
    service_name: str
    duration_hours: int = 1

class ECSMemoryMetricsResponse(BaseModel):
    memory_metrics: list

class SQSDetailsRequest(BaseModel):
    profile_name: str
    region: str

class SQSDetailsResponse(BaseModel):
    queues: list

class RDSDetailsRequest(BaseModel):
    profile_name: str
    region: str

class RDSDetailsResponse(BaseModel):
    instances: list

class ElastiCacheDetailsRequest(BaseModel):
    profile_name: str
    region: str

class ElastiCacheDetailsResponse(BaseModel):
    clusters: list

class VPCDetailsRequest(BaseModel):
    profile_name: str
    region: str

class VPCDetailsResponse(BaseModel):
    vpcs: list

class IAMDetailsRequest(BaseModel):
    profile_name: str

class IAMDetailsResponse(BaseModel):
    users: list
    groups: list
    roles: list
    policies: list

class CloudWatchLogsRequest(BaseModel):
    profile_name: str
    region: str

class CloudWatchLogsResponse(BaseModel):
    log_groups: list
    log_streams: list

class CloudWatchAlarmsRequest(BaseModel):
    profile_name: str
    region: str

class CloudWatchAlarmsResponse(BaseModel):
    alarms: list

class CloudTrailInsightsRequest(BaseModel):
    profile_name: str
    region: str
    start_time: str
    end_time: str

class CloudTrailInsightsResponse(BaseModel):
    insights: list

class CostEstimationRequest(BaseModel):
    profile_name: str
    region: str
    instance_type: str
    duration_hours: int

class CostEstimationResponse(BaseModel):
    estimated_cost: float

class ListRecommendationsRequest(BaseModel):
    profile_name: str
    region: str

class ListRecommendationsResponse(BaseModel):
    recommendations: list

class MonthlyBillRequest(BaseModel):
    profile_name: str
    start_date: str
    end_date: str

class MonthlyBillResponse(BaseModel):
    total_cost: float
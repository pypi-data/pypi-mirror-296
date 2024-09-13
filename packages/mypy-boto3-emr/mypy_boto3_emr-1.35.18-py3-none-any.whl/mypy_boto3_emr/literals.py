"""
Type annotations for emr service literal definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/literals/)

Usage::

    ```python
    from mypy_boto3_emr.literals import ActionOnFailureType

    data: ActionOnFailureType = "CANCEL_AND_WAIT"
    ```
"""

import sys

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "ActionOnFailureType",
    "AdjustmentTypeType",
    "AuthModeType",
    "AutoScalingPolicyStateChangeReasonCodeType",
    "AutoScalingPolicyStateType",
    "CancelStepsRequestStatusType",
    "ClusterRunningWaiterName",
    "ClusterStateChangeReasonCodeType",
    "ClusterStateType",
    "ClusterTerminatedWaiterName",
    "ComparisonOperatorType",
    "ComputeLimitsUnitTypeType",
    "ExecutionEngineTypeType",
    "IdcUserAssignmentType",
    "IdentityTypeType",
    "InstanceCollectionTypeType",
    "InstanceFleetStateChangeReasonCodeType",
    "InstanceFleetStateType",
    "InstanceFleetTypeType",
    "InstanceGroupStateChangeReasonCodeType",
    "InstanceGroupStateType",
    "InstanceGroupTypeType",
    "InstanceRoleTypeType",
    "InstanceStateChangeReasonCodeType",
    "InstanceStateType",
    "JobFlowExecutionStateType",
    "ListBootstrapActionsPaginatorName",
    "ListClustersPaginatorName",
    "ListInstanceFleetsPaginatorName",
    "ListInstanceGroupsPaginatorName",
    "ListInstancesPaginatorName",
    "ListNotebookExecutionsPaginatorName",
    "ListSecurityConfigurationsPaginatorName",
    "ListStepsPaginatorName",
    "ListStudioSessionMappingsPaginatorName",
    "ListStudiosPaginatorName",
    "MarketTypeType",
    "NotebookExecutionStatusType",
    "OnDemandCapacityReservationPreferenceType",
    "OnDemandCapacityReservationUsageStrategyType",
    "OnDemandProvisioningAllocationStrategyType",
    "OutputNotebookFormatType",
    "PlacementGroupStrategyType",
    "ReconfigurationTypeType",
    "RepoUpgradeOnBootType",
    "ScaleDownBehaviorType",
    "SpotProvisioningAllocationStrategyType",
    "SpotProvisioningTimeoutActionType",
    "StatisticType",
    "StepCancellationOptionType",
    "StepCompleteWaiterName",
    "StepExecutionStateType",
    "StepStateChangeReasonCodeType",
    "StepStateType",
    "UnitType",
    "EMRServiceName",
    "ServiceName",
    "ResourceServiceName",
    "PaginatorName",
    "WaiterName",
    "RegionName",
)


ActionOnFailureType = Literal[
    "CANCEL_AND_WAIT", "CONTINUE", "TERMINATE_CLUSTER", "TERMINATE_JOB_FLOW"
]
AdjustmentTypeType = Literal["CHANGE_IN_CAPACITY", "EXACT_CAPACITY", "PERCENT_CHANGE_IN_CAPACITY"]
AuthModeType = Literal["IAM", "SSO"]
AutoScalingPolicyStateChangeReasonCodeType = Literal[
    "CLEANUP_FAILURE", "PROVISION_FAILURE", "USER_REQUEST"
]
AutoScalingPolicyStateType = Literal[
    "ATTACHED", "ATTACHING", "DETACHED", "DETACHING", "FAILED", "PENDING"
]
CancelStepsRequestStatusType = Literal["FAILED", "SUBMITTED"]
ClusterRunningWaiterName = Literal["cluster_running"]
ClusterStateChangeReasonCodeType = Literal[
    "ALL_STEPS_COMPLETED",
    "BOOTSTRAP_FAILURE",
    "INSTANCE_FAILURE",
    "INSTANCE_FLEET_TIMEOUT",
    "INTERNAL_ERROR",
    "STEP_FAILURE",
    "USER_REQUEST",
    "VALIDATION_ERROR",
]
ClusterStateType = Literal[
    "BOOTSTRAPPING",
    "RUNNING",
    "STARTING",
    "TERMINATED",
    "TERMINATED_WITH_ERRORS",
    "TERMINATING",
    "WAITING",
]
ClusterTerminatedWaiterName = Literal["cluster_terminated"]
ComparisonOperatorType = Literal[
    "GREATER_THAN", "GREATER_THAN_OR_EQUAL", "LESS_THAN", "LESS_THAN_OR_EQUAL"
]
ComputeLimitsUnitTypeType = Literal["InstanceFleetUnits", "Instances", "VCPU"]
ExecutionEngineTypeType = Literal["EMR"]
IdcUserAssignmentType = Literal["OPTIONAL", "REQUIRED"]
IdentityTypeType = Literal["GROUP", "USER"]
InstanceCollectionTypeType = Literal["INSTANCE_FLEET", "INSTANCE_GROUP"]
InstanceFleetStateChangeReasonCodeType = Literal[
    "CLUSTER_TERMINATED", "INSTANCE_FAILURE", "INTERNAL_ERROR", "VALIDATION_ERROR"
]
InstanceFleetStateType = Literal[
    "BOOTSTRAPPING", "PROVISIONING", "RESIZING", "RUNNING", "SUSPENDED", "TERMINATED", "TERMINATING"
]
InstanceFleetTypeType = Literal["CORE", "MASTER", "TASK"]
InstanceGroupStateChangeReasonCodeType = Literal[
    "CLUSTER_TERMINATED", "INSTANCE_FAILURE", "INTERNAL_ERROR", "VALIDATION_ERROR"
]
InstanceGroupStateType = Literal[
    "ARRESTED",
    "BOOTSTRAPPING",
    "ENDED",
    "PROVISIONING",
    "RECONFIGURING",
    "RESIZING",
    "RUNNING",
    "SHUTTING_DOWN",
    "SUSPENDED",
    "TERMINATED",
    "TERMINATING",
]
InstanceGroupTypeType = Literal["CORE", "MASTER", "TASK"]
InstanceRoleTypeType = Literal["CORE", "MASTER", "TASK"]
InstanceStateChangeReasonCodeType = Literal[
    "BOOTSTRAP_FAILURE",
    "CLUSTER_TERMINATED",
    "INSTANCE_FAILURE",
    "INTERNAL_ERROR",
    "VALIDATION_ERROR",
]
InstanceStateType = Literal[
    "AWAITING_FULFILLMENT", "BOOTSTRAPPING", "PROVISIONING", "RUNNING", "TERMINATED"
]
JobFlowExecutionStateType = Literal[
    "BOOTSTRAPPING",
    "COMPLETED",
    "FAILED",
    "RUNNING",
    "SHUTTING_DOWN",
    "STARTING",
    "TERMINATED",
    "WAITING",
]
ListBootstrapActionsPaginatorName = Literal["list_bootstrap_actions"]
ListClustersPaginatorName = Literal["list_clusters"]
ListInstanceFleetsPaginatorName = Literal["list_instance_fleets"]
ListInstanceGroupsPaginatorName = Literal["list_instance_groups"]
ListInstancesPaginatorName = Literal["list_instances"]
ListNotebookExecutionsPaginatorName = Literal["list_notebook_executions"]
ListSecurityConfigurationsPaginatorName = Literal["list_security_configurations"]
ListStepsPaginatorName = Literal["list_steps"]
ListStudioSessionMappingsPaginatorName = Literal["list_studio_session_mappings"]
ListStudiosPaginatorName = Literal["list_studios"]
MarketTypeType = Literal["ON_DEMAND", "SPOT"]
NotebookExecutionStatusType = Literal[
    "FAILED",
    "FAILING",
    "FINISHED",
    "FINISHING",
    "RUNNING",
    "STARTING",
    "START_PENDING",
    "STOPPED",
    "STOPPING",
    "STOP_PENDING",
]
OnDemandCapacityReservationPreferenceType = Literal["none", "open"]
OnDemandCapacityReservationUsageStrategyType = Literal["use-capacity-reservations-first"]
OnDemandProvisioningAllocationStrategyType = Literal["lowest-price", "prioritized"]
OutputNotebookFormatType = Literal["HTML"]
PlacementGroupStrategyType = Literal["CLUSTER", "NONE", "PARTITION", "SPREAD"]
ReconfigurationTypeType = Literal["MERGE", "OVERWRITE"]
RepoUpgradeOnBootType = Literal["NONE", "SECURITY"]
ScaleDownBehaviorType = Literal["TERMINATE_AT_INSTANCE_HOUR", "TERMINATE_AT_TASK_COMPLETION"]
SpotProvisioningAllocationStrategyType = Literal[
    "capacity-optimized",
    "capacity-optimized-prioritized",
    "diversified",
    "lowest-price",
    "price-capacity-optimized",
]
SpotProvisioningTimeoutActionType = Literal["SWITCH_TO_ON_DEMAND", "TERMINATE_CLUSTER"]
StatisticType = Literal["AVERAGE", "MAXIMUM", "MINIMUM", "SAMPLE_COUNT", "SUM"]
StepCancellationOptionType = Literal["SEND_INTERRUPT", "TERMINATE_PROCESS"]
StepCompleteWaiterName = Literal["step_complete"]
StepExecutionStateType = Literal[
    "CANCELLED", "COMPLETED", "CONTINUE", "FAILED", "INTERRUPTED", "PENDING", "RUNNING"
]
StepStateChangeReasonCodeType = Literal["NONE"]
StepStateType = Literal[
    "CANCELLED", "CANCEL_PENDING", "COMPLETED", "FAILED", "INTERRUPTED", "PENDING", "RUNNING"
]
UnitType = Literal[
    "BITS",
    "BITS_PER_SECOND",
    "BYTES",
    "BYTES_PER_SECOND",
    "COUNT",
    "COUNT_PER_SECOND",
    "GIGA_BITS",
    "GIGA_BITS_PER_SECOND",
    "GIGA_BYTES",
    "GIGA_BYTES_PER_SECOND",
    "KILO_BITS",
    "KILO_BITS_PER_SECOND",
    "KILO_BYTES",
    "KILO_BYTES_PER_SECOND",
    "MEGA_BITS",
    "MEGA_BITS_PER_SECOND",
    "MEGA_BYTES",
    "MEGA_BYTES_PER_SECOND",
    "MICRO_SECONDS",
    "MILLI_SECONDS",
    "NONE",
    "PERCENT",
    "SECONDS",
    "TERA_BITS",
    "TERA_BITS_PER_SECOND",
    "TERA_BYTES",
    "TERA_BYTES_PER_SECOND",
]
EMRServiceName = Literal["emr"]
ServiceName = Literal[
    "accessanalyzer",
    "account",
    "acm",
    "acm-pca",
    "amp",
    "amplify",
    "amplifybackend",
    "amplifyuibuilder",
    "apigateway",
    "apigatewaymanagementapi",
    "apigatewayv2",
    "appconfig",
    "appconfigdata",
    "appfabric",
    "appflow",
    "appintegrations",
    "application-autoscaling",
    "application-insights",
    "application-signals",
    "applicationcostprofiler",
    "appmesh",
    "apprunner",
    "appstream",
    "appsync",
    "apptest",
    "arc-zonal-shift",
    "artifact",
    "athena",
    "auditmanager",
    "autoscaling",
    "autoscaling-plans",
    "b2bi",
    "backup",
    "backup-gateway",
    "batch",
    "bcm-data-exports",
    "bedrock",
    "bedrock-agent",
    "bedrock-agent-runtime",
    "bedrock-runtime",
    "billingconductor",
    "braket",
    "budgets",
    "ce",
    "chatbot",
    "chime",
    "chime-sdk-identity",
    "chime-sdk-media-pipelines",
    "chime-sdk-meetings",
    "chime-sdk-messaging",
    "chime-sdk-voice",
    "cleanrooms",
    "cleanroomsml",
    "cloud9",
    "cloudcontrol",
    "clouddirectory",
    "cloudformation",
    "cloudfront",
    "cloudfront-keyvaluestore",
    "cloudhsm",
    "cloudhsmv2",
    "cloudsearch",
    "cloudsearchdomain",
    "cloudtrail",
    "cloudtrail-data",
    "cloudwatch",
    "codeartifact",
    "codebuild",
    "codecatalyst",
    "codecommit",
    "codeconnections",
    "codedeploy",
    "codeguru-reviewer",
    "codeguru-security",
    "codeguruprofiler",
    "codepipeline",
    "codestar-connections",
    "codestar-notifications",
    "cognito-identity",
    "cognito-idp",
    "cognito-sync",
    "comprehend",
    "comprehendmedical",
    "compute-optimizer",
    "config",
    "connect",
    "connect-contact-lens",
    "connectcampaigns",
    "connectcases",
    "connectparticipant",
    "controlcatalog",
    "controltower",
    "cost-optimization-hub",
    "cur",
    "customer-profiles",
    "databrew",
    "dataexchange",
    "datapipeline",
    "datasync",
    "datazone",
    "dax",
    "deadline",
    "detective",
    "devicefarm",
    "devops-guru",
    "directconnect",
    "discovery",
    "dlm",
    "dms",
    "docdb",
    "docdb-elastic",
    "drs",
    "ds",
    "dynamodb",
    "dynamodbstreams",
    "ebs",
    "ec2",
    "ec2-instance-connect",
    "ecr",
    "ecr-public",
    "ecs",
    "efs",
    "eks",
    "eks-auth",
    "elastic-inference",
    "elasticache",
    "elasticbeanstalk",
    "elastictranscoder",
    "elb",
    "elbv2",
    "emr",
    "emr-containers",
    "emr-serverless",
    "entityresolution",
    "es",
    "events",
    "evidently",
    "finspace",
    "finspace-data",
    "firehose",
    "fis",
    "fms",
    "forecast",
    "forecastquery",
    "frauddetector",
    "freetier",
    "fsx",
    "gamelift",
    "glacier",
    "globalaccelerator",
    "glue",
    "grafana",
    "greengrass",
    "greengrassv2",
    "groundstation",
    "guardduty",
    "health",
    "healthlake",
    "iam",
    "identitystore",
    "imagebuilder",
    "importexport",
    "inspector",
    "inspector-scan",
    "inspector2",
    "internetmonitor",
    "iot",
    "iot-data",
    "iot-jobs-data",
    "iot1click-devices",
    "iot1click-projects",
    "iotanalytics",
    "iotdeviceadvisor",
    "iotevents",
    "iotevents-data",
    "iotfleethub",
    "iotfleetwise",
    "iotsecuretunneling",
    "iotsitewise",
    "iotthingsgraph",
    "iottwinmaker",
    "iotwireless",
    "ivs",
    "ivs-realtime",
    "ivschat",
    "kafka",
    "kafkaconnect",
    "kendra",
    "kendra-ranking",
    "keyspaces",
    "kinesis",
    "kinesis-video-archived-media",
    "kinesis-video-media",
    "kinesis-video-signaling",
    "kinesis-video-webrtc-storage",
    "kinesisanalytics",
    "kinesisanalyticsv2",
    "kinesisvideo",
    "kms",
    "lakeformation",
    "lambda",
    "launch-wizard",
    "lex-models",
    "lex-runtime",
    "lexv2-models",
    "lexv2-runtime",
    "license-manager",
    "license-manager-linux-subscriptions",
    "license-manager-user-subscriptions",
    "lightsail",
    "location",
    "logs",
    "lookoutequipment",
    "lookoutmetrics",
    "lookoutvision",
    "m2",
    "machinelearning",
    "macie2",
    "mailmanager",
    "managedblockchain",
    "managedblockchain-query",
    "marketplace-agreement",
    "marketplace-catalog",
    "marketplace-deployment",
    "marketplace-entitlement",
    "marketplacecommerceanalytics",
    "mediaconnect",
    "mediaconvert",
    "medialive",
    "mediapackage",
    "mediapackage-vod",
    "mediapackagev2",
    "mediastore",
    "mediastore-data",
    "mediatailor",
    "medical-imaging",
    "memorydb",
    "meteringmarketplace",
    "mgh",
    "mgn",
    "migration-hub-refactor-spaces",
    "migrationhub-config",
    "migrationhuborchestrator",
    "migrationhubstrategy",
    "mq",
    "mturk",
    "mwaa",
    "neptune",
    "neptune-graph",
    "neptunedata",
    "network-firewall",
    "networkmanager",
    "networkmonitor",
    "nimble",
    "oam",
    "omics",
    "opensearch",
    "opensearchserverless",
    "opsworks",
    "opsworkscm",
    "organizations",
    "osis",
    "outposts",
    "panorama",
    "payment-cryptography",
    "payment-cryptography-data",
    "pca-connector-ad",
    "pca-connector-scep",
    "pcs",
    "personalize",
    "personalize-events",
    "personalize-runtime",
    "pi",
    "pinpoint",
    "pinpoint-email",
    "pinpoint-sms-voice",
    "pinpoint-sms-voice-v2",
    "pipes",
    "polly",
    "pricing",
    "privatenetworks",
    "proton",
    "qapps",
    "qbusiness",
    "qconnect",
    "qldb",
    "qldb-session",
    "quicksight",
    "ram",
    "rbin",
    "rds",
    "rds-data",
    "redshift",
    "redshift-data",
    "redshift-serverless",
    "rekognition",
    "repostspace",
    "resiliencehub",
    "resource-explorer-2",
    "resource-groups",
    "resourcegroupstaggingapi",
    "robomaker",
    "rolesanywhere",
    "route53",
    "route53-recovery-cluster",
    "route53-recovery-control-config",
    "route53-recovery-readiness",
    "route53domains",
    "route53profiles",
    "route53resolver",
    "rum",
    "s3",
    "s3control",
    "s3outposts",
    "sagemaker",
    "sagemaker-a2i-runtime",
    "sagemaker-edge",
    "sagemaker-featurestore-runtime",
    "sagemaker-geospatial",
    "sagemaker-metrics",
    "sagemaker-runtime",
    "savingsplans",
    "scheduler",
    "schemas",
    "sdb",
    "secretsmanager",
    "securityhub",
    "securitylake",
    "serverlessrepo",
    "service-quotas",
    "servicecatalog",
    "servicecatalog-appregistry",
    "servicediscovery",
    "ses",
    "sesv2",
    "shield",
    "signer",
    "simspaceweaver",
    "sms",
    "sms-voice",
    "snow-device-management",
    "snowball",
    "sns",
    "sqs",
    "ssm",
    "ssm-contacts",
    "ssm-incidents",
    "ssm-quicksetup",
    "ssm-sap",
    "sso",
    "sso-admin",
    "sso-oidc",
    "stepfunctions",
    "storagegateway",
    "sts",
    "supplychain",
    "support",
    "support-app",
    "swf",
    "synthetics",
    "taxsettings",
    "textract",
    "timestream-influxdb",
    "timestream-query",
    "timestream-write",
    "tnb",
    "transcribe",
    "transfer",
    "translate",
    "trustedadvisor",
    "verifiedpermissions",
    "voice-id",
    "vpc-lattice",
    "waf",
    "waf-regional",
    "wafv2",
    "wellarchitected",
    "wisdom",
    "workdocs",
    "worklink",
    "workmail",
    "workmailmessageflow",
    "workspaces",
    "workspaces-thin-client",
    "workspaces-web",
    "xray",
]
ResourceServiceName = Literal[
    "cloudformation",
    "cloudwatch",
    "dynamodb",
    "ec2",
    "glacier",
    "iam",
    "opsworks",
    "s3",
    "sns",
    "sqs",
]
PaginatorName = Literal[
    "list_bootstrap_actions",
    "list_clusters",
    "list_instance_fleets",
    "list_instance_groups",
    "list_instances",
    "list_notebook_executions",
    "list_security_configurations",
    "list_steps",
    "list_studio_session_mappings",
    "list_studios",
]
WaiterName = Literal["cluster_running", "cluster_terminated", "step_complete"]
RegionName = Literal[
    "af-south-1",
    "ap-east-1",
    "ap-northeast-1",
    "ap-northeast-2",
    "ap-northeast-3",
    "ap-south-1",
    "ap-south-2",
    "ap-southeast-1",
    "ap-southeast-2",
    "ap-southeast-3",
    "ap-southeast-4",
    "ap-southeast-5",
    "ca-central-1",
    "ca-west-1",
    "eu-central-1",
    "eu-central-2",
    "eu-north-1",
    "eu-south-1",
    "eu-south-2",
    "eu-west-1",
    "eu-west-2",
    "eu-west-3",
    "il-central-1",
    "me-central-1",
    "me-south-1",
    "sa-east-1",
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2",
]

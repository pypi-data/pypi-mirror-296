"""
Type annotations for elbv2 service literal definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elbv2/literals/)

Usage::

    ```python
    from mypy_boto3_elbv2.literals import ActionTypeEnumType

    data: ActionTypeEnumType = "authenticate-cognito"
    ```
"""

import sys

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "ActionTypeEnumType",
    "AnomalyResultEnumType",
    "AuthenticateCognitoActionConditionalBehaviorEnumType",
    "AuthenticateOidcActionConditionalBehaviorEnumType",
    "DescribeAccountLimitsPaginatorName",
    "DescribeListenerCertificatesPaginatorName",
    "DescribeListenersPaginatorName",
    "DescribeLoadBalancersPaginatorName",
    "DescribeRulesPaginatorName",
    "DescribeSSLPoliciesPaginatorName",
    "DescribeTargetGroupsPaginatorName",
    "DescribeTargetHealthInputIncludeEnumType",
    "EnforceSecurityGroupInboundRulesOnPrivateLinkTrafficEnumType",
    "IpAddressTypeType",
    "LoadBalancerAvailableWaiterName",
    "LoadBalancerExistsWaiterName",
    "LoadBalancerSchemeEnumType",
    "LoadBalancerStateEnumType",
    "LoadBalancerTypeEnumType",
    "LoadBalancersDeletedWaiterName",
    "MitigationInEffectEnumType",
    "ProtocolEnumType",
    "RedirectActionStatusCodeEnumType",
    "RevocationTypeType",
    "TargetDeregisteredWaiterName",
    "TargetGroupIpAddressTypeEnumType",
    "TargetHealthReasonEnumType",
    "TargetHealthStateEnumType",
    "TargetInServiceWaiterName",
    "TargetTypeEnumType",
    "TrustStoreAssociationStatusEnumType",
    "TrustStoreStatusType",
    "ElasticLoadBalancingv2ServiceName",
    "ServiceName",
    "ResourceServiceName",
    "PaginatorName",
    "WaiterName",
    "RegionName",
)


ActionTypeEnumType = Literal[
    "authenticate-cognito", "authenticate-oidc", "fixed-response", "forward", "redirect"
]
AnomalyResultEnumType = Literal["anomalous", "normal"]
AuthenticateCognitoActionConditionalBehaviorEnumType = Literal["allow", "authenticate", "deny"]
AuthenticateOidcActionConditionalBehaviorEnumType = Literal["allow", "authenticate", "deny"]
DescribeAccountLimitsPaginatorName = Literal["describe_account_limits"]
DescribeListenerCertificatesPaginatorName = Literal["describe_listener_certificates"]
DescribeListenersPaginatorName = Literal["describe_listeners"]
DescribeLoadBalancersPaginatorName = Literal["describe_load_balancers"]
DescribeRulesPaginatorName = Literal["describe_rules"]
DescribeSSLPoliciesPaginatorName = Literal["describe_ssl_policies"]
DescribeTargetGroupsPaginatorName = Literal["describe_target_groups"]
DescribeTargetHealthInputIncludeEnumType = Literal["All", "AnomalyDetection"]
EnforceSecurityGroupInboundRulesOnPrivateLinkTrafficEnumType = Literal["off", "on"]
IpAddressTypeType = Literal["dualstack", "dualstack-without-public-ipv4", "ipv4"]
LoadBalancerAvailableWaiterName = Literal["load_balancer_available"]
LoadBalancerExistsWaiterName = Literal["load_balancer_exists"]
LoadBalancerSchemeEnumType = Literal["internal", "internet-facing"]
LoadBalancerStateEnumType = Literal["active", "active_impaired", "failed", "provisioning"]
LoadBalancerTypeEnumType = Literal["application", "gateway", "network"]
LoadBalancersDeletedWaiterName = Literal["load_balancers_deleted"]
MitigationInEffectEnumType = Literal["no", "yes"]
ProtocolEnumType = Literal["GENEVE", "HTTP", "HTTPS", "TCP", "TCP_UDP", "TLS", "UDP"]
RedirectActionStatusCodeEnumType = Literal["HTTP_301", "HTTP_302"]
RevocationTypeType = Literal["CRL"]
TargetDeregisteredWaiterName = Literal["target_deregistered"]
TargetGroupIpAddressTypeEnumType = Literal["ipv4", "ipv6"]
TargetHealthReasonEnumType = Literal[
    "Elb.InitialHealthChecking",
    "Elb.InternalError",
    "Elb.RegistrationInProgress",
    "Target.DeregistrationInProgress",
    "Target.FailedHealthChecks",
    "Target.HealthCheckDisabled",
    "Target.InvalidState",
    "Target.IpUnusable",
    "Target.NotInUse",
    "Target.NotRegistered",
    "Target.ResponseCodeMismatch",
    "Target.Timeout",
]
TargetHealthStateEnumType = Literal[
    "draining", "healthy", "initial", "unavailable", "unhealthy", "unhealthy.draining", "unused"
]
TargetInServiceWaiterName = Literal["target_in_service"]
TargetTypeEnumType = Literal["alb", "instance", "ip", "lambda"]
TrustStoreAssociationStatusEnumType = Literal["active", "removed"]
TrustStoreStatusType = Literal["ACTIVE", "CREATING"]
ElasticLoadBalancingv2ServiceName = Literal["elbv2"]
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
    "describe_account_limits",
    "describe_listener_certificates",
    "describe_listeners",
    "describe_load_balancers",
    "describe_rules",
    "describe_ssl_policies",
    "describe_target_groups",
]
WaiterName = Literal[
    "load_balancer_available",
    "load_balancer_exists",
    "load_balancers_deleted",
    "target_deregistered",
    "target_in_service",
]
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

"""
Type annotations for emr service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_emr.client import EMRClient

    session = Session()
    client: EMRClient = session.client("emr")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListBootstrapActionsPaginator,
    ListClustersPaginator,
    ListInstanceFleetsPaginator,
    ListInstanceGroupsPaginator,
    ListInstancesPaginator,
    ListNotebookExecutionsPaginator,
    ListSecurityConfigurationsPaginator,
    ListStepsPaginator,
    ListStudioSessionMappingsPaginator,
    ListStudiosPaginator,
)
from .type_defs import (
    AddInstanceFleetInputRequestTypeDef,
    AddInstanceFleetOutputTypeDef,
    AddInstanceGroupsInputRequestTypeDef,
    AddInstanceGroupsOutputTypeDef,
    AddJobFlowStepsInputRequestTypeDef,
    AddJobFlowStepsOutputTypeDef,
    AddTagsInputRequestTypeDef,
    CancelStepsInputRequestTypeDef,
    CancelStepsOutputTypeDef,
    CreateSecurityConfigurationInputRequestTypeDef,
    CreateSecurityConfigurationOutputTypeDef,
    CreateStudioInputRequestTypeDef,
    CreateStudioOutputTypeDef,
    CreateStudioSessionMappingInputRequestTypeDef,
    DeleteSecurityConfigurationInputRequestTypeDef,
    DeleteStudioInputRequestTypeDef,
    DeleteStudioSessionMappingInputRequestTypeDef,
    DescribeClusterInputRequestTypeDef,
    DescribeClusterOutputTypeDef,
    DescribeJobFlowsInputRequestTypeDef,
    DescribeJobFlowsOutputTypeDef,
    DescribeNotebookExecutionInputRequestTypeDef,
    DescribeNotebookExecutionOutputTypeDef,
    DescribeReleaseLabelInputRequestTypeDef,
    DescribeReleaseLabelOutputTypeDef,
    DescribeSecurityConfigurationInputRequestTypeDef,
    DescribeSecurityConfigurationOutputTypeDef,
    DescribeStepInputRequestTypeDef,
    DescribeStepOutputTypeDef,
    DescribeStudioInputRequestTypeDef,
    DescribeStudioOutputTypeDef,
    EmptyResponseMetadataTypeDef,
    GetAutoTerminationPolicyInputRequestTypeDef,
    GetAutoTerminationPolicyOutputTypeDef,
    GetBlockPublicAccessConfigurationOutputTypeDef,
    GetClusterSessionCredentialsInputRequestTypeDef,
    GetClusterSessionCredentialsOutputTypeDef,
    GetManagedScalingPolicyInputRequestTypeDef,
    GetManagedScalingPolicyOutputTypeDef,
    GetStudioSessionMappingInputRequestTypeDef,
    GetStudioSessionMappingOutputTypeDef,
    ListBootstrapActionsInputRequestTypeDef,
    ListBootstrapActionsOutputTypeDef,
    ListClustersInputRequestTypeDef,
    ListClustersOutputTypeDef,
    ListInstanceFleetsInputRequestTypeDef,
    ListInstanceFleetsOutputTypeDef,
    ListInstanceGroupsInputRequestTypeDef,
    ListInstanceGroupsOutputTypeDef,
    ListInstancesInputRequestTypeDef,
    ListInstancesOutputTypeDef,
    ListNotebookExecutionsInputRequestTypeDef,
    ListNotebookExecutionsOutputTypeDef,
    ListReleaseLabelsInputRequestTypeDef,
    ListReleaseLabelsOutputTypeDef,
    ListSecurityConfigurationsInputRequestTypeDef,
    ListSecurityConfigurationsOutputTypeDef,
    ListStepsInputRequestTypeDef,
    ListStepsOutputTypeDef,
    ListStudioSessionMappingsInputRequestTypeDef,
    ListStudioSessionMappingsOutputTypeDef,
    ListStudiosInputRequestTypeDef,
    ListStudiosOutputTypeDef,
    ListSupportedInstanceTypesInputRequestTypeDef,
    ListSupportedInstanceTypesOutputTypeDef,
    ModifyClusterInputRequestTypeDef,
    ModifyClusterOutputTypeDef,
    ModifyInstanceFleetInputRequestTypeDef,
    ModifyInstanceGroupsInputRequestTypeDef,
    PutAutoScalingPolicyInputRequestTypeDef,
    PutAutoScalingPolicyOutputTypeDef,
    PutAutoTerminationPolicyInputRequestTypeDef,
    PutBlockPublicAccessConfigurationInputRequestTypeDef,
    PutManagedScalingPolicyInputRequestTypeDef,
    RemoveAutoScalingPolicyInputRequestTypeDef,
    RemoveAutoTerminationPolicyInputRequestTypeDef,
    RemoveManagedScalingPolicyInputRequestTypeDef,
    RemoveTagsInputRequestTypeDef,
    RunJobFlowInputRequestTypeDef,
    RunJobFlowOutputTypeDef,
    SetKeepJobFlowAliveWhenNoStepsInputRequestTypeDef,
    SetTerminationProtectionInputRequestTypeDef,
    SetUnhealthyNodeReplacementInputRequestTypeDef,
    SetVisibleToAllUsersInputRequestTypeDef,
    StartNotebookExecutionInputRequestTypeDef,
    StartNotebookExecutionOutputTypeDef,
    StopNotebookExecutionInputRequestTypeDef,
    TerminateJobFlowsInputRequestTypeDef,
    UpdateStudioInputRequestTypeDef,
    UpdateStudioSessionMappingInputRequestTypeDef,
)
from .waiter import ClusterRunningWaiter, ClusterTerminatedWaiter, StepCompleteWaiter

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("EMRClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalServerError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]


class EMRClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        EMRClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#exceptions)
        """

    def add_instance_fleet(
        self, **kwargs: Unpack[AddInstanceFleetInputRequestTypeDef]
    ) -> AddInstanceFleetOutputTypeDef:
        """
        Adds an instance fleet to a running cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.add_instance_fleet)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#add_instance_fleet)
        """

    def add_instance_groups(
        self, **kwargs: Unpack[AddInstanceGroupsInputRequestTypeDef]
    ) -> AddInstanceGroupsOutputTypeDef:
        """
        Adds one or more instance groups to a running cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.add_instance_groups)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#add_instance_groups)
        """

    def add_job_flow_steps(
        self, **kwargs: Unpack[AddJobFlowStepsInputRequestTypeDef]
    ) -> AddJobFlowStepsOutputTypeDef:
        """
        AddJobFlowSteps adds new steps to a running cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.add_job_flow_steps)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#add_job_flow_steps)
        """

    def add_tags(self, **kwargs: Unpack[AddTagsInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds tags to an Amazon EMR resource, such as a cluster or an Amazon EMR Studio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.add_tags)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#add_tags)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#can_paginate)
        """

    def cancel_steps(
        self, **kwargs: Unpack[CancelStepsInputRequestTypeDef]
    ) -> CancelStepsOutputTypeDef:
        """
        Cancels a pending step or steps in a running cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.cancel_steps)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#cancel_steps)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#close)
        """

    def create_security_configuration(
        self, **kwargs: Unpack[CreateSecurityConfigurationInputRequestTypeDef]
    ) -> CreateSecurityConfigurationOutputTypeDef:
        """
        Creates a security configuration, which is stored in the service and can be
        specified when a cluster is
        created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.create_security_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#create_security_configuration)
        """

    def create_studio(
        self, **kwargs: Unpack[CreateStudioInputRequestTypeDef]
    ) -> CreateStudioOutputTypeDef:
        """
        Creates a new Amazon EMR Studio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.create_studio)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#create_studio)
        """

    def create_studio_session_mapping(
        self, **kwargs: Unpack[CreateStudioSessionMappingInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Maps a user or group to the Amazon EMR Studio specified by `StudioId`, and
        applies a session policy to refine Studio permissions for that user or
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.create_studio_session_mapping)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#create_studio_session_mapping)
        """

    def delete_security_configuration(
        self, **kwargs: Unpack[DeleteSecurityConfigurationInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a security configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.delete_security_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#delete_security_configuration)
        """

    def delete_studio(
        self, **kwargs: Unpack[DeleteStudioInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes an Amazon EMR Studio from the Studio metadata store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.delete_studio)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#delete_studio)
        """

    def delete_studio_session_mapping(
        self, **kwargs: Unpack[DeleteStudioSessionMappingInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes a user or group from an Amazon EMR Studio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.delete_studio_session_mapping)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#delete_studio_session_mapping)
        """

    def describe_cluster(
        self, **kwargs: Unpack[DescribeClusterInputRequestTypeDef]
    ) -> DescribeClusterOutputTypeDef:
        """
        Provides cluster-level details including status, hardware and software
        configuration, VPC settings, and so
        on.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.describe_cluster)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#describe_cluster)
        """

    def describe_job_flows(
        self, **kwargs: Unpack[DescribeJobFlowsInputRequestTypeDef]
    ) -> DescribeJobFlowsOutputTypeDef:
        """
        This API is no longer supported and will eventually be removed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.describe_job_flows)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#describe_job_flows)
        """

    def describe_notebook_execution(
        self, **kwargs: Unpack[DescribeNotebookExecutionInputRequestTypeDef]
    ) -> DescribeNotebookExecutionOutputTypeDef:
        """
        Provides details of a notebook execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.describe_notebook_execution)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#describe_notebook_execution)
        """

    def describe_release_label(
        self, **kwargs: Unpack[DescribeReleaseLabelInputRequestTypeDef]
    ) -> DescribeReleaseLabelOutputTypeDef:
        """
        Provides Amazon EMR release label details, such as the releases available the
        Region where the API request is run, and the available applications for a
        specific Amazon EMR release
        label.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.describe_release_label)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#describe_release_label)
        """

    def describe_security_configuration(
        self, **kwargs: Unpack[DescribeSecurityConfigurationInputRequestTypeDef]
    ) -> DescribeSecurityConfigurationOutputTypeDef:
        """
        Provides the details of a security configuration by returning the configuration
        JSON.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.describe_security_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#describe_security_configuration)
        """

    def describe_step(
        self, **kwargs: Unpack[DescribeStepInputRequestTypeDef]
    ) -> DescribeStepOutputTypeDef:
        """
        Provides more detail about the cluster step.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.describe_step)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#describe_step)
        """

    def describe_studio(
        self, **kwargs: Unpack[DescribeStudioInputRequestTypeDef]
    ) -> DescribeStudioOutputTypeDef:
        """
        Returns details for the specified Amazon EMR Studio including ID, Name, VPC,
        Studio access URL, and so
        on.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.describe_studio)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#describe_studio)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#generate_presigned_url)
        """

    def get_auto_termination_policy(
        self, **kwargs: Unpack[GetAutoTerminationPolicyInputRequestTypeDef]
    ) -> GetAutoTerminationPolicyOutputTypeDef:
        """
        Returns the auto-termination policy for an Amazon EMR cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.get_auto_termination_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#get_auto_termination_policy)
        """

    def get_block_public_access_configuration(
        self,
    ) -> GetBlockPublicAccessConfigurationOutputTypeDef:
        """
        Returns the Amazon EMR block public access configuration for your Amazon Web
        Services account in the current
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.get_block_public_access_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#get_block_public_access_configuration)
        """

    def get_cluster_session_credentials(
        self, **kwargs: Unpack[GetClusterSessionCredentialsInputRequestTypeDef]
    ) -> GetClusterSessionCredentialsOutputTypeDef:
        """
        Provides temporary, HTTP basic credentials that are associated with a given
        runtime IAM role and used by a cluster with fine-grained access control
        activated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.get_cluster_session_credentials)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#get_cluster_session_credentials)
        """

    def get_managed_scaling_policy(
        self, **kwargs: Unpack[GetManagedScalingPolicyInputRequestTypeDef]
    ) -> GetManagedScalingPolicyOutputTypeDef:
        """
        Fetches the attached managed scaling policy for an Amazon EMR cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.get_managed_scaling_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#get_managed_scaling_policy)
        """

    def get_studio_session_mapping(
        self, **kwargs: Unpack[GetStudioSessionMappingInputRequestTypeDef]
    ) -> GetStudioSessionMappingOutputTypeDef:
        """
        Fetches mapping details for the specified Amazon EMR Studio and identity (user
        or
        group).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.get_studio_session_mapping)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#get_studio_session_mapping)
        """

    def list_bootstrap_actions(
        self, **kwargs: Unpack[ListBootstrapActionsInputRequestTypeDef]
    ) -> ListBootstrapActionsOutputTypeDef:
        """
        Provides information about the bootstrap actions associated with a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.list_bootstrap_actions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#list_bootstrap_actions)
        """

    def list_clusters(
        self, **kwargs: Unpack[ListClustersInputRequestTypeDef]
    ) -> ListClustersOutputTypeDef:
        """
        Provides the status of all clusters visible to this Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.list_clusters)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#list_clusters)
        """

    def list_instance_fleets(
        self, **kwargs: Unpack[ListInstanceFleetsInputRequestTypeDef]
    ) -> ListInstanceFleetsOutputTypeDef:
        """
        Lists all available details about the instance fleets in a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.list_instance_fleets)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#list_instance_fleets)
        """

    def list_instance_groups(
        self, **kwargs: Unpack[ListInstanceGroupsInputRequestTypeDef]
    ) -> ListInstanceGroupsOutputTypeDef:
        """
        Provides all available details about the instance groups in a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.list_instance_groups)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#list_instance_groups)
        """

    def list_instances(
        self, **kwargs: Unpack[ListInstancesInputRequestTypeDef]
    ) -> ListInstancesOutputTypeDef:
        """
        Provides information for all active Amazon EC2 instances and Amazon EC2
        instances terminated in the last 30 days, up to a maximum of
        2,000.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.list_instances)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#list_instances)
        """

    def list_notebook_executions(
        self, **kwargs: Unpack[ListNotebookExecutionsInputRequestTypeDef]
    ) -> ListNotebookExecutionsOutputTypeDef:
        """
        Provides summaries of all notebook executions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.list_notebook_executions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#list_notebook_executions)
        """

    def list_release_labels(
        self, **kwargs: Unpack[ListReleaseLabelsInputRequestTypeDef]
    ) -> ListReleaseLabelsOutputTypeDef:
        """
        Retrieves release labels of Amazon EMR services in the Region where the API is
        called.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.list_release_labels)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#list_release_labels)
        """

    def list_security_configurations(
        self, **kwargs: Unpack[ListSecurityConfigurationsInputRequestTypeDef]
    ) -> ListSecurityConfigurationsOutputTypeDef:
        """
        Lists all the security configurations visible to this account, providing their
        creation dates and times, and their
        names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.list_security_configurations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#list_security_configurations)
        """

    def list_steps(self, **kwargs: Unpack[ListStepsInputRequestTypeDef]) -> ListStepsOutputTypeDef:
        """
        Provides a list of steps for the cluster in reverse order unless you specify
        `stepIds` with the request or filter by
        `StepStates`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.list_steps)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#list_steps)
        """

    def list_studio_session_mappings(
        self, **kwargs: Unpack[ListStudioSessionMappingsInputRequestTypeDef]
    ) -> ListStudioSessionMappingsOutputTypeDef:
        """
        Returns a list of all user or group session mappings for the Amazon EMR Studio
        specified by
        `StudioId`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.list_studio_session_mappings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#list_studio_session_mappings)
        """

    def list_studios(
        self, **kwargs: Unpack[ListStudiosInputRequestTypeDef]
    ) -> ListStudiosOutputTypeDef:
        """
        Returns a list of all Amazon EMR Studios associated with the Amazon Web
        Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.list_studios)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#list_studios)
        """

    def list_supported_instance_types(
        self, **kwargs: Unpack[ListSupportedInstanceTypesInputRequestTypeDef]
    ) -> ListSupportedInstanceTypesOutputTypeDef:
        """
        A list of the instance types that Amazon EMR supports.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.list_supported_instance_types)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#list_supported_instance_types)
        """

    def modify_cluster(
        self, **kwargs: Unpack[ModifyClusterInputRequestTypeDef]
    ) -> ModifyClusterOutputTypeDef:
        """
        Modifies the number of steps that can be executed concurrently for the cluster
        specified using
        ClusterID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.modify_cluster)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#modify_cluster)
        """

    def modify_instance_fleet(
        self, **kwargs: Unpack[ModifyInstanceFleetInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Modifies the target On-Demand and target Spot capacities for the instance fleet
        with the specified InstanceFleetID within the cluster specified using
        ClusterID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.modify_instance_fleet)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#modify_instance_fleet)
        """

    def modify_instance_groups(
        self, **kwargs: Unpack[ModifyInstanceGroupsInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        ModifyInstanceGroups modifies the number of nodes and configuration settings of
        an instance
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.modify_instance_groups)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#modify_instance_groups)
        """

    def put_auto_scaling_policy(
        self, **kwargs: Unpack[PutAutoScalingPolicyInputRequestTypeDef]
    ) -> PutAutoScalingPolicyOutputTypeDef:
        """
        Creates or updates an automatic scaling policy for a core instance group or
        task instance group in an Amazon EMR
        cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.put_auto_scaling_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#put_auto_scaling_policy)
        """

    def put_auto_termination_policy(
        self, **kwargs: Unpack[PutAutoTerminationPolicyInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.put_auto_termination_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#put_auto_termination_policy)
        """

    def put_block_public_access_configuration(
        self, **kwargs: Unpack[PutBlockPublicAccessConfigurationInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates or updates an Amazon EMR block public access configuration for your
        Amazon Web Services account in the current
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.put_block_public_access_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#put_block_public_access_configuration)
        """

    def put_managed_scaling_policy(
        self, **kwargs: Unpack[PutManagedScalingPolicyInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates or updates a managed scaling policy for an Amazon EMR cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.put_managed_scaling_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#put_managed_scaling_policy)
        """

    def remove_auto_scaling_policy(
        self, **kwargs: Unpack[RemoveAutoScalingPolicyInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes an automatic scaling policy from a specified instance group within an
        Amazon EMR
        cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.remove_auto_scaling_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#remove_auto_scaling_policy)
        """

    def remove_auto_termination_policy(
        self, **kwargs: Unpack[RemoveAutoTerminationPolicyInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes an auto-termination policy from an Amazon EMR cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.remove_auto_termination_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#remove_auto_termination_policy)
        """

    def remove_managed_scaling_policy(
        self, **kwargs: Unpack[RemoveManagedScalingPolicyInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a managed scaling policy from a specified Amazon EMR cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.remove_managed_scaling_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#remove_managed_scaling_policy)
        """

    def remove_tags(self, **kwargs: Unpack[RemoveTagsInputRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes tags from an Amazon EMR resource, such as a cluster or Amazon EMR
        Studio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.remove_tags)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#remove_tags)
        """

    def run_job_flow(
        self, **kwargs: Unpack[RunJobFlowInputRequestTypeDef]
    ) -> RunJobFlowOutputTypeDef:
        """
        RunJobFlow creates and starts running a new cluster (job flow).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.run_job_flow)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#run_job_flow)
        """

    def set_keep_job_flow_alive_when_no_steps(
        self, **kwargs: Unpack[SetKeepJobFlowAliveWhenNoStepsInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        You can use the `SetKeepJobFlowAliveWhenNoSteps` to configure a cluster (job
        flow) to terminate after the step execution, i.e., all your steps are
        executed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.set_keep_job_flow_alive_when_no_steps)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#set_keep_job_flow_alive_when_no_steps)
        """

    def set_termination_protection(
        self, **kwargs: Unpack[SetTerminationProtectionInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        SetTerminationProtection locks a cluster (job flow) so the Amazon EC2 instances
        in the cluster cannot be terminated by user intervention, an API call, or in
        the event of a job-flow
        error.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.set_termination_protection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#set_termination_protection)
        """

    def set_unhealthy_node_replacement(
        self, **kwargs: Unpack[SetUnhealthyNodeReplacementInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Specify whether to enable unhealthy node replacement, which lets Amazon EMR
        gracefully replace core nodes on a cluster if any nodes become
        unhealthy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.set_unhealthy_node_replacement)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#set_unhealthy_node_replacement)
        """

    def set_visible_to_all_users(
        self, **kwargs: Unpack[SetVisibleToAllUsersInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.set_visible_to_all_users)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#set_visible_to_all_users)
        """

    def start_notebook_execution(
        self, **kwargs: Unpack[StartNotebookExecutionInputRequestTypeDef]
    ) -> StartNotebookExecutionOutputTypeDef:
        """
        Starts a notebook execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.start_notebook_execution)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#start_notebook_execution)
        """

    def stop_notebook_execution(
        self, **kwargs: Unpack[StopNotebookExecutionInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stops a notebook execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.stop_notebook_execution)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#stop_notebook_execution)
        """

    def terminate_job_flows(
        self, **kwargs: Unpack[TerminateJobFlowsInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        TerminateJobFlows shuts a list of clusters (job flows) down.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.terminate_job_flows)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#terminate_job_flows)
        """

    def update_studio(
        self, **kwargs: Unpack[UpdateStudioInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates an Amazon EMR Studio configuration, including attributes such as name,
        description, and
        subnets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.update_studio)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#update_studio)
        """

    def update_studio_session_mapping(
        self, **kwargs: Unpack[UpdateStudioSessionMappingInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the session policy attached to the user or group for the specified
        Amazon EMR
        Studio.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.update_studio_session_mapping)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#update_studio_session_mapping)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_bootstrap_actions"]
    ) -> ListBootstrapActionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_clusters"]) -> ListClustersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_instance_fleets"]
    ) -> ListInstanceFleetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_instance_groups"]
    ) -> ListInstanceGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_instances"]) -> ListInstancesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_notebook_executions"]
    ) -> ListNotebookExecutionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_security_configurations"]
    ) -> ListSecurityConfigurationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_steps"]) -> ListStepsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_studio_session_mappings"]
    ) -> ListStudioSessionMappingsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_studios"]) -> ListStudiosPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#get_paginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["cluster_running"]) -> ClusterRunningWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["cluster_terminated"]) -> ClusterTerminatedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["step_complete"]) -> StepCompleteWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/client/#get_waiter)
        """

# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = [
    'GetInfrastructureResult',
    'AwaitableGetInfrastructureResult',
    'get_infrastructure',
    'get_infrastructure_output',
]

@pulumi.output_type
class GetInfrastructureResult:
    """
    A collection of values returned by getInfrastructure.
    """
    def __init__(__self__, deployment_type=None, description=None, env_id=None, git_details=None, id=None, identifier=None, name=None, org_id=None, project_id=None, tags=None, type=None, yaml=None):
        if deployment_type and not isinstance(deployment_type, str):
            raise TypeError("Expected argument 'deployment_type' to be a str")
        pulumi.set(__self__, "deployment_type", deployment_type)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if env_id and not isinstance(env_id, str):
            raise TypeError("Expected argument 'env_id' to be a str")
        pulumi.set(__self__, "env_id", env_id)
        if git_details and not isinstance(git_details, dict):
            raise TypeError("Expected argument 'git_details' to be a dict")
        pulumi.set(__self__, "git_details", git_details)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identifier and not isinstance(identifier, str):
            raise TypeError("Expected argument 'identifier' to be a str")
        pulumi.set(__self__, "identifier", identifier)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if org_id and not isinstance(org_id, str):
            raise TypeError("Expected argument 'org_id' to be a str")
        pulumi.set(__self__, "org_id", org_id)
        if project_id and not isinstance(project_id, str):
            raise TypeError("Expected argument 'project_id' to be a str")
        pulumi.set(__self__, "project_id", project_id)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if yaml and not isinstance(yaml, str):
            raise TypeError("Expected argument 'yaml' to be a str")
        pulumi.set(__self__, "yaml", yaml)

    @property
    @pulumi.getter(name="deploymentType")
    def deployment_type(self) -> str:
        """
        Infrastructure deployment type. Valid values are Kubernetes, NativeHelm, Ssh, WinRm, ServerlessAwsLambda, AzureWebApp, Custom, ECS.
        """
        return pulumi.get(self, "deployment_type")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Description of the resource.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="envId")
    def env_id(self) -> str:
        """
        environment identifier.
        """
        return pulumi.get(self, "env_id")

    @property
    @pulumi.getter(name="gitDetails")
    def git_details(self) -> 'outputs.GetInfrastructureGitDetailsResult':
        return pulumi.get(self, "git_details")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identifier(self) -> str:
        """
        Unique identifier of the resource.
        """
        return pulumi.get(self, "identifier")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> Optional[str]:
        """
        Unique identifier of the organization.
        """
        return pulumi.get(self, "org_id")

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> Optional[str]:
        """
        Unique identifier of the project.
        """
        return pulumi.get(self, "project_id")

    @property
    @pulumi.getter
    def tags(self) -> Sequence[str]:
        """
        Tags to associate with the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of Infrastructure. Valid values are KubernetesDirect, KubernetesGcp, ServerlessAwsLambda, Pdc, KubernetesAzure, SshWinRmAzure, SshWinRmAws, AzureWebApp, ECS, GitOps, CustomDeployment, TAS, KubernetesRancher, AWS_SAM.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def yaml(self) -> str:
        """
        Infrastructure YAML
        """
        return pulumi.get(self, "yaml")


class AwaitableGetInfrastructureResult(GetInfrastructureResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetInfrastructureResult(
            deployment_type=self.deployment_type,
            description=self.description,
            env_id=self.env_id,
            git_details=self.git_details,
            id=self.id,
            identifier=self.identifier,
            name=self.name,
            org_id=self.org_id,
            project_id=self.project_id,
            tags=self.tags,
            type=self.type,
            yaml=self.yaml)


def get_infrastructure(env_id: Optional[str] = None,
                       git_details: Optional[Union['GetInfrastructureGitDetailsArgs', 'GetInfrastructureGitDetailsArgsDict']] = None,
                       identifier: Optional[str] = None,
                       name: Optional[str] = None,
                       org_id: Optional[str] = None,
                       project_id: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetInfrastructureResult:
    """
    Data source for retrieving a Harness Infrastructure.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_harness as harness

    example = harness.platform.get_infrastructure(identifier="identifier",
        name="name",
        org_id="org_id",
        project_id="project_id",
        env_id="env_id")
    ```


    :param str env_id: environment identifier.
    :param str identifier: Unique identifier of the resource.
    :param str name: Name of the resource.
    :param str org_id: Unique identifier of the organization.
    :param str project_id: Unique identifier of the project.
    """
    __args__ = dict()
    __args__['envId'] = env_id
    __args__['gitDetails'] = git_details
    __args__['identifier'] = identifier
    __args__['name'] = name
    __args__['orgId'] = org_id
    __args__['projectId'] = project_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('harness:platform/getInfrastructure:getInfrastructure', __args__, opts=opts, typ=GetInfrastructureResult).value

    return AwaitableGetInfrastructureResult(
        deployment_type=pulumi.get(__ret__, 'deployment_type'),
        description=pulumi.get(__ret__, 'description'),
        env_id=pulumi.get(__ret__, 'env_id'),
        git_details=pulumi.get(__ret__, 'git_details'),
        id=pulumi.get(__ret__, 'id'),
        identifier=pulumi.get(__ret__, 'identifier'),
        name=pulumi.get(__ret__, 'name'),
        org_id=pulumi.get(__ret__, 'org_id'),
        project_id=pulumi.get(__ret__, 'project_id'),
        tags=pulumi.get(__ret__, 'tags'),
        type=pulumi.get(__ret__, 'type'),
        yaml=pulumi.get(__ret__, 'yaml'))


@_utilities.lift_output_func(get_infrastructure)
def get_infrastructure_output(env_id: Optional[pulumi.Input[str]] = None,
                              git_details: Optional[pulumi.Input[Optional[Union['GetInfrastructureGitDetailsArgs', 'GetInfrastructureGitDetailsArgsDict']]]] = None,
                              identifier: Optional[pulumi.Input[str]] = None,
                              name: Optional[pulumi.Input[Optional[str]]] = None,
                              org_id: Optional[pulumi.Input[Optional[str]]] = None,
                              project_id: Optional[pulumi.Input[Optional[str]]] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetInfrastructureResult]:
    """
    Data source for retrieving a Harness Infrastructure.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_harness as harness

    example = harness.platform.get_infrastructure(identifier="identifier",
        name="name",
        org_id="org_id",
        project_id="project_id",
        env_id="env_id")
    ```


    :param str env_id: environment identifier.
    :param str identifier: Unique identifier of the resource.
    :param str name: Name of the resource.
    :param str org_id: Unique identifier of the organization.
    :param str project_id: Unique identifier of the project.
    """
    ...

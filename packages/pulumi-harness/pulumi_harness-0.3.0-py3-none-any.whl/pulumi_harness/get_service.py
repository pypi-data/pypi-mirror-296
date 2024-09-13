# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = [
    'GetServiceResult',
    'AwaitableGetServiceResult',
    'get_service',
    'get_service_output',
]

@pulumi.output_type
class GetServiceResult:
    """
    A collection of values returned by getService.
    """
    def __init__(__self__, app_id=None, artifact_type=None, description=None, helm_version=None, id=None, name=None, tags=None, template_uri=None, type=None):
        if app_id and not isinstance(app_id, str):
            raise TypeError("Expected argument 'app_id' to be a str")
        pulumi.set(__self__, "app_id", app_id)
        if artifact_type and not isinstance(artifact_type, str):
            raise TypeError("Expected argument 'artifact_type' to be a str")
        pulumi.set(__self__, "artifact_type", artifact_type)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if helm_version and not isinstance(helm_version, str):
            raise TypeError("Expected argument 'helm_version' to be a str")
        pulumi.set(__self__, "helm_version", helm_version)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if template_uri and not isinstance(template_uri, str):
            raise TypeError("Expected argument 'template_uri' to be a str")
        pulumi.set(__self__, "template_uri", template_uri)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="appId")
    def app_id(self) -> str:
        """
        The id of the application the service belongs to
        """
        return pulumi.get(self, "app_id")

    @property
    @pulumi.getter(name="artifactType")
    def artifact_type(self) -> str:
        """
        The type of artifact deployed by the service
        """
        return pulumi.get(self, "artifact_type")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        The application description
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="helmVersion")
    def helm_version(self) -> str:
        """
        The version of Helm being used by the service.
        """
        return pulumi.get(self, "helm_version")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Unique identifier of the application
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the service
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        Tags for the service
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="templateUri")
    def template_uri(self) -> str:
        """
        The path of the template used for the custom deployment
        """
        return pulumi.get(self, "template_uri")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the deployment
        """
        return pulumi.get(self, "type")


class AwaitableGetServiceResult(GetServiceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetServiceResult(
            app_id=self.app_id,
            artifact_type=self.artifact_type,
            description=self.description,
            helm_version=self.helm_version,
            id=self.id,
            name=self.name,
            tags=self.tags,
            template_uri=self.template_uri,
            type=self.type)


def get_service(app_id: Optional[str] = None,
                id: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetServiceResult:
    """
    Data source for retrieving a Harness service


    :param str app_id: The id of the application the service belongs to
    :param str id: Unique identifier of the application
    """
    __args__ = dict()
    __args__['appId'] = app_id
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('harness:index/getService:getService', __args__, opts=opts, typ=GetServiceResult).value

    return AwaitableGetServiceResult(
        app_id=pulumi.get(__ret__, 'app_id'),
        artifact_type=pulumi.get(__ret__, 'artifact_type'),
        description=pulumi.get(__ret__, 'description'),
        helm_version=pulumi.get(__ret__, 'helm_version'),
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'),
        tags=pulumi.get(__ret__, 'tags'),
        template_uri=pulumi.get(__ret__, 'template_uri'),
        type=pulumi.get(__ret__, 'type'))


@_utilities.lift_output_func(get_service)
def get_service_output(app_id: Optional[pulumi.Input[str]] = None,
                       id: Optional[pulumi.Input[str]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetServiceResult]:
    """
    Data source for retrieving a Harness service


    :param str app_id: The id of the application the service belongs to
    :param str id: Unique identifier of the application
    """
    ...

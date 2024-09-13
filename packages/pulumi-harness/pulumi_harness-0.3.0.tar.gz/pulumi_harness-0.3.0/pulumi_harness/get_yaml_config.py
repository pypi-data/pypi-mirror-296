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
    'GetYamlConfigResult',
    'AwaitableGetYamlConfigResult',
    'get_yaml_config',
    'get_yaml_config_output',
]

@pulumi.output_type
class GetYamlConfigResult:
    """
    A collection of values returned by getYamlConfig.
    """
    def __init__(__self__, app_id=None, content=None, id=None, name=None, path=None):
        if app_id and not isinstance(app_id, str):
            raise TypeError("Expected argument 'app_id' to be a str")
        pulumi.set(__self__, "app_id", app_id)
        if content and not isinstance(content, str):
            raise TypeError("Expected argument 'content' to be a str")
        pulumi.set(__self__, "content", content)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if path and not isinstance(path, str):
            raise TypeError("Expected argument 'path' to be a str")
        pulumi.set(__self__, "path", path)

    @property
    @pulumi.getter(name="appId")
    def app_id(self) -> Optional[str]:
        """
        Unique identifier of the application. This is not required for account level resources (i.e. cloud providers, connectors, etc.).
        """
        return pulumi.get(self, "app_id")

    @property
    @pulumi.getter
    def content(self) -> str:
        """
        Content of the yaml file.
        """
        return pulumi.get(self, "content")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Unique identifier of the yaml resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the yaml resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def path(self) -> str:
        """
        Path to the yaml file.
        """
        return pulumi.get(self, "path")


class AwaitableGetYamlConfigResult(GetYamlConfigResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetYamlConfigResult(
            app_id=self.app_id,
            content=self.content,
            id=self.id,
            name=self.name,
            path=self.path)


def get_yaml_config(app_id: Optional[str] = None,
                    path: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetYamlConfigResult:
    """
    Data source for retrieving a yaml config.


    :param str app_id: Unique identifier of the application. This is not required for account level resources (i.e. cloud providers, connectors, etc.).
    :param str path: Path to the yaml file.
    """
    __args__ = dict()
    __args__['appId'] = app_id
    __args__['path'] = path
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('harness:index/getYamlConfig:getYamlConfig', __args__, opts=opts, typ=GetYamlConfigResult).value

    return AwaitableGetYamlConfigResult(
        app_id=pulumi.get(__ret__, 'app_id'),
        content=pulumi.get(__ret__, 'content'),
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'),
        path=pulumi.get(__ret__, 'path'))


@_utilities.lift_output_func(get_yaml_config)
def get_yaml_config_output(app_id: Optional[pulumi.Input[Optional[str]]] = None,
                           path: Optional[pulumi.Input[str]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetYamlConfigResult]:
    """
    Data source for retrieving a yaml config.


    :param str app_id: Unique identifier of the application. This is not required for account level resources (i.e. cloud providers, connectors, etc.).
    :param str path: Path to the yaml file.
    """
    ...

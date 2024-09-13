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

__all__ = [
    'GetManualFreezeResult',
    'AwaitableGetManualFreezeResult',
    'get_manual_freeze',
    'get_manual_freeze_output',
]

@pulumi.output_type
class GetManualFreezeResult:
    """
    A collection of values returned by getManualFreeze.
    """
    def __init__(__self__, account_id=None, current_or_upcoming_windows=None, description=None, freeze_windows=None, id=None, identifier=None, name=None, org_id=None, project_id=None, scope=None, status=None, tags=None, type=None, yaml=None):
        if account_id and not isinstance(account_id, str):
            raise TypeError("Expected argument 'account_id' to be a str")
        pulumi.set(__self__, "account_id", account_id)
        if current_or_upcoming_windows and not isinstance(current_or_upcoming_windows, list):
            raise TypeError("Expected argument 'current_or_upcoming_windows' to be a list")
        pulumi.set(__self__, "current_or_upcoming_windows", current_or_upcoming_windows)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if freeze_windows and not isinstance(freeze_windows, list):
            raise TypeError("Expected argument 'freeze_windows' to be a list")
        pulumi.set(__self__, "freeze_windows", freeze_windows)
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
        if scope and not isinstance(scope, str):
            raise TypeError("Expected argument 'scope' to be a str")
        pulumi.set(__self__, "scope", scope)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
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
    @pulumi.getter(name="accountId")
    def account_id(self) -> str:
        """
        Account Identifier of the freeze
        """
        return pulumi.get(self, "account_id")

    @property
    @pulumi.getter(name="currentOrUpcomingWindows")
    def current_or_upcoming_windows(self) -> Sequence['outputs.GetManualFreezeCurrentOrUpcomingWindowResult']:
        """
        Current or upcoming windows
        """
        return pulumi.get(self, "current_or_upcoming_windows")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Description of the freeze
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="freezeWindows")
    def freeze_windows(self) -> Sequence['outputs.GetManualFreezeFreezeWindowResult']:
        """
        Freeze windows in the freeze response
        """
        return pulumi.get(self, "freeze_windows")

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
        Identifier of the freeze
        """
        return pulumi.get(self, "identifier")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the freeze
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> Optional[str]:
        """
        Organization identifier of the freeze
        """
        return pulumi.get(self, "org_id")

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> Optional[str]:
        """
        Project identifier of the freeze
        """
        return pulumi.get(self, "project_id")

    @property
    @pulumi.getter
    def scope(self) -> str:
        """
        Scope of the freeze
        """
        return pulumi.get(self, "scope")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Status of the freeze
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> Sequence[str]:
        """
        Tags associated with the freeze
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of freeze
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def yaml(self) -> str:
        """
        Yaml of the freeze
        """
        return pulumi.get(self, "yaml")


class AwaitableGetManualFreezeResult(GetManualFreezeResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetManualFreezeResult(
            account_id=self.account_id,
            current_or_upcoming_windows=self.current_or_upcoming_windows,
            description=self.description,
            freeze_windows=self.freeze_windows,
            id=self.id,
            identifier=self.identifier,
            name=self.name,
            org_id=self.org_id,
            project_id=self.project_id,
            scope=self.scope,
            status=self.status,
            tags=self.tags,
            type=self.type,
            yaml=self.yaml)


def get_manual_freeze(account_id: Optional[str] = None,
                      identifier: Optional[str] = None,
                      org_id: Optional[str] = None,
                      project_id: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetManualFreezeResult:
    """
    DataSource for deployment freeze in harness.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_harness as harness

    example = harness.platform.get_manual_freeze(identifier="identifier",
        org_id="org_id",
        project_id="project_id",
        account_id="account_id")
    ```


    :param str account_id: Account Identifier of the freeze
    :param str identifier: Identifier of the freeze
    :param str org_id: Organization identifier of the freeze
    :param str project_id: Project identifier of the freeze
    """
    __args__ = dict()
    __args__['accountId'] = account_id
    __args__['identifier'] = identifier
    __args__['orgId'] = org_id
    __args__['projectId'] = project_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('harness:platform/getManualFreeze:getManualFreeze', __args__, opts=opts, typ=GetManualFreezeResult).value

    return AwaitableGetManualFreezeResult(
        account_id=pulumi.get(__ret__, 'account_id'),
        current_or_upcoming_windows=pulumi.get(__ret__, 'current_or_upcoming_windows'),
        description=pulumi.get(__ret__, 'description'),
        freeze_windows=pulumi.get(__ret__, 'freeze_windows'),
        id=pulumi.get(__ret__, 'id'),
        identifier=pulumi.get(__ret__, 'identifier'),
        name=pulumi.get(__ret__, 'name'),
        org_id=pulumi.get(__ret__, 'org_id'),
        project_id=pulumi.get(__ret__, 'project_id'),
        scope=pulumi.get(__ret__, 'scope'),
        status=pulumi.get(__ret__, 'status'),
        tags=pulumi.get(__ret__, 'tags'),
        type=pulumi.get(__ret__, 'type'),
        yaml=pulumi.get(__ret__, 'yaml'))


@_utilities.lift_output_func(get_manual_freeze)
def get_manual_freeze_output(account_id: Optional[pulumi.Input[str]] = None,
                             identifier: Optional[pulumi.Input[str]] = None,
                             org_id: Optional[pulumi.Input[Optional[str]]] = None,
                             project_id: Optional[pulumi.Input[Optional[str]]] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetManualFreezeResult]:
    """
    DataSource for deployment freeze in harness.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_harness as harness

    example = harness.platform.get_manual_freeze(identifier="identifier",
        org_id="org_id",
        project_id="project_id",
        account_id="account_id")
    ```


    :param str account_id: Account Identifier of the freeze
    :param str identifier: Identifier of the freeze
    :param str org_id: Organization identifier of the freeze
    :param str project_id: Project identifier of the freeze
    """
    ...

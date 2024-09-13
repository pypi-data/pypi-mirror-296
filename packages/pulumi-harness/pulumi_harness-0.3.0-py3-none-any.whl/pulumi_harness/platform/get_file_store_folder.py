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
    'GetFileStoreFolderResult',
    'AwaitableGetFileStoreFolderResult',
    'get_file_store_folder',
    'get_file_store_folder_output',
]

@pulumi.output_type
class GetFileStoreFolderResult:
    """
    A collection of values returned by getFileStoreFolder.
    """
    def __init__(__self__, created_bies=None, description=None, id=None, identifier=None, last_modified_at=None, last_modified_bies=None, name=None, org_id=None, parent_identifier=None, path=None, project_id=None, tags=None):
        if created_bies and not isinstance(created_bies, list):
            raise TypeError("Expected argument 'created_bies' to be a list")
        pulumi.set(__self__, "created_bies", created_bies)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identifier and not isinstance(identifier, str):
            raise TypeError("Expected argument 'identifier' to be a str")
        pulumi.set(__self__, "identifier", identifier)
        if last_modified_at and not isinstance(last_modified_at, int):
            raise TypeError("Expected argument 'last_modified_at' to be a int")
        pulumi.set(__self__, "last_modified_at", last_modified_at)
        if last_modified_bies and not isinstance(last_modified_bies, list):
            raise TypeError("Expected argument 'last_modified_bies' to be a list")
        pulumi.set(__self__, "last_modified_bies", last_modified_bies)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if org_id and not isinstance(org_id, str):
            raise TypeError("Expected argument 'org_id' to be a str")
        pulumi.set(__self__, "org_id", org_id)
        if parent_identifier and not isinstance(parent_identifier, str):
            raise TypeError("Expected argument 'parent_identifier' to be a str")
        pulumi.set(__self__, "parent_identifier", parent_identifier)
        if path and not isinstance(path, str):
            raise TypeError("Expected argument 'path' to be a str")
        pulumi.set(__self__, "path", path)
        if project_id and not isinstance(project_id, str):
            raise TypeError("Expected argument 'project_id' to be a str")
        pulumi.set(__self__, "project_id", project_id)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="createdBies")
    def created_bies(self) -> Sequence['outputs.GetFileStoreFolderCreatedByResult']:
        """
        Created by
        """
        return pulumi.get(self, "created_bies")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Description of the resource.
        """
        return pulumi.get(self, "description")

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
    @pulumi.getter(name="lastModifiedAt")
    def last_modified_at(self) -> int:
        """
        Last modified at
        """
        return pulumi.get(self, "last_modified_at")

    @property
    @pulumi.getter(name="lastModifiedBies")
    def last_modified_bies(self) -> Sequence['outputs.GetFileStoreFolderLastModifiedByResult']:
        """
        Last modified by
        """
        return pulumi.get(self, "last_modified_bies")

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
    @pulumi.getter(name="parentIdentifier")
    def parent_identifier(self) -> str:
        """
        Folder parent identifier on Harness File Store
        """
        return pulumi.get(self, "parent_identifier")

    @property
    @pulumi.getter
    def path(self) -> str:
        """
        Harness File Store folder path
        """
        return pulumi.get(self, "path")

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


class AwaitableGetFileStoreFolderResult(GetFileStoreFolderResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetFileStoreFolderResult(
            created_bies=self.created_bies,
            description=self.description,
            id=self.id,
            identifier=self.identifier,
            last_modified_at=self.last_modified_at,
            last_modified_bies=self.last_modified_bies,
            name=self.name,
            org_id=self.org_id,
            parent_identifier=self.parent_identifier,
            path=self.path,
            project_id=self.project_id,
            tags=self.tags)


def get_file_store_folder(identifier: Optional[str] = None,
                          name: Optional[str] = None,
                          org_id: Optional[str] = None,
                          project_id: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetFileStoreFolderResult:
    """
    Data source for retrieving folders.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_harness as harness

    example = harness.platform.get_file_store_folder(identifier="identifier")
    ```


    :param str identifier: Unique identifier of the resource.
    :param str name: Name of the resource.
    :param str org_id: Unique identifier of the organization.
    :param str project_id: Unique identifier of the project.
    """
    __args__ = dict()
    __args__['identifier'] = identifier
    __args__['name'] = name
    __args__['orgId'] = org_id
    __args__['projectId'] = project_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('harness:platform/getFileStoreFolder:getFileStoreFolder', __args__, opts=opts, typ=GetFileStoreFolderResult).value

    return AwaitableGetFileStoreFolderResult(
        created_bies=pulumi.get(__ret__, 'created_bies'),
        description=pulumi.get(__ret__, 'description'),
        id=pulumi.get(__ret__, 'id'),
        identifier=pulumi.get(__ret__, 'identifier'),
        last_modified_at=pulumi.get(__ret__, 'last_modified_at'),
        last_modified_bies=pulumi.get(__ret__, 'last_modified_bies'),
        name=pulumi.get(__ret__, 'name'),
        org_id=pulumi.get(__ret__, 'org_id'),
        parent_identifier=pulumi.get(__ret__, 'parent_identifier'),
        path=pulumi.get(__ret__, 'path'),
        project_id=pulumi.get(__ret__, 'project_id'),
        tags=pulumi.get(__ret__, 'tags'))


@_utilities.lift_output_func(get_file_store_folder)
def get_file_store_folder_output(identifier: Optional[pulumi.Input[str]] = None,
                                 name: Optional[pulumi.Input[Optional[str]]] = None,
                                 org_id: Optional[pulumi.Input[Optional[str]]] = None,
                                 project_id: Optional[pulumi.Input[Optional[str]]] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetFileStoreFolderResult]:
    """
    Data source for retrieving folders.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_harness as harness

    example = harness.platform.get_file_store_folder(identifier="identifier")
    ```


    :param str identifier: Unique identifier of the resource.
    :param str name: Name of the resource.
    :param str org_id: Unique identifier of the organization.
    :param str project_id: Unique identifier of the project.
    """
    ...

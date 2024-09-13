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

__all__ = ['ArtifactoryConnectorArgs', 'ArtifactoryConnector']

@pulumi.input_type
class ArtifactoryConnectorArgs:
    def __init__(__self__, *,
                 identifier: pulumi.Input[str],
                 url: pulumi.Input[str],
                 credentials: Optional[pulumi.Input['ArtifactoryConnectorCredentialsArgs']] = None,
                 delegate_selectors: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a ArtifactoryConnector resource.
        :param pulumi.Input[str] identifier: Unique identifier of the resource.
        :param pulumi.Input[str] url: URL of the Artifactory server.
        :param pulumi.Input['ArtifactoryConnectorCredentialsArgs'] credentials: Credentials to use for authentication.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] delegate_selectors: Tags to filter delegates for connection.
        :param pulumi.Input[str] description: Description of the resource.
        :param pulumi.Input[str] name: Name of the resource.
        :param pulumi.Input[str] org_id: Unique identifier of the organization.
        :param pulumi.Input[str] project_id: Unique identifier of the project.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: Tags to associate with the resource.
        """
        pulumi.set(__self__, "identifier", identifier)
        pulumi.set(__self__, "url", url)
        if credentials is not None:
            pulumi.set(__self__, "credentials", credentials)
        if delegate_selectors is not None:
            pulumi.set(__self__, "delegate_selectors", delegate_selectors)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if org_id is not None:
            pulumi.set(__self__, "org_id", org_id)
        if project_id is not None:
            pulumi.set(__self__, "project_id", project_id)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def identifier(self) -> pulumi.Input[str]:
        """
        Unique identifier of the resource.
        """
        return pulumi.get(self, "identifier")

    @identifier.setter
    def identifier(self, value: pulumi.Input[str]):
        pulumi.set(self, "identifier", value)

    @property
    @pulumi.getter
    def url(self) -> pulumi.Input[str]:
        """
        URL of the Artifactory server.
        """
        return pulumi.get(self, "url")

    @url.setter
    def url(self, value: pulumi.Input[str]):
        pulumi.set(self, "url", value)

    @property
    @pulumi.getter
    def credentials(self) -> Optional[pulumi.Input['ArtifactoryConnectorCredentialsArgs']]:
        """
        Credentials to use for authentication.
        """
        return pulumi.get(self, "credentials")

    @credentials.setter
    def credentials(self, value: Optional[pulumi.Input['ArtifactoryConnectorCredentialsArgs']]):
        pulumi.set(self, "credentials", value)

    @property
    @pulumi.getter(name="delegateSelectors")
    def delegate_selectors(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Tags to filter delegates for connection.
        """
        return pulumi.get(self, "delegate_selectors")

    @delegate_selectors.setter
    def delegate_selectors(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "delegate_selectors", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the resource.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the resource.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> Optional[pulumi.Input[str]]:
        """
        Unique identifier of the organization.
        """
        return pulumi.get(self, "org_id")

    @org_id.setter
    def org_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "org_id", value)

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> Optional[pulumi.Input[str]]:
        """
        Unique identifier of the project.
        """
        return pulumi.get(self, "project_id")

    @project_id.setter
    def project_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project_id", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Tags to associate with the resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _ArtifactoryConnectorState:
    def __init__(__self__, *,
                 credentials: Optional[pulumi.Input['ArtifactoryConnectorCredentialsArgs']] = None,
                 delegate_selectors: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 identifier: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 url: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ArtifactoryConnector resources.
        :param pulumi.Input['ArtifactoryConnectorCredentialsArgs'] credentials: Credentials to use for authentication.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] delegate_selectors: Tags to filter delegates for connection.
        :param pulumi.Input[str] description: Description of the resource.
        :param pulumi.Input[str] identifier: Unique identifier of the resource.
        :param pulumi.Input[str] name: Name of the resource.
        :param pulumi.Input[str] org_id: Unique identifier of the organization.
        :param pulumi.Input[str] project_id: Unique identifier of the project.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: Tags to associate with the resource.
        :param pulumi.Input[str] url: URL of the Artifactory server.
        """
        if credentials is not None:
            pulumi.set(__self__, "credentials", credentials)
        if delegate_selectors is not None:
            pulumi.set(__self__, "delegate_selectors", delegate_selectors)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if identifier is not None:
            pulumi.set(__self__, "identifier", identifier)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if org_id is not None:
            pulumi.set(__self__, "org_id", org_id)
        if project_id is not None:
            pulumi.set(__self__, "project_id", project_id)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if url is not None:
            pulumi.set(__self__, "url", url)

    @property
    @pulumi.getter
    def credentials(self) -> Optional[pulumi.Input['ArtifactoryConnectorCredentialsArgs']]:
        """
        Credentials to use for authentication.
        """
        return pulumi.get(self, "credentials")

    @credentials.setter
    def credentials(self, value: Optional[pulumi.Input['ArtifactoryConnectorCredentialsArgs']]):
        pulumi.set(self, "credentials", value)

    @property
    @pulumi.getter(name="delegateSelectors")
    def delegate_selectors(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Tags to filter delegates for connection.
        """
        return pulumi.get(self, "delegate_selectors")

    @delegate_selectors.setter
    def delegate_selectors(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "delegate_selectors", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the resource.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def identifier(self) -> Optional[pulumi.Input[str]]:
        """
        Unique identifier of the resource.
        """
        return pulumi.get(self, "identifier")

    @identifier.setter
    def identifier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "identifier", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the resource.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> Optional[pulumi.Input[str]]:
        """
        Unique identifier of the organization.
        """
        return pulumi.get(self, "org_id")

    @org_id.setter
    def org_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "org_id", value)

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> Optional[pulumi.Input[str]]:
        """
        Unique identifier of the project.
        """
        return pulumi.get(self, "project_id")

    @project_id.setter
    def project_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project_id", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Tags to associate with the resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def url(self) -> Optional[pulumi.Input[str]]:
        """
        URL of the Artifactory server.
        """
        return pulumi.get(self, "url")

    @url.setter
    def url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "url", value)


class ArtifactoryConnector(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 credentials: Optional[pulumi.Input[Union['ArtifactoryConnectorCredentialsArgs', 'ArtifactoryConnectorCredentialsArgsDict']]] = None,
                 delegate_selectors: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 identifier: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 url: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource for creating an Artifactory connector.

        ## Example to create Artifactory Connector at different levels (Org, Project, Account)

        ### Account Level
        ```python
        import pulumi
        import pulumi_harness as harness

        # Authentication mechanism as username and password
        example = harness.platform.ArtifactoryConnector("example",
            identifier="identifier",
            name="name",
            description="test",
            tags=["foo:bar"],
            url="https://artifactory.example.com",
            delegate_selectors=["harness-delegate"],
            credentials={
                "username": "admin",
                "password_ref": "account.secret_id",
            })
        # Authentication mechanism as anonymous
        test = harness.platform.ArtifactoryConnector("test",
            identifier="identifier",
            name="name",
            description="test",
            tags=["foo:bar"],
            url="https://artifactory.example.com",
            delegate_selectors=["harness-delegate"])
        ```

        ### Org Level
        ```python
        import pulumi
        import pulumi_harness as harness

        # Authentication mechanism as username and password
        example = harness.platform.ArtifactoryConnector("example",
            identifier="identifier",
            name="name",
            description="test",
            tags=["foo:bar"],
            org_id=test_harness_platform_project["orgId"],
            url="https://artifactory.example.com",
            delegate_selectors=["harness-delegate"],
            credentials={
                "username": "admin",
                "password_ref": "account.secret_id",
            })
        # Authentication mechanism as anonymous
        test = harness.platform.ArtifactoryConnector("test",
            identifier="identifier",
            name="name",
            description="test",
            tags=["foo:bar"],
            org_id=test_harness_platform_project["orgId"],
            url="https://artifactory.example.com",
            delegate_selectors=["harness-delegate"])
        ```

        ### Project Level
        ```python
        import pulumi
        import pulumi_harness as harness

        # Authentication mechanism as username and password
        example = harness.platform.ArtifactoryConnector("example",
            identifier="identifier",
            name="name",
            description="test",
            tags=["foo:bar"],
            org_id=test_harness_platform_project["orgId"],
            project_id=test_harness_platform_project["id"],
            url="https://artifactory.example.com",
            delegate_selectors=["harness-delegate"],
            credentials={
                "username": "admin",
                "password_ref": "account.secret_id",
            })
        # Authentication mechanism as anonymous
        test = harness.platform.ArtifactoryConnector("test",
            identifier="identifier",
            name="name",
            description="test",
            tags=["foo:bar"],
            org_id=test_harness_platform_project["orgId"],
            project_id=test_harness_platform_project["id"],
            url="https://artifactory.example.com",
            delegate_selectors=["harness-delegate"])
        ```

        ## Import

        Import account level artifactory connector

        ```sh
        $ pulumi import harness:platform/artifactoryConnector:ArtifactoryConnector example <connector_id>
        ```

        Import org level artifactory connector

        ```sh
        $ pulumi import harness:platform/artifactoryConnector:ArtifactoryConnector example <ord_id>/<connector_id>
        ```

        Import project level artifactory connector

        ```sh
        $ pulumi import harness:platform/artifactoryConnector:ArtifactoryConnector example <org_id>/<project_id>/<connector_id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union['ArtifactoryConnectorCredentialsArgs', 'ArtifactoryConnectorCredentialsArgsDict']] credentials: Credentials to use for authentication.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] delegate_selectors: Tags to filter delegates for connection.
        :param pulumi.Input[str] description: Description of the resource.
        :param pulumi.Input[str] identifier: Unique identifier of the resource.
        :param pulumi.Input[str] name: Name of the resource.
        :param pulumi.Input[str] org_id: Unique identifier of the organization.
        :param pulumi.Input[str] project_id: Unique identifier of the project.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: Tags to associate with the resource.
        :param pulumi.Input[str] url: URL of the Artifactory server.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ArtifactoryConnectorArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource for creating an Artifactory connector.

        ## Example to create Artifactory Connector at different levels (Org, Project, Account)

        ### Account Level
        ```python
        import pulumi
        import pulumi_harness as harness

        # Authentication mechanism as username and password
        example = harness.platform.ArtifactoryConnector("example",
            identifier="identifier",
            name="name",
            description="test",
            tags=["foo:bar"],
            url="https://artifactory.example.com",
            delegate_selectors=["harness-delegate"],
            credentials={
                "username": "admin",
                "password_ref": "account.secret_id",
            })
        # Authentication mechanism as anonymous
        test = harness.platform.ArtifactoryConnector("test",
            identifier="identifier",
            name="name",
            description="test",
            tags=["foo:bar"],
            url="https://artifactory.example.com",
            delegate_selectors=["harness-delegate"])
        ```

        ### Org Level
        ```python
        import pulumi
        import pulumi_harness as harness

        # Authentication mechanism as username and password
        example = harness.platform.ArtifactoryConnector("example",
            identifier="identifier",
            name="name",
            description="test",
            tags=["foo:bar"],
            org_id=test_harness_platform_project["orgId"],
            url="https://artifactory.example.com",
            delegate_selectors=["harness-delegate"],
            credentials={
                "username": "admin",
                "password_ref": "account.secret_id",
            })
        # Authentication mechanism as anonymous
        test = harness.platform.ArtifactoryConnector("test",
            identifier="identifier",
            name="name",
            description="test",
            tags=["foo:bar"],
            org_id=test_harness_platform_project["orgId"],
            url="https://artifactory.example.com",
            delegate_selectors=["harness-delegate"])
        ```

        ### Project Level
        ```python
        import pulumi
        import pulumi_harness as harness

        # Authentication mechanism as username and password
        example = harness.platform.ArtifactoryConnector("example",
            identifier="identifier",
            name="name",
            description="test",
            tags=["foo:bar"],
            org_id=test_harness_platform_project["orgId"],
            project_id=test_harness_platform_project["id"],
            url="https://artifactory.example.com",
            delegate_selectors=["harness-delegate"],
            credentials={
                "username": "admin",
                "password_ref": "account.secret_id",
            })
        # Authentication mechanism as anonymous
        test = harness.platform.ArtifactoryConnector("test",
            identifier="identifier",
            name="name",
            description="test",
            tags=["foo:bar"],
            org_id=test_harness_platform_project["orgId"],
            project_id=test_harness_platform_project["id"],
            url="https://artifactory.example.com",
            delegate_selectors=["harness-delegate"])
        ```

        ## Import

        Import account level artifactory connector

        ```sh
        $ pulumi import harness:platform/artifactoryConnector:ArtifactoryConnector example <connector_id>
        ```

        Import org level artifactory connector

        ```sh
        $ pulumi import harness:platform/artifactoryConnector:ArtifactoryConnector example <ord_id>/<connector_id>
        ```

        Import project level artifactory connector

        ```sh
        $ pulumi import harness:platform/artifactoryConnector:ArtifactoryConnector example <org_id>/<project_id>/<connector_id>
        ```

        :param str resource_name: The name of the resource.
        :param ArtifactoryConnectorArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ArtifactoryConnectorArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 credentials: Optional[pulumi.Input[Union['ArtifactoryConnectorCredentialsArgs', 'ArtifactoryConnectorCredentialsArgsDict']]] = None,
                 delegate_selectors: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 identifier: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 url: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ArtifactoryConnectorArgs.__new__(ArtifactoryConnectorArgs)

            __props__.__dict__["credentials"] = credentials
            __props__.__dict__["delegate_selectors"] = delegate_selectors
            __props__.__dict__["description"] = description
            if identifier is None and not opts.urn:
                raise TypeError("Missing required property 'identifier'")
            __props__.__dict__["identifier"] = identifier
            __props__.__dict__["name"] = name
            __props__.__dict__["org_id"] = org_id
            __props__.__dict__["project_id"] = project_id
            __props__.__dict__["tags"] = tags
            if url is None and not opts.urn:
                raise TypeError("Missing required property 'url'")
            __props__.__dict__["url"] = url
        super(ArtifactoryConnector, __self__).__init__(
            'harness:platform/artifactoryConnector:ArtifactoryConnector',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            credentials: Optional[pulumi.Input[Union['ArtifactoryConnectorCredentialsArgs', 'ArtifactoryConnectorCredentialsArgsDict']]] = None,
            delegate_selectors: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            description: Optional[pulumi.Input[str]] = None,
            identifier: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            org_id: Optional[pulumi.Input[str]] = None,
            project_id: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            url: Optional[pulumi.Input[str]] = None) -> 'ArtifactoryConnector':
        """
        Get an existing ArtifactoryConnector resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union['ArtifactoryConnectorCredentialsArgs', 'ArtifactoryConnectorCredentialsArgsDict']] credentials: Credentials to use for authentication.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] delegate_selectors: Tags to filter delegates for connection.
        :param pulumi.Input[str] description: Description of the resource.
        :param pulumi.Input[str] identifier: Unique identifier of the resource.
        :param pulumi.Input[str] name: Name of the resource.
        :param pulumi.Input[str] org_id: Unique identifier of the organization.
        :param pulumi.Input[str] project_id: Unique identifier of the project.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: Tags to associate with the resource.
        :param pulumi.Input[str] url: URL of the Artifactory server.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ArtifactoryConnectorState.__new__(_ArtifactoryConnectorState)

        __props__.__dict__["credentials"] = credentials
        __props__.__dict__["delegate_selectors"] = delegate_selectors
        __props__.__dict__["description"] = description
        __props__.__dict__["identifier"] = identifier
        __props__.__dict__["name"] = name
        __props__.__dict__["org_id"] = org_id
        __props__.__dict__["project_id"] = project_id
        __props__.__dict__["tags"] = tags
        __props__.__dict__["url"] = url
        return ArtifactoryConnector(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def credentials(self) -> pulumi.Output[Optional['outputs.ArtifactoryConnectorCredentials']]:
        """
        Credentials to use for authentication.
        """
        return pulumi.get(self, "credentials")

    @property
    @pulumi.getter(name="delegateSelectors")
    def delegate_selectors(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Tags to filter delegates for connection.
        """
        return pulumi.get(self, "delegate_selectors")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Description of the resource.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def identifier(self) -> pulumi.Output[str]:
        """
        Unique identifier of the resource.
        """
        return pulumi.get(self, "identifier")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> pulumi.Output[Optional[str]]:
        """
        Unique identifier of the organization.
        """
        return pulumi.get(self, "org_id")

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> pulumi.Output[Optional[str]]:
        """
        Unique identifier of the project.
        """
        return pulumi.get(self, "project_id")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Tags to associate with the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def url(self) -> pulumi.Output[str]:
        """
        URL of the Artifactory server.
        """
        return pulumi.get(self, "url")


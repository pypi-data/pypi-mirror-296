# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['FeatureFlagApiKeyArgs', 'FeatureFlagApiKey']

@pulumi.input_type
class FeatureFlagApiKeyArgs:
    def __init__(__self__, *,
                 env_id: pulumi.Input[str],
                 identifier: pulumi.Input[str],
                 org_id: pulumi.Input[str],
                 project_id: pulumi.Input[str],
                 type: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 expired_at: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a FeatureFlagApiKey resource.
        :param pulumi.Input[str] env_id: Environment Identifier
        :param pulumi.Input[str] identifier: Identifier of the SDK API Key
        :param pulumi.Input[str] org_id: Organization Identifier
        :param pulumi.Input[str] project_id: Project Identifier
        :param pulumi.Input[str] type: Type of SDK. Valid values are `Server` or `Client`.
        :param pulumi.Input[str] description: Description of the SDK API Key
        :param pulumi.Input[int] expired_at: Expiration datetime of the SDK API Key
        :param pulumi.Input[str] name: Name of the SDK API Key
        """
        pulumi.set(__self__, "env_id", env_id)
        pulumi.set(__self__, "identifier", identifier)
        pulumi.set(__self__, "org_id", org_id)
        pulumi.set(__self__, "project_id", project_id)
        pulumi.set(__self__, "type", type)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if expired_at is not None:
            pulumi.set(__self__, "expired_at", expired_at)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="envId")
    def env_id(self) -> pulumi.Input[str]:
        """
        Environment Identifier
        """
        return pulumi.get(self, "env_id")

    @env_id.setter
    def env_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "env_id", value)

    @property
    @pulumi.getter
    def identifier(self) -> pulumi.Input[str]:
        """
        Identifier of the SDK API Key
        """
        return pulumi.get(self, "identifier")

    @identifier.setter
    def identifier(self, value: pulumi.Input[str]):
        pulumi.set(self, "identifier", value)

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> pulumi.Input[str]:
        """
        Organization Identifier
        """
        return pulumi.get(self, "org_id")

    @org_id.setter
    def org_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "org_id", value)

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> pulumi.Input[str]:
        """
        Project Identifier
        """
        return pulumi.get(self, "project_id")

    @project_id.setter
    def project_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "project_id", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        Type of SDK. Valid values are `Server` or `Client`.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the SDK API Key
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="expiredAt")
    def expired_at(self) -> Optional[pulumi.Input[int]]:
        """
        Expiration datetime of the SDK API Key
        """
        return pulumi.get(self, "expired_at")

    @expired_at.setter
    def expired_at(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "expired_at", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the SDK API Key
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _FeatureFlagApiKeyState:
    def __init__(__self__, *,
                 api_key: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 env_id: Optional[pulumi.Input[str]] = None,
                 expired_at: Optional[pulumi.Input[int]] = None,
                 identifier: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering FeatureFlagApiKey resources.
        :param pulumi.Input[str] api_key: The value of the SDK API Key
        :param pulumi.Input[str] description: Description of the SDK API Key
        :param pulumi.Input[str] env_id: Environment Identifier
        :param pulumi.Input[int] expired_at: Expiration datetime of the SDK API Key
        :param pulumi.Input[str] identifier: Identifier of the SDK API Key
        :param pulumi.Input[str] name: Name of the SDK API Key
        :param pulumi.Input[str] org_id: Organization Identifier
        :param pulumi.Input[str] project_id: Project Identifier
        :param pulumi.Input[str] type: Type of SDK. Valid values are `Server` or `Client`.
        """
        if api_key is not None:
            pulumi.set(__self__, "api_key", api_key)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if env_id is not None:
            pulumi.set(__self__, "env_id", env_id)
        if expired_at is not None:
            pulumi.set(__self__, "expired_at", expired_at)
        if identifier is not None:
            pulumi.set(__self__, "identifier", identifier)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if org_id is not None:
            pulumi.set(__self__, "org_id", org_id)
        if project_id is not None:
            pulumi.set(__self__, "project_id", project_id)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="apiKey")
    def api_key(self) -> Optional[pulumi.Input[str]]:
        """
        The value of the SDK API Key
        """
        return pulumi.get(self, "api_key")

    @api_key.setter
    def api_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "api_key", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the SDK API Key
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="envId")
    def env_id(self) -> Optional[pulumi.Input[str]]:
        """
        Environment Identifier
        """
        return pulumi.get(self, "env_id")

    @env_id.setter
    def env_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "env_id", value)

    @property
    @pulumi.getter(name="expiredAt")
    def expired_at(self) -> Optional[pulumi.Input[int]]:
        """
        Expiration datetime of the SDK API Key
        """
        return pulumi.get(self, "expired_at")

    @expired_at.setter
    def expired_at(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "expired_at", value)

    @property
    @pulumi.getter
    def identifier(self) -> Optional[pulumi.Input[str]]:
        """
        Identifier of the SDK API Key
        """
        return pulumi.get(self, "identifier")

    @identifier.setter
    def identifier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "identifier", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the SDK API Key
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> Optional[pulumi.Input[str]]:
        """
        Organization Identifier
        """
        return pulumi.get(self, "org_id")

    @org_id.setter
    def org_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "org_id", value)

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> Optional[pulumi.Input[str]]:
        """
        Project Identifier
        """
        return pulumi.get(self, "project_id")

    @project_id.setter
    def project_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project_id", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        Type of SDK. Valid values are `Server` or `Client`.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)


class FeatureFlagApiKey(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 env_id: Optional[pulumi.Input[str]] = None,
                 expired_at: Optional[pulumi.Input[int]] = None,
                 identifier: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource for creating an environment SDK key for Feature Flags.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_harness as harness

        testserverapikey = harness.platform.FeatureFlagApiKey("testserverapikey",
            identifier="testserver",
            name="TestServer",
            description="this is a server SDK key",
            org_id="test",
            project_id="testff",
            env_id="testenv",
            expired_at=1713729225,
            type="Server")
        pulumi.export("serversdkkey", testserverapikey.api_key)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Description of the SDK API Key
        :param pulumi.Input[str] env_id: Environment Identifier
        :param pulumi.Input[int] expired_at: Expiration datetime of the SDK API Key
        :param pulumi.Input[str] identifier: Identifier of the SDK API Key
        :param pulumi.Input[str] name: Name of the SDK API Key
        :param pulumi.Input[str] org_id: Organization Identifier
        :param pulumi.Input[str] project_id: Project Identifier
        :param pulumi.Input[str] type: Type of SDK. Valid values are `Server` or `Client`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: FeatureFlagApiKeyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource for creating an environment SDK key for Feature Flags.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_harness as harness

        testserverapikey = harness.platform.FeatureFlagApiKey("testserverapikey",
            identifier="testserver",
            name="TestServer",
            description="this is a server SDK key",
            org_id="test",
            project_id="testff",
            env_id="testenv",
            expired_at=1713729225,
            type="Server")
        pulumi.export("serversdkkey", testserverapikey.api_key)
        ```

        :param str resource_name: The name of the resource.
        :param FeatureFlagApiKeyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(FeatureFlagApiKeyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 env_id: Optional[pulumi.Input[str]] = None,
                 expired_at: Optional[pulumi.Input[int]] = None,
                 identifier: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = FeatureFlagApiKeyArgs.__new__(FeatureFlagApiKeyArgs)

            __props__.__dict__["description"] = description
            if env_id is None and not opts.urn:
                raise TypeError("Missing required property 'env_id'")
            __props__.__dict__["env_id"] = env_id
            __props__.__dict__["expired_at"] = expired_at
            if identifier is None and not opts.urn:
                raise TypeError("Missing required property 'identifier'")
            __props__.__dict__["identifier"] = identifier
            __props__.__dict__["name"] = name
            if org_id is None and not opts.urn:
                raise TypeError("Missing required property 'org_id'")
            __props__.__dict__["org_id"] = org_id
            if project_id is None and not opts.urn:
                raise TypeError("Missing required property 'project_id'")
            __props__.__dict__["project_id"] = project_id
            if type is None and not opts.urn:
                raise TypeError("Missing required property 'type'")
            __props__.__dict__["type"] = type
            __props__.__dict__["api_key"] = None
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["apiKey"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(FeatureFlagApiKey, __self__).__init__(
            'harness:platform/featureFlagApiKey:FeatureFlagApiKey',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            api_key: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            env_id: Optional[pulumi.Input[str]] = None,
            expired_at: Optional[pulumi.Input[int]] = None,
            identifier: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            org_id: Optional[pulumi.Input[str]] = None,
            project_id: Optional[pulumi.Input[str]] = None,
            type: Optional[pulumi.Input[str]] = None) -> 'FeatureFlagApiKey':
        """
        Get an existing FeatureFlagApiKey resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_key: The value of the SDK API Key
        :param pulumi.Input[str] description: Description of the SDK API Key
        :param pulumi.Input[str] env_id: Environment Identifier
        :param pulumi.Input[int] expired_at: Expiration datetime of the SDK API Key
        :param pulumi.Input[str] identifier: Identifier of the SDK API Key
        :param pulumi.Input[str] name: Name of the SDK API Key
        :param pulumi.Input[str] org_id: Organization Identifier
        :param pulumi.Input[str] project_id: Project Identifier
        :param pulumi.Input[str] type: Type of SDK. Valid values are `Server` or `Client`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _FeatureFlagApiKeyState.__new__(_FeatureFlagApiKeyState)

        __props__.__dict__["api_key"] = api_key
        __props__.__dict__["description"] = description
        __props__.__dict__["env_id"] = env_id
        __props__.__dict__["expired_at"] = expired_at
        __props__.__dict__["identifier"] = identifier
        __props__.__dict__["name"] = name
        __props__.__dict__["org_id"] = org_id
        __props__.__dict__["project_id"] = project_id
        __props__.__dict__["type"] = type
        return FeatureFlagApiKey(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="apiKey")
    def api_key(self) -> pulumi.Output[str]:
        """
        The value of the SDK API Key
        """
        return pulumi.get(self, "api_key")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Description of the SDK API Key
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="envId")
    def env_id(self) -> pulumi.Output[str]:
        """
        Environment Identifier
        """
        return pulumi.get(self, "env_id")

    @property
    @pulumi.getter(name="expiredAt")
    def expired_at(self) -> pulumi.Output[Optional[int]]:
        """
        Expiration datetime of the SDK API Key
        """
        return pulumi.get(self, "expired_at")

    @property
    @pulumi.getter
    def identifier(self) -> pulumi.Output[str]:
        """
        Identifier of the SDK API Key
        """
        return pulumi.get(self, "identifier")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the SDK API Key
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> pulumi.Output[str]:
        """
        Organization Identifier
        """
        return pulumi.get(self, "org_id")

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> pulumi.Output[str]:
        """
        Project Identifier
        """
        return pulumi.get(self, "project_id")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Type of SDK. Valid values are `Server` or `Client`.
        """
        return pulumi.get(self, "type")


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

__all__ = ['DbSchemaArgs', 'DbSchema']

@pulumi.input_type
class DbSchemaArgs:
    def __init__(__self__, *,
                 identifier: pulumi.Input[str],
                 org_id: pulumi.Input[str],
                 project_id: pulumi.Input[str],
                 schema_source: pulumi.Input['DbSchemaSchemaSourceArgs'],
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 service: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a DbSchema resource.
        :param pulumi.Input[str] identifier: Unique identifier of the resource.
        :param pulumi.Input[str] org_id: Unique identifier of the organization.
        :param pulumi.Input[str] project_id: Unique identifier of the project.
        :param pulumi.Input['DbSchemaSchemaSourceArgs'] schema_source: Provides a connector and path at which to find the database schema representation
        :param pulumi.Input[str] description: Description of the resource.
        :param pulumi.Input[str] name: Name of the resource.
        :param pulumi.Input[str] service: The service associated with schema
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: Tags to associate with the resource.
        """
        pulumi.set(__self__, "identifier", identifier)
        pulumi.set(__self__, "org_id", org_id)
        pulumi.set(__self__, "project_id", project_id)
        pulumi.set(__self__, "schema_source", schema_source)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if service is not None:
            pulumi.set(__self__, "service", service)
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
    @pulumi.getter(name="orgId")
    def org_id(self) -> pulumi.Input[str]:
        """
        Unique identifier of the organization.
        """
        return pulumi.get(self, "org_id")

    @org_id.setter
    def org_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "org_id", value)

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> pulumi.Input[str]:
        """
        Unique identifier of the project.
        """
        return pulumi.get(self, "project_id")

    @project_id.setter
    def project_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "project_id", value)

    @property
    @pulumi.getter(name="schemaSource")
    def schema_source(self) -> pulumi.Input['DbSchemaSchemaSourceArgs']:
        """
        Provides a connector and path at which to find the database schema representation
        """
        return pulumi.get(self, "schema_source")

    @schema_source.setter
    def schema_source(self, value: pulumi.Input['DbSchemaSchemaSourceArgs']):
        pulumi.set(self, "schema_source", value)

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
    @pulumi.getter
    def service(self) -> Optional[pulumi.Input[str]]:
        """
        The service associated with schema
        """
        return pulumi.get(self, "service")

    @service.setter
    def service(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service", value)

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
class _DbSchemaState:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 identifier: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 schema_source: Optional[pulumi.Input['DbSchemaSchemaSourceArgs']] = None,
                 service: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering DbSchema resources.
        :param pulumi.Input[str] description: Description of the resource.
        :param pulumi.Input[str] identifier: Unique identifier of the resource.
        :param pulumi.Input[str] name: Name of the resource.
        :param pulumi.Input[str] org_id: Unique identifier of the organization.
        :param pulumi.Input[str] project_id: Unique identifier of the project.
        :param pulumi.Input['DbSchemaSchemaSourceArgs'] schema_source: Provides a connector and path at which to find the database schema representation
        :param pulumi.Input[str] service: The service associated with schema
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: Tags to associate with the resource.
        """
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
        if schema_source is not None:
            pulumi.set(__self__, "schema_source", schema_source)
        if service is not None:
            pulumi.set(__self__, "service", service)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

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
    @pulumi.getter(name="schemaSource")
    def schema_source(self) -> Optional[pulumi.Input['DbSchemaSchemaSourceArgs']]:
        """
        Provides a connector and path at which to find the database schema representation
        """
        return pulumi.get(self, "schema_source")

    @schema_source.setter
    def schema_source(self, value: Optional[pulumi.Input['DbSchemaSchemaSourceArgs']]):
        pulumi.set(self, "schema_source", value)

    @property
    @pulumi.getter
    def service(self) -> Optional[pulumi.Input[str]]:
        """
        The service associated with schema
        """
        return pulumi.get(self, "service")

    @service.setter
    def service(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service", value)

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


class DbSchema(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 identifier: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 schema_source: Optional[pulumi.Input[Union['DbSchemaSchemaSourceArgs', 'DbSchemaSchemaSourceArgsDict']]] = None,
                 service: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Resource for creating a Harness DBDevOps Schema.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_harness as harness

        test = harness.platform.DbSchema("test",
            identifier="identifier",
            org_id="org_id",
            project_id="project_id",
            name="name",
            service="service1",
            tags=[
                "foo:bar",
                "bar:foo",
            ],
            schema_source={
                "connector": "gitConnector",
                "repo": "TestRepo",
                "location": "db/example-changelog.yaml",
            })
        ```

        ## Import

        Import project level db schema

        ```sh
        $ pulumi import harness:platform/dbSchema:DbSchema example <org_id>/<project_id>/<db_schema_id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Description of the resource.
        :param pulumi.Input[str] identifier: Unique identifier of the resource.
        :param pulumi.Input[str] name: Name of the resource.
        :param pulumi.Input[str] org_id: Unique identifier of the organization.
        :param pulumi.Input[str] project_id: Unique identifier of the project.
        :param pulumi.Input[Union['DbSchemaSchemaSourceArgs', 'DbSchemaSchemaSourceArgsDict']] schema_source: Provides a connector and path at which to find the database schema representation
        :param pulumi.Input[str] service: The service associated with schema
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: Tags to associate with the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DbSchemaArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource for creating a Harness DBDevOps Schema.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_harness as harness

        test = harness.platform.DbSchema("test",
            identifier="identifier",
            org_id="org_id",
            project_id="project_id",
            name="name",
            service="service1",
            tags=[
                "foo:bar",
                "bar:foo",
            ],
            schema_source={
                "connector": "gitConnector",
                "repo": "TestRepo",
                "location": "db/example-changelog.yaml",
            })
        ```

        ## Import

        Import project level db schema

        ```sh
        $ pulumi import harness:platform/dbSchema:DbSchema example <org_id>/<project_id>/<db_schema_id>
        ```

        :param str resource_name: The name of the resource.
        :param DbSchemaArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DbSchemaArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 identifier: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 schema_source: Optional[pulumi.Input[Union['DbSchemaSchemaSourceArgs', 'DbSchemaSchemaSourceArgsDict']]] = None,
                 service: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DbSchemaArgs.__new__(DbSchemaArgs)

            __props__.__dict__["description"] = description
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
            if schema_source is None and not opts.urn:
                raise TypeError("Missing required property 'schema_source'")
            __props__.__dict__["schema_source"] = schema_source
            __props__.__dict__["service"] = service
            __props__.__dict__["tags"] = tags
        super(DbSchema, __self__).__init__(
            'harness:platform/dbSchema:DbSchema',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            description: Optional[pulumi.Input[str]] = None,
            identifier: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            org_id: Optional[pulumi.Input[str]] = None,
            project_id: Optional[pulumi.Input[str]] = None,
            schema_source: Optional[pulumi.Input[Union['DbSchemaSchemaSourceArgs', 'DbSchemaSchemaSourceArgsDict']]] = None,
            service: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None) -> 'DbSchema':
        """
        Get an existing DbSchema resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Description of the resource.
        :param pulumi.Input[str] identifier: Unique identifier of the resource.
        :param pulumi.Input[str] name: Name of the resource.
        :param pulumi.Input[str] org_id: Unique identifier of the organization.
        :param pulumi.Input[str] project_id: Unique identifier of the project.
        :param pulumi.Input[Union['DbSchemaSchemaSourceArgs', 'DbSchemaSchemaSourceArgsDict']] schema_source: Provides a connector and path at which to find the database schema representation
        :param pulumi.Input[str] service: The service associated with schema
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: Tags to associate with the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _DbSchemaState.__new__(_DbSchemaState)

        __props__.__dict__["description"] = description
        __props__.__dict__["identifier"] = identifier
        __props__.__dict__["name"] = name
        __props__.__dict__["org_id"] = org_id
        __props__.__dict__["project_id"] = project_id
        __props__.__dict__["schema_source"] = schema_source
        __props__.__dict__["service"] = service
        __props__.__dict__["tags"] = tags
        return DbSchema(resource_name, opts=opts, __props__=__props__)

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
    def org_id(self) -> pulumi.Output[str]:
        """
        Unique identifier of the organization.
        """
        return pulumi.get(self, "org_id")

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> pulumi.Output[str]:
        """
        Unique identifier of the project.
        """
        return pulumi.get(self, "project_id")

    @property
    @pulumi.getter(name="schemaSource")
    def schema_source(self) -> pulumi.Output['outputs.DbSchemaSchemaSource']:
        """
        Provides a connector and path at which to find the database schema representation
        """
        return pulumi.get(self, "schema_source")

    @property
    @pulumi.getter
    def service(self) -> pulumi.Output[Optional[str]]:
        """
        The service associated with schema
        """
        return pulumi.get(self, "service")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Tags to associate with the resource.
        """
        return pulumi.get(self, "tags")


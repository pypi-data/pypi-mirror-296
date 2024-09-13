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

__all__ = ['InputSetArgs', 'InputSet']

@pulumi.input_type
class InputSetArgs:
    def __init__(__self__, *,
                 identifier: pulumi.Input[str],
                 org_id: pulumi.Input[str],
                 pipeline_id: pulumi.Input[str],
                 project_id: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 git_details: Optional[pulumi.Input['InputSetGitDetailsArgs']] = None,
                 git_import_info: Optional[pulumi.Input['InputSetGitImportInfoArgs']] = None,
                 import_from_git: Optional[pulumi.Input[bool]] = None,
                 input_set_import_request: Optional[pulumi.Input['InputSetInputSetImportRequestArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 yaml: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a InputSet resource.
        :param pulumi.Input[str] identifier: Unique identifier of the resource.
        :param pulumi.Input[str] org_id: Unique identifier of the organization.
        :param pulumi.Input[str] pipeline_id: Identifier of the pipeline
        :param pulumi.Input[str] project_id: Unique identifier of the project.
        :param pulumi.Input[str] description: Description of the resource.
        :param pulumi.Input['InputSetGitDetailsArgs'] git_details: Contains parameters related to creating an Entity for Git Experience.
        :param pulumi.Input['InputSetGitImportInfoArgs'] git_import_info: Contains Git Information for importing entities from Git
        :param pulumi.Input[bool] import_from_git: Flag to set if importing from Git
        :param pulumi.Input['InputSetInputSetImportRequestArgs'] input_set_import_request: Contains parameters for importing a input set
        :param pulumi.Input[str] name: Name of the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: Tags to associate with the resource.
        :param pulumi.Input[str] yaml: Input Set YAML. In YAML, to reference an entity at the organization scope, prefix 'org' to the expression: org.{identifier}. To reference an entity at the account scope, prefix 'account` to the expression: account.{identifier}. For eg, to reference a connector with identifier 'connectorId' at the organization scope in a stage mention it as connectorRef: org.connectorId.
        """
        pulumi.set(__self__, "identifier", identifier)
        pulumi.set(__self__, "org_id", org_id)
        pulumi.set(__self__, "pipeline_id", pipeline_id)
        pulumi.set(__self__, "project_id", project_id)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if git_details is not None:
            pulumi.set(__self__, "git_details", git_details)
        if git_import_info is not None:
            pulumi.set(__self__, "git_import_info", git_import_info)
        if import_from_git is not None:
            pulumi.set(__self__, "import_from_git", import_from_git)
        if input_set_import_request is not None:
            pulumi.set(__self__, "input_set_import_request", input_set_import_request)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if yaml is not None:
            pulumi.set(__self__, "yaml", yaml)

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
    @pulumi.getter(name="pipelineId")
    def pipeline_id(self) -> pulumi.Input[str]:
        """
        Identifier of the pipeline
        """
        return pulumi.get(self, "pipeline_id")

    @pipeline_id.setter
    def pipeline_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "pipeline_id", value)

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
    @pulumi.getter(name="gitDetails")
    def git_details(self) -> Optional[pulumi.Input['InputSetGitDetailsArgs']]:
        """
        Contains parameters related to creating an Entity for Git Experience.
        """
        return pulumi.get(self, "git_details")

    @git_details.setter
    def git_details(self, value: Optional[pulumi.Input['InputSetGitDetailsArgs']]):
        pulumi.set(self, "git_details", value)

    @property
    @pulumi.getter(name="gitImportInfo")
    def git_import_info(self) -> Optional[pulumi.Input['InputSetGitImportInfoArgs']]:
        """
        Contains Git Information for importing entities from Git
        """
        return pulumi.get(self, "git_import_info")

    @git_import_info.setter
    def git_import_info(self, value: Optional[pulumi.Input['InputSetGitImportInfoArgs']]):
        pulumi.set(self, "git_import_info", value)

    @property
    @pulumi.getter(name="importFromGit")
    def import_from_git(self) -> Optional[pulumi.Input[bool]]:
        """
        Flag to set if importing from Git
        """
        return pulumi.get(self, "import_from_git")

    @import_from_git.setter
    def import_from_git(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "import_from_git", value)

    @property
    @pulumi.getter(name="inputSetImportRequest")
    def input_set_import_request(self) -> Optional[pulumi.Input['InputSetInputSetImportRequestArgs']]:
        """
        Contains parameters for importing a input set
        """
        return pulumi.get(self, "input_set_import_request")

    @input_set_import_request.setter
    def input_set_import_request(self, value: Optional[pulumi.Input['InputSetInputSetImportRequestArgs']]):
        pulumi.set(self, "input_set_import_request", value)

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
    def yaml(self) -> Optional[pulumi.Input[str]]:
        """
        Input Set YAML. In YAML, to reference an entity at the organization scope, prefix 'org' to the expression: org.{identifier}. To reference an entity at the account scope, prefix 'account` to the expression: account.{identifier}. For eg, to reference a connector with identifier 'connectorId' at the organization scope in a stage mention it as connectorRef: org.connectorId.
        """
        return pulumi.get(self, "yaml")

    @yaml.setter
    def yaml(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "yaml", value)


@pulumi.input_type
class _InputSetState:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 git_details: Optional[pulumi.Input['InputSetGitDetailsArgs']] = None,
                 git_import_info: Optional[pulumi.Input['InputSetGitImportInfoArgs']] = None,
                 identifier: Optional[pulumi.Input[str]] = None,
                 import_from_git: Optional[pulumi.Input[bool]] = None,
                 input_set_import_request: Optional[pulumi.Input['InputSetInputSetImportRequestArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 pipeline_id: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 yaml: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering InputSet resources.
        :param pulumi.Input[str] description: Description of the resource.
        :param pulumi.Input['InputSetGitDetailsArgs'] git_details: Contains parameters related to creating an Entity for Git Experience.
        :param pulumi.Input['InputSetGitImportInfoArgs'] git_import_info: Contains Git Information for importing entities from Git
        :param pulumi.Input[str] identifier: Unique identifier of the resource.
        :param pulumi.Input[bool] import_from_git: Flag to set if importing from Git
        :param pulumi.Input['InputSetInputSetImportRequestArgs'] input_set_import_request: Contains parameters for importing a input set
        :param pulumi.Input[str] name: Name of the resource.
        :param pulumi.Input[str] org_id: Unique identifier of the organization.
        :param pulumi.Input[str] pipeline_id: Identifier of the pipeline
        :param pulumi.Input[str] project_id: Unique identifier of the project.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: Tags to associate with the resource.
        :param pulumi.Input[str] yaml: Input Set YAML. In YAML, to reference an entity at the organization scope, prefix 'org' to the expression: org.{identifier}. To reference an entity at the account scope, prefix 'account` to the expression: account.{identifier}. For eg, to reference a connector with identifier 'connectorId' at the organization scope in a stage mention it as connectorRef: org.connectorId.
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if git_details is not None:
            pulumi.set(__self__, "git_details", git_details)
        if git_import_info is not None:
            pulumi.set(__self__, "git_import_info", git_import_info)
        if identifier is not None:
            pulumi.set(__self__, "identifier", identifier)
        if import_from_git is not None:
            pulumi.set(__self__, "import_from_git", import_from_git)
        if input_set_import_request is not None:
            pulumi.set(__self__, "input_set_import_request", input_set_import_request)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if org_id is not None:
            pulumi.set(__self__, "org_id", org_id)
        if pipeline_id is not None:
            pulumi.set(__self__, "pipeline_id", pipeline_id)
        if project_id is not None:
            pulumi.set(__self__, "project_id", project_id)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if yaml is not None:
            pulumi.set(__self__, "yaml", yaml)

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
    @pulumi.getter(name="gitDetails")
    def git_details(self) -> Optional[pulumi.Input['InputSetGitDetailsArgs']]:
        """
        Contains parameters related to creating an Entity for Git Experience.
        """
        return pulumi.get(self, "git_details")

    @git_details.setter
    def git_details(self, value: Optional[pulumi.Input['InputSetGitDetailsArgs']]):
        pulumi.set(self, "git_details", value)

    @property
    @pulumi.getter(name="gitImportInfo")
    def git_import_info(self) -> Optional[pulumi.Input['InputSetGitImportInfoArgs']]:
        """
        Contains Git Information for importing entities from Git
        """
        return pulumi.get(self, "git_import_info")

    @git_import_info.setter
    def git_import_info(self, value: Optional[pulumi.Input['InputSetGitImportInfoArgs']]):
        pulumi.set(self, "git_import_info", value)

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
    @pulumi.getter(name="importFromGit")
    def import_from_git(self) -> Optional[pulumi.Input[bool]]:
        """
        Flag to set if importing from Git
        """
        return pulumi.get(self, "import_from_git")

    @import_from_git.setter
    def import_from_git(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "import_from_git", value)

    @property
    @pulumi.getter(name="inputSetImportRequest")
    def input_set_import_request(self) -> Optional[pulumi.Input['InputSetInputSetImportRequestArgs']]:
        """
        Contains parameters for importing a input set
        """
        return pulumi.get(self, "input_set_import_request")

    @input_set_import_request.setter
    def input_set_import_request(self, value: Optional[pulumi.Input['InputSetInputSetImportRequestArgs']]):
        pulumi.set(self, "input_set_import_request", value)

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
    @pulumi.getter(name="pipelineId")
    def pipeline_id(self) -> Optional[pulumi.Input[str]]:
        """
        Identifier of the pipeline
        """
        return pulumi.get(self, "pipeline_id")

    @pipeline_id.setter
    def pipeline_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "pipeline_id", value)

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
    def yaml(self) -> Optional[pulumi.Input[str]]:
        """
        Input Set YAML. In YAML, to reference an entity at the organization scope, prefix 'org' to the expression: org.{identifier}. To reference an entity at the account scope, prefix 'account` to the expression: account.{identifier}. For eg, to reference a connector with identifier 'connectorId' at the organization scope in a stage mention it as connectorRef: org.connectorId.
        """
        return pulumi.get(self, "yaml")

    @yaml.setter
    def yaml(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "yaml", value)


class InputSet(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 git_details: Optional[pulumi.Input[Union['InputSetGitDetailsArgs', 'InputSetGitDetailsArgsDict']]] = None,
                 git_import_info: Optional[pulumi.Input[Union['InputSetGitImportInfoArgs', 'InputSetGitImportInfoArgsDict']]] = None,
                 identifier: Optional[pulumi.Input[str]] = None,
                 import_from_git: Optional[pulumi.Input[bool]] = None,
                 input_set_import_request: Optional[pulumi.Input[Union['InputSetInputSetImportRequestArgs', 'InputSetInputSetImportRequestArgsDict']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 pipeline_id: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 yaml: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource for creating a Harness InputSet.

        ## Import

        Import input set

        ```sh
        $ pulumi import harness:platform/inputSet:InputSet example <org_id>/<project_id>/<pipeline_id>/<input_set_id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Description of the resource.
        :param pulumi.Input[Union['InputSetGitDetailsArgs', 'InputSetGitDetailsArgsDict']] git_details: Contains parameters related to creating an Entity for Git Experience.
        :param pulumi.Input[Union['InputSetGitImportInfoArgs', 'InputSetGitImportInfoArgsDict']] git_import_info: Contains Git Information for importing entities from Git
        :param pulumi.Input[str] identifier: Unique identifier of the resource.
        :param pulumi.Input[bool] import_from_git: Flag to set if importing from Git
        :param pulumi.Input[Union['InputSetInputSetImportRequestArgs', 'InputSetInputSetImportRequestArgsDict']] input_set_import_request: Contains parameters for importing a input set
        :param pulumi.Input[str] name: Name of the resource.
        :param pulumi.Input[str] org_id: Unique identifier of the organization.
        :param pulumi.Input[str] pipeline_id: Identifier of the pipeline
        :param pulumi.Input[str] project_id: Unique identifier of the project.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: Tags to associate with the resource.
        :param pulumi.Input[str] yaml: Input Set YAML. In YAML, to reference an entity at the organization scope, prefix 'org' to the expression: org.{identifier}. To reference an entity at the account scope, prefix 'account` to the expression: account.{identifier}. For eg, to reference a connector with identifier 'connectorId' at the organization scope in a stage mention it as connectorRef: org.connectorId.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: InputSetArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource for creating a Harness InputSet.

        ## Import

        Import input set

        ```sh
        $ pulumi import harness:platform/inputSet:InputSet example <org_id>/<project_id>/<pipeline_id>/<input_set_id>
        ```

        :param str resource_name: The name of the resource.
        :param InputSetArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(InputSetArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 git_details: Optional[pulumi.Input[Union['InputSetGitDetailsArgs', 'InputSetGitDetailsArgsDict']]] = None,
                 git_import_info: Optional[pulumi.Input[Union['InputSetGitImportInfoArgs', 'InputSetGitImportInfoArgsDict']]] = None,
                 identifier: Optional[pulumi.Input[str]] = None,
                 import_from_git: Optional[pulumi.Input[bool]] = None,
                 input_set_import_request: Optional[pulumi.Input[Union['InputSetInputSetImportRequestArgs', 'InputSetInputSetImportRequestArgsDict']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 pipeline_id: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 yaml: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = InputSetArgs.__new__(InputSetArgs)

            __props__.__dict__["description"] = description
            __props__.__dict__["git_details"] = git_details
            __props__.__dict__["git_import_info"] = git_import_info
            if identifier is None and not opts.urn:
                raise TypeError("Missing required property 'identifier'")
            __props__.__dict__["identifier"] = identifier
            __props__.__dict__["import_from_git"] = import_from_git
            __props__.__dict__["input_set_import_request"] = input_set_import_request
            __props__.__dict__["name"] = name
            if org_id is None and not opts.urn:
                raise TypeError("Missing required property 'org_id'")
            __props__.__dict__["org_id"] = org_id
            if pipeline_id is None and not opts.urn:
                raise TypeError("Missing required property 'pipeline_id'")
            __props__.__dict__["pipeline_id"] = pipeline_id
            if project_id is None and not opts.urn:
                raise TypeError("Missing required property 'project_id'")
            __props__.__dict__["project_id"] = project_id
            __props__.__dict__["tags"] = tags
            __props__.__dict__["yaml"] = yaml
        super(InputSet, __self__).__init__(
            'harness:platform/inputSet:InputSet',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            description: Optional[pulumi.Input[str]] = None,
            git_details: Optional[pulumi.Input[Union['InputSetGitDetailsArgs', 'InputSetGitDetailsArgsDict']]] = None,
            git_import_info: Optional[pulumi.Input[Union['InputSetGitImportInfoArgs', 'InputSetGitImportInfoArgsDict']]] = None,
            identifier: Optional[pulumi.Input[str]] = None,
            import_from_git: Optional[pulumi.Input[bool]] = None,
            input_set_import_request: Optional[pulumi.Input[Union['InputSetInputSetImportRequestArgs', 'InputSetInputSetImportRequestArgsDict']]] = None,
            name: Optional[pulumi.Input[str]] = None,
            org_id: Optional[pulumi.Input[str]] = None,
            pipeline_id: Optional[pulumi.Input[str]] = None,
            project_id: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            yaml: Optional[pulumi.Input[str]] = None) -> 'InputSet':
        """
        Get an existing InputSet resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Description of the resource.
        :param pulumi.Input[Union['InputSetGitDetailsArgs', 'InputSetGitDetailsArgsDict']] git_details: Contains parameters related to creating an Entity for Git Experience.
        :param pulumi.Input[Union['InputSetGitImportInfoArgs', 'InputSetGitImportInfoArgsDict']] git_import_info: Contains Git Information for importing entities from Git
        :param pulumi.Input[str] identifier: Unique identifier of the resource.
        :param pulumi.Input[bool] import_from_git: Flag to set if importing from Git
        :param pulumi.Input[Union['InputSetInputSetImportRequestArgs', 'InputSetInputSetImportRequestArgsDict']] input_set_import_request: Contains parameters for importing a input set
        :param pulumi.Input[str] name: Name of the resource.
        :param pulumi.Input[str] org_id: Unique identifier of the organization.
        :param pulumi.Input[str] pipeline_id: Identifier of the pipeline
        :param pulumi.Input[str] project_id: Unique identifier of the project.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: Tags to associate with the resource.
        :param pulumi.Input[str] yaml: Input Set YAML. In YAML, to reference an entity at the organization scope, prefix 'org' to the expression: org.{identifier}. To reference an entity at the account scope, prefix 'account` to the expression: account.{identifier}. For eg, to reference a connector with identifier 'connectorId' at the organization scope in a stage mention it as connectorRef: org.connectorId.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _InputSetState.__new__(_InputSetState)

        __props__.__dict__["description"] = description
        __props__.__dict__["git_details"] = git_details
        __props__.__dict__["git_import_info"] = git_import_info
        __props__.__dict__["identifier"] = identifier
        __props__.__dict__["import_from_git"] = import_from_git
        __props__.__dict__["input_set_import_request"] = input_set_import_request
        __props__.__dict__["name"] = name
        __props__.__dict__["org_id"] = org_id
        __props__.__dict__["pipeline_id"] = pipeline_id
        __props__.__dict__["project_id"] = project_id
        __props__.__dict__["tags"] = tags
        __props__.__dict__["yaml"] = yaml
        return InputSet(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Description of the resource.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="gitDetails")
    def git_details(self) -> pulumi.Output['outputs.InputSetGitDetails']:
        """
        Contains parameters related to creating an Entity for Git Experience.
        """
        return pulumi.get(self, "git_details")

    @property
    @pulumi.getter(name="gitImportInfo")
    def git_import_info(self) -> pulumi.Output[Optional['outputs.InputSetGitImportInfo']]:
        """
        Contains Git Information for importing entities from Git
        """
        return pulumi.get(self, "git_import_info")

    @property
    @pulumi.getter
    def identifier(self) -> pulumi.Output[str]:
        """
        Unique identifier of the resource.
        """
        return pulumi.get(self, "identifier")

    @property
    @pulumi.getter(name="importFromGit")
    def import_from_git(self) -> pulumi.Output[Optional[bool]]:
        """
        Flag to set if importing from Git
        """
        return pulumi.get(self, "import_from_git")

    @property
    @pulumi.getter(name="inputSetImportRequest")
    def input_set_import_request(self) -> pulumi.Output[Optional['outputs.InputSetInputSetImportRequest']]:
        """
        Contains parameters for importing a input set
        """
        return pulumi.get(self, "input_set_import_request")

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
    @pulumi.getter(name="pipelineId")
    def pipeline_id(self) -> pulumi.Output[str]:
        """
        Identifier of the pipeline
        """
        return pulumi.get(self, "pipeline_id")

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> pulumi.Output[str]:
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
    def yaml(self) -> pulumi.Output[str]:
        """
        Input Set YAML. In YAML, to reference an entity at the organization scope, prefix 'org' to the expression: org.{identifier}. To reference an entity at the account scope, prefix 'account` to the expression: account.{identifier}. For eg, to reference a connector with identifier 'connectorId' at the organization scope in a stage mention it as connectorRef: org.connectorId.
        """
        return pulumi.get(self, "yaml")


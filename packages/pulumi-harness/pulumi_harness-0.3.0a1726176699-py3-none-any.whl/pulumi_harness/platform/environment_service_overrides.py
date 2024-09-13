# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['EnvironmentServiceOverridesArgs', 'EnvironmentServiceOverrides']

@pulumi.input_type
class EnvironmentServiceOverridesArgs:
    def __init__(__self__, *,
                 env_id: pulumi.Input[str],
                 service_id: pulumi.Input[str],
                 yaml: pulumi.Input[str],
                 identifier: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a EnvironmentServiceOverrides resource.
        :param pulumi.Input[str] env_id: The env Id associated with the overrides. To reference an environment at the organization scope, prefix 'org' to the expression: org.{env*id}. To reference an environment at the account scope, prefix 'account' to the expression: account.{env*id}).
        :param pulumi.Input[str] service_id: The service Id associated with the overrides. To reference a service at the organization scope, prefix 'org' to the expression: org.{service*id}. To reference a service at the account scope, prefix 'account' to the expression: account.{service*id}).
        :param pulumi.Input[str] yaml: Environment Service Overrides YAML. In YAML, to reference an entity at the organization scope, prefix 'org' to the expression: org.{identifier}. To reference an entity at the account scope, prefix 'account` to the expression: account.{identifier}. For eg, to reference a connector with identifier 'connectorId' at the organization scope in a stage mention it as connectorRef: org.connectorId.
        :param pulumi.Input[str] identifier: identifier of the service overrides.
        :param pulumi.Input[str] org_id: Unique identifier of the organization.
        :param pulumi.Input[str] project_id: Unique identifier of the project.
        """
        pulumi.set(__self__, "env_id", env_id)
        pulumi.set(__self__, "service_id", service_id)
        pulumi.set(__self__, "yaml", yaml)
        if identifier is not None:
            pulumi.set(__self__, "identifier", identifier)
        if org_id is not None:
            pulumi.set(__self__, "org_id", org_id)
        if project_id is not None:
            pulumi.set(__self__, "project_id", project_id)

    @property
    @pulumi.getter(name="envId")
    def env_id(self) -> pulumi.Input[str]:
        """
        The env Id associated with the overrides. To reference an environment at the organization scope, prefix 'org' to the expression: org.{env*id}. To reference an environment at the account scope, prefix 'account' to the expression: account.{env*id}).
        """
        return pulumi.get(self, "env_id")

    @env_id.setter
    def env_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "env_id", value)

    @property
    @pulumi.getter(name="serviceId")
    def service_id(self) -> pulumi.Input[str]:
        """
        The service Id associated with the overrides. To reference a service at the organization scope, prefix 'org' to the expression: org.{service*id}. To reference a service at the account scope, prefix 'account' to the expression: account.{service*id}).
        """
        return pulumi.get(self, "service_id")

    @service_id.setter
    def service_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "service_id", value)

    @property
    @pulumi.getter
    def yaml(self) -> pulumi.Input[str]:
        """
        Environment Service Overrides YAML. In YAML, to reference an entity at the organization scope, prefix 'org' to the expression: org.{identifier}. To reference an entity at the account scope, prefix 'account` to the expression: account.{identifier}. For eg, to reference a connector with identifier 'connectorId' at the organization scope in a stage mention it as connectorRef: org.connectorId.
        """
        return pulumi.get(self, "yaml")

    @yaml.setter
    def yaml(self, value: pulumi.Input[str]):
        pulumi.set(self, "yaml", value)

    @property
    @pulumi.getter
    def identifier(self) -> Optional[pulumi.Input[str]]:
        """
        identifier of the service overrides.
        """
        return pulumi.get(self, "identifier")

    @identifier.setter
    def identifier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "identifier", value)

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


@pulumi.input_type
class _EnvironmentServiceOverridesState:
    def __init__(__self__, *,
                 env_id: Optional[pulumi.Input[str]] = None,
                 identifier: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 service_id: Optional[pulumi.Input[str]] = None,
                 yaml: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering EnvironmentServiceOverrides resources.
        :param pulumi.Input[str] env_id: The env Id associated with the overrides. To reference an environment at the organization scope, prefix 'org' to the expression: org.{env*id}. To reference an environment at the account scope, prefix 'account' to the expression: account.{env*id}).
        :param pulumi.Input[str] identifier: identifier of the service overrides.
        :param pulumi.Input[str] org_id: Unique identifier of the organization.
        :param pulumi.Input[str] project_id: Unique identifier of the project.
        :param pulumi.Input[str] service_id: The service Id associated with the overrides. To reference a service at the organization scope, prefix 'org' to the expression: org.{service*id}. To reference a service at the account scope, prefix 'account' to the expression: account.{service*id}).
        :param pulumi.Input[str] yaml: Environment Service Overrides YAML. In YAML, to reference an entity at the organization scope, prefix 'org' to the expression: org.{identifier}. To reference an entity at the account scope, prefix 'account` to the expression: account.{identifier}. For eg, to reference a connector with identifier 'connectorId' at the organization scope in a stage mention it as connectorRef: org.connectorId.
        """
        if env_id is not None:
            pulumi.set(__self__, "env_id", env_id)
        if identifier is not None:
            pulumi.set(__self__, "identifier", identifier)
        if org_id is not None:
            pulumi.set(__self__, "org_id", org_id)
        if project_id is not None:
            pulumi.set(__self__, "project_id", project_id)
        if service_id is not None:
            pulumi.set(__self__, "service_id", service_id)
        if yaml is not None:
            pulumi.set(__self__, "yaml", yaml)

    @property
    @pulumi.getter(name="envId")
    def env_id(self) -> Optional[pulumi.Input[str]]:
        """
        The env Id associated with the overrides. To reference an environment at the organization scope, prefix 'org' to the expression: org.{env*id}. To reference an environment at the account scope, prefix 'account' to the expression: account.{env*id}).
        """
        return pulumi.get(self, "env_id")

    @env_id.setter
    def env_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "env_id", value)

    @property
    @pulumi.getter
    def identifier(self) -> Optional[pulumi.Input[str]]:
        """
        identifier of the service overrides.
        """
        return pulumi.get(self, "identifier")

    @identifier.setter
    def identifier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "identifier", value)

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
    @pulumi.getter(name="serviceId")
    def service_id(self) -> Optional[pulumi.Input[str]]:
        """
        The service Id associated with the overrides. To reference a service at the organization scope, prefix 'org' to the expression: org.{service*id}. To reference a service at the account scope, prefix 'account' to the expression: account.{service*id}).
        """
        return pulumi.get(self, "service_id")

    @service_id.setter
    def service_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_id", value)

    @property
    @pulumi.getter
    def yaml(self) -> Optional[pulumi.Input[str]]:
        """
        Environment Service Overrides YAML. In YAML, to reference an entity at the organization scope, prefix 'org' to the expression: org.{identifier}. To reference an entity at the account scope, prefix 'account` to the expression: account.{identifier}. For eg, to reference a connector with identifier 'connectorId' at the organization scope in a stage mention it as connectorRef: org.connectorId.
        """
        return pulumi.get(self, "yaml")

    @yaml.setter
    def yaml(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "yaml", value)


class EnvironmentServiceOverrides(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 env_id: Optional[pulumi.Input[str]] = None,
                 identifier: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 service_id: Optional[pulumi.Input[str]] = None,
                 yaml: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource for creating a Harness environment service overrides.
        ## Example to create Environment Service Override at different levels (Org, Project, Account)

        ### Account Level
        ```python
        import pulumi
        import pulumi_harness as harness

        example = harness.platform.EnvironmentServiceOverrides("example",
            env_id="environmentIdentifier",
            service_id="serviceIdentifier",
            yaml=\"\"\"serviceOverrides:
          environmentRef: environmentIdentifier
          serviceRef: serviceIdentifier
          variables:
           - name: asda
             type: String
             value: asddad
          manifests:
             - manifest:
                 identifier: manifestEnv
                 type: Values
                 spec:
                   store:
                     type: Git
                     spec:
                       connectorRef: <+input>
                       gitFetchType: Branch
                       paths:
                         - file1
                       repoName: <+input>
                       branch: master
          configFiles:
             - configFile:
                 identifier: configFileEnv
                 spec:
                   store:
                     type: Harness
                     spec:
                       files:
                         - account:/Add-ons/svcOverrideTest
                       secretFiles: []
        \"\"\")
        ```

        ### Org Level
        ```python
        import pulumi
        import pulumi_harness as harness

        example = harness.platform.EnvironmentServiceOverrides("example",
            org_id="orgIdentifier",
            env_id="environmentIdentifier",
            service_id="serviceIdentifier",
            yaml=\"\"\"serviceOverrides:
          environmentRef: environmentIdentifier
          serviceRef: serviceIdentifier
          variables:
           - name: asda
             type: String
             value: asddad
          manifests:
             - manifest:
                 identifier: manifestEnv
                 type: Values
                 spec:
                   store:
                     type: Git
                     spec:
                       connectorRef: <+input>
                       gitFetchType: Branch
                       paths:
                         - file1
                       repoName: <+input>
                       branch: master
          configFiles:
             - configFile:
                 identifier: configFileEnv
                 spec:
                   store:
                     type: Harness
                     spec:
                       files:
                         - account:/Add-ons/svcOverrideTest
                       secretFiles: []
        \"\"\")
        ```

        ### Project Level
        ```python
        import pulumi
        import pulumi_harness as harness

        example = harness.platform.EnvironmentServiceOverrides("example",
            org_id="orgIdentifier",
            project_id="projectIdentifier",
            env_id="environmentIdentifier",
            service_id="serviceIdentifier",
            yaml=\"\"\"serviceOverrides:
          environmentRef: environmentIdentifier
          serviceRef: serviceIdentifier
          variables:
           - name: asda
             type: String
             value: asddad
          manifests:
             - manifest:
                 identifier: manifestEnv
                 type: Values
                 spec:
                   store:
                     type: Git
                     spec:
                       connectorRef: <+input>
                       gitFetchType: Branch
                       paths:
                         - file1
                       repoName: <+input>
                       branch: master
          configFiles:
             - configFile:
                 identifier: configFileEnv
                 spec:
                   store:
                     type: Harness
                     spec:
                       files:
                         - account:/Add-ons/svcOverrideTest
                       secretFiles: []
        \"\"\")
        ```

        ## Import

        Import list of account level service overrides using the env id associated with them

        ```sh
        $ pulumi import harness:platform/environmentServiceOverrides:EnvironmentServiceOverrides example <env_id>
        ```

        Import list of org level service overrides using the env id associated with them

        ```sh
        $ pulumi import harness:platform/environmentServiceOverrides:EnvironmentServiceOverrides example <org_id>/<env_id>
        ```

        Import list of project level service overrides using the env id associated with them

        ```sh
        $ pulumi import harness:platform/environmentServiceOverrides:EnvironmentServiceOverrides example <org_id>/<project_id>/<env_id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] env_id: The env Id associated with the overrides. To reference an environment at the organization scope, prefix 'org' to the expression: org.{env*id}. To reference an environment at the account scope, prefix 'account' to the expression: account.{env*id}).
        :param pulumi.Input[str] identifier: identifier of the service overrides.
        :param pulumi.Input[str] org_id: Unique identifier of the organization.
        :param pulumi.Input[str] project_id: Unique identifier of the project.
        :param pulumi.Input[str] service_id: The service Id associated with the overrides. To reference a service at the organization scope, prefix 'org' to the expression: org.{service*id}. To reference a service at the account scope, prefix 'account' to the expression: account.{service*id}).
        :param pulumi.Input[str] yaml: Environment Service Overrides YAML. In YAML, to reference an entity at the organization scope, prefix 'org' to the expression: org.{identifier}. To reference an entity at the account scope, prefix 'account` to the expression: account.{identifier}. For eg, to reference a connector with identifier 'connectorId' at the organization scope in a stage mention it as connectorRef: org.connectorId.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: EnvironmentServiceOverridesArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource for creating a Harness environment service overrides.
        ## Example to create Environment Service Override at different levels (Org, Project, Account)

        ### Account Level
        ```python
        import pulumi
        import pulumi_harness as harness

        example = harness.platform.EnvironmentServiceOverrides("example",
            env_id="environmentIdentifier",
            service_id="serviceIdentifier",
            yaml=\"\"\"serviceOverrides:
          environmentRef: environmentIdentifier
          serviceRef: serviceIdentifier
          variables:
           - name: asda
             type: String
             value: asddad
          manifests:
             - manifest:
                 identifier: manifestEnv
                 type: Values
                 spec:
                   store:
                     type: Git
                     spec:
                       connectorRef: <+input>
                       gitFetchType: Branch
                       paths:
                         - file1
                       repoName: <+input>
                       branch: master
          configFiles:
             - configFile:
                 identifier: configFileEnv
                 spec:
                   store:
                     type: Harness
                     spec:
                       files:
                         - account:/Add-ons/svcOverrideTest
                       secretFiles: []
        \"\"\")
        ```

        ### Org Level
        ```python
        import pulumi
        import pulumi_harness as harness

        example = harness.platform.EnvironmentServiceOverrides("example",
            org_id="orgIdentifier",
            env_id="environmentIdentifier",
            service_id="serviceIdentifier",
            yaml=\"\"\"serviceOverrides:
          environmentRef: environmentIdentifier
          serviceRef: serviceIdentifier
          variables:
           - name: asda
             type: String
             value: asddad
          manifests:
             - manifest:
                 identifier: manifestEnv
                 type: Values
                 spec:
                   store:
                     type: Git
                     spec:
                       connectorRef: <+input>
                       gitFetchType: Branch
                       paths:
                         - file1
                       repoName: <+input>
                       branch: master
          configFiles:
             - configFile:
                 identifier: configFileEnv
                 spec:
                   store:
                     type: Harness
                     spec:
                       files:
                         - account:/Add-ons/svcOverrideTest
                       secretFiles: []
        \"\"\")
        ```

        ### Project Level
        ```python
        import pulumi
        import pulumi_harness as harness

        example = harness.platform.EnvironmentServiceOverrides("example",
            org_id="orgIdentifier",
            project_id="projectIdentifier",
            env_id="environmentIdentifier",
            service_id="serviceIdentifier",
            yaml=\"\"\"serviceOverrides:
          environmentRef: environmentIdentifier
          serviceRef: serviceIdentifier
          variables:
           - name: asda
             type: String
             value: asddad
          manifests:
             - manifest:
                 identifier: manifestEnv
                 type: Values
                 spec:
                   store:
                     type: Git
                     spec:
                       connectorRef: <+input>
                       gitFetchType: Branch
                       paths:
                         - file1
                       repoName: <+input>
                       branch: master
          configFiles:
             - configFile:
                 identifier: configFileEnv
                 spec:
                   store:
                     type: Harness
                     spec:
                       files:
                         - account:/Add-ons/svcOverrideTest
                       secretFiles: []
        \"\"\")
        ```

        ## Import

        Import list of account level service overrides using the env id associated with them

        ```sh
        $ pulumi import harness:platform/environmentServiceOverrides:EnvironmentServiceOverrides example <env_id>
        ```

        Import list of org level service overrides using the env id associated with them

        ```sh
        $ pulumi import harness:platform/environmentServiceOverrides:EnvironmentServiceOverrides example <org_id>/<env_id>
        ```

        Import list of project level service overrides using the env id associated with them

        ```sh
        $ pulumi import harness:platform/environmentServiceOverrides:EnvironmentServiceOverrides example <org_id>/<project_id>/<env_id>
        ```

        :param str resource_name: The name of the resource.
        :param EnvironmentServiceOverridesArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(EnvironmentServiceOverridesArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 env_id: Optional[pulumi.Input[str]] = None,
                 identifier: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 service_id: Optional[pulumi.Input[str]] = None,
                 yaml: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = EnvironmentServiceOverridesArgs.__new__(EnvironmentServiceOverridesArgs)

            if env_id is None and not opts.urn:
                raise TypeError("Missing required property 'env_id'")
            __props__.__dict__["env_id"] = env_id
            __props__.__dict__["identifier"] = identifier
            __props__.__dict__["org_id"] = org_id
            __props__.__dict__["project_id"] = project_id
            if service_id is None and not opts.urn:
                raise TypeError("Missing required property 'service_id'")
            __props__.__dict__["service_id"] = service_id
            if yaml is None and not opts.urn:
                raise TypeError("Missing required property 'yaml'")
            __props__.__dict__["yaml"] = yaml
        super(EnvironmentServiceOverrides, __self__).__init__(
            'harness:platform/environmentServiceOverrides:EnvironmentServiceOverrides',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            env_id: Optional[pulumi.Input[str]] = None,
            identifier: Optional[pulumi.Input[str]] = None,
            org_id: Optional[pulumi.Input[str]] = None,
            project_id: Optional[pulumi.Input[str]] = None,
            service_id: Optional[pulumi.Input[str]] = None,
            yaml: Optional[pulumi.Input[str]] = None) -> 'EnvironmentServiceOverrides':
        """
        Get an existing EnvironmentServiceOverrides resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] env_id: The env Id associated with the overrides. To reference an environment at the organization scope, prefix 'org' to the expression: org.{env*id}. To reference an environment at the account scope, prefix 'account' to the expression: account.{env*id}).
        :param pulumi.Input[str] identifier: identifier of the service overrides.
        :param pulumi.Input[str] org_id: Unique identifier of the organization.
        :param pulumi.Input[str] project_id: Unique identifier of the project.
        :param pulumi.Input[str] service_id: The service Id associated with the overrides. To reference a service at the organization scope, prefix 'org' to the expression: org.{service*id}. To reference a service at the account scope, prefix 'account' to the expression: account.{service*id}).
        :param pulumi.Input[str] yaml: Environment Service Overrides YAML. In YAML, to reference an entity at the organization scope, prefix 'org' to the expression: org.{identifier}. To reference an entity at the account scope, prefix 'account` to the expression: account.{identifier}. For eg, to reference a connector with identifier 'connectorId' at the organization scope in a stage mention it as connectorRef: org.connectorId.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _EnvironmentServiceOverridesState.__new__(_EnvironmentServiceOverridesState)

        __props__.__dict__["env_id"] = env_id
        __props__.__dict__["identifier"] = identifier
        __props__.__dict__["org_id"] = org_id
        __props__.__dict__["project_id"] = project_id
        __props__.__dict__["service_id"] = service_id
        __props__.__dict__["yaml"] = yaml
        return EnvironmentServiceOverrides(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="envId")
    def env_id(self) -> pulumi.Output[str]:
        """
        The env Id associated with the overrides. To reference an environment at the organization scope, prefix 'org' to the expression: org.{env*id}. To reference an environment at the account scope, prefix 'account' to the expression: account.{env*id}).
        """
        return pulumi.get(self, "env_id")

    @property
    @pulumi.getter
    def identifier(self) -> pulumi.Output[str]:
        """
        identifier of the service overrides.
        """
        return pulumi.get(self, "identifier")

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
    @pulumi.getter(name="serviceId")
    def service_id(self) -> pulumi.Output[str]:
        """
        The service Id associated with the overrides. To reference a service at the organization scope, prefix 'org' to the expression: org.{service*id}. To reference a service at the account scope, prefix 'account' to the expression: account.{service*id}).
        """
        return pulumi.get(self, "service_id")

    @property
    @pulumi.getter
    def yaml(self) -> pulumi.Output[str]:
        """
        Environment Service Overrides YAML. In YAML, to reference an entity at the organization scope, prefix 'org' to the expression: org.{identifier}. To reference an entity at the account scope, prefix 'account` to the expression: account.{identifier}. For eg, to reference a connector with identifier 'connectorId' at the organization scope in a stage mention it as connectorRef: org.connectorId.
        """
        return pulumi.get(self, "yaml")


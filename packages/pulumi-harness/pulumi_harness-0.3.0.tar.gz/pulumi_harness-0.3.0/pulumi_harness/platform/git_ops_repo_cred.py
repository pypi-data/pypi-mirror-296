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

__all__ = ['GitOpsRepoCredArgs', 'GitOpsRepoCred']

@pulumi.input_type
class GitOpsRepoCredArgs:
    def __init__(__self__, *,
                 account_id: pulumi.Input[str],
                 agent_id: pulumi.Input[str],
                 identifier: pulumi.Input[str],
                 creds: Optional[pulumi.Input[Sequence[pulumi.Input['GitOpsRepoCredCredArgs']]]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 upsert: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a GitOpsRepoCred resource.
        :param pulumi.Input[str] account_id: Account identifier of the Repository Credentials.
        :param pulumi.Input[str] agent_id: Agent identifier of the Repository Credentials.
        :param pulumi.Input[str] identifier: Identifier of the Repository Credentials.
        :param pulumi.Input[Sequence[pulumi.Input['GitOpsRepoCredCredArgs']]] creds: credential details.
        :param pulumi.Input[str] org_id: Organization identifier of the Repository Credentials.
        :param pulumi.Input[str] project_id: Project identifier of the Repository Credentials.
        :param pulumi.Input[bool] upsert: Indicates if the GitOps repository credential should be updated if existing and inserted if not.
        """
        pulumi.set(__self__, "account_id", account_id)
        pulumi.set(__self__, "agent_id", agent_id)
        pulumi.set(__self__, "identifier", identifier)
        if creds is not None:
            pulumi.set(__self__, "creds", creds)
        if org_id is not None:
            pulumi.set(__self__, "org_id", org_id)
        if project_id is not None:
            pulumi.set(__self__, "project_id", project_id)
        if upsert is not None:
            pulumi.set(__self__, "upsert", upsert)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> pulumi.Input[str]:
        """
        Account identifier of the Repository Credentials.
        """
        return pulumi.get(self, "account_id")

    @account_id.setter
    def account_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "account_id", value)

    @property
    @pulumi.getter(name="agentId")
    def agent_id(self) -> pulumi.Input[str]:
        """
        Agent identifier of the Repository Credentials.
        """
        return pulumi.get(self, "agent_id")

    @agent_id.setter
    def agent_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "agent_id", value)

    @property
    @pulumi.getter
    def identifier(self) -> pulumi.Input[str]:
        """
        Identifier of the Repository Credentials.
        """
        return pulumi.get(self, "identifier")

    @identifier.setter
    def identifier(self, value: pulumi.Input[str]):
        pulumi.set(self, "identifier", value)

    @property
    @pulumi.getter
    def creds(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['GitOpsRepoCredCredArgs']]]]:
        """
        credential details.
        """
        return pulumi.get(self, "creds")

    @creds.setter
    def creds(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['GitOpsRepoCredCredArgs']]]]):
        pulumi.set(self, "creds", value)

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> Optional[pulumi.Input[str]]:
        """
        Organization identifier of the Repository Credentials.
        """
        return pulumi.get(self, "org_id")

    @org_id.setter
    def org_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "org_id", value)

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> Optional[pulumi.Input[str]]:
        """
        Project identifier of the Repository Credentials.
        """
        return pulumi.get(self, "project_id")

    @project_id.setter
    def project_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project_id", value)

    @property
    @pulumi.getter
    def upsert(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates if the GitOps repository credential should be updated if existing and inserted if not.
        """
        return pulumi.get(self, "upsert")

    @upsert.setter
    def upsert(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "upsert", value)


@pulumi.input_type
class _GitOpsRepoCredState:
    def __init__(__self__, *,
                 account_id: Optional[pulumi.Input[str]] = None,
                 agent_id: Optional[pulumi.Input[str]] = None,
                 creds: Optional[pulumi.Input[Sequence[pulumi.Input['GitOpsRepoCredCredArgs']]]] = None,
                 identifier: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 upsert: Optional[pulumi.Input[bool]] = None):
        """
        Input properties used for looking up and filtering GitOpsRepoCred resources.
        :param pulumi.Input[str] account_id: Account identifier of the Repository Credentials.
        :param pulumi.Input[str] agent_id: Agent identifier of the Repository Credentials.
        :param pulumi.Input[Sequence[pulumi.Input['GitOpsRepoCredCredArgs']]] creds: credential details.
        :param pulumi.Input[str] identifier: Identifier of the Repository Credentials.
        :param pulumi.Input[str] org_id: Organization identifier of the Repository Credentials.
        :param pulumi.Input[str] project_id: Project identifier of the Repository Credentials.
        :param pulumi.Input[bool] upsert: Indicates if the GitOps repository credential should be updated if existing and inserted if not.
        """
        if account_id is not None:
            pulumi.set(__self__, "account_id", account_id)
        if agent_id is not None:
            pulumi.set(__self__, "agent_id", agent_id)
        if creds is not None:
            pulumi.set(__self__, "creds", creds)
        if identifier is not None:
            pulumi.set(__self__, "identifier", identifier)
        if org_id is not None:
            pulumi.set(__self__, "org_id", org_id)
        if project_id is not None:
            pulumi.set(__self__, "project_id", project_id)
        if upsert is not None:
            pulumi.set(__self__, "upsert", upsert)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> Optional[pulumi.Input[str]]:
        """
        Account identifier of the Repository Credentials.
        """
        return pulumi.get(self, "account_id")

    @account_id.setter
    def account_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "account_id", value)

    @property
    @pulumi.getter(name="agentId")
    def agent_id(self) -> Optional[pulumi.Input[str]]:
        """
        Agent identifier of the Repository Credentials.
        """
        return pulumi.get(self, "agent_id")

    @agent_id.setter
    def agent_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "agent_id", value)

    @property
    @pulumi.getter
    def creds(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['GitOpsRepoCredCredArgs']]]]:
        """
        credential details.
        """
        return pulumi.get(self, "creds")

    @creds.setter
    def creds(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['GitOpsRepoCredCredArgs']]]]):
        pulumi.set(self, "creds", value)

    @property
    @pulumi.getter
    def identifier(self) -> Optional[pulumi.Input[str]]:
        """
        Identifier of the Repository Credentials.
        """
        return pulumi.get(self, "identifier")

    @identifier.setter
    def identifier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "identifier", value)

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> Optional[pulumi.Input[str]]:
        """
        Organization identifier of the Repository Credentials.
        """
        return pulumi.get(self, "org_id")

    @org_id.setter
    def org_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "org_id", value)

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> Optional[pulumi.Input[str]]:
        """
        Project identifier of the Repository Credentials.
        """
        return pulumi.get(self, "project_id")

    @project_id.setter
    def project_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project_id", value)

    @property
    @pulumi.getter
    def upsert(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates if the GitOps repository credential should be updated if existing and inserted if not.
        """
        return pulumi.get(self, "upsert")

    @upsert.setter
    def upsert(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "upsert", value)


class GitOpsRepoCred(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_id: Optional[pulumi.Input[str]] = None,
                 agent_id: Optional[pulumi.Input[str]] = None,
                 creds: Optional[pulumi.Input[Sequence[pulumi.Input[Union['GitOpsRepoCredCredArgs', 'GitOpsRepoCredCredArgsDict']]]]] = None,
                 identifier: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 upsert: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        Resource for managing a Harness Gitops Repository Credentials.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_harness as harness

        test = harness.platform.GitOpsRepoCred("test",
            identifier="identifier",
            account_id="account_id",
            agent_id="agent_id",
            project_id="project_id",
            org_id="org_id",
            creds=[{
                "type": "git",
                "url": "git@github.com:yourorg",
                "ssh_private_key": \"\"\"----- BEGIN OPENSSH PRIVATE KEY-----
        XXXXX
        XXXXX
        XXXXX
        -----END OPENSSH PRIVATE KEY -----
        \"\"\",
            }])
        ```

        ## Import

        Import an Account level Gitops Repository Credentials

        ```sh
        $ pulumi import harness:platform/gitOpsRepoCred:GitOpsRepoCred example <agent_id>/<repocred_id>
        ```

        Import an Org level Gitops Repository Credentials

        ```sh
        $ pulumi import harness:platform/gitOpsRepoCred:GitOpsRepoCred example <organization_id>/<agent_id>/<repocred_id>
        ```

        Import a Project level Gitops Repository Credentials

        ```sh
        $ pulumi import harness:platform/gitOpsRepoCred:GitOpsRepoCred example <organization_id>/<project_id>/<agent_id>/<repocred_id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_id: Account identifier of the Repository Credentials.
        :param pulumi.Input[str] agent_id: Agent identifier of the Repository Credentials.
        :param pulumi.Input[Sequence[pulumi.Input[Union['GitOpsRepoCredCredArgs', 'GitOpsRepoCredCredArgsDict']]]] creds: credential details.
        :param pulumi.Input[str] identifier: Identifier of the Repository Credentials.
        :param pulumi.Input[str] org_id: Organization identifier of the Repository Credentials.
        :param pulumi.Input[str] project_id: Project identifier of the Repository Credentials.
        :param pulumi.Input[bool] upsert: Indicates if the GitOps repository credential should be updated if existing and inserted if not.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: GitOpsRepoCredArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource for managing a Harness Gitops Repository Credentials.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_harness as harness

        test = harness.platform.GitOpsRepoCred("test",
            identifier="identifier",
            account_id="account_id",
            agent_id="agent_id",
            project_id="project_id",
            org_id="org_id",
            creds=[{
                "type": "git",
                "url": "git@github.com:yourorg",
                "ssh_private_key": \"\"\"----- BEGIN OPENSSH PRIVATE KEY-----
        XXXXX
        XXXXX
        XXXXX
        -----END OPENSSH PRIVATE KEY -----
        \"\"\",
            }])
        ```

        ## Import

        Import an Account level Gitops Repository Credentials

        ```sh
        $ pulumi import harness:platform/gitOpsRepoCred:GitOpsRepoCred example <agent_id>/<repocred_id>
        ```

        Import an Org level Gitops Repository Credentials

        ```sh
        $ pulumi import harness:platform/gitOpsRepoCred:GitOpsRepoCred example <organization_id>/<agent_id>/<repocred_id>
        ```

        Import a Project level Gitops Repository Credentials

        ```sh
        $ pulumi import harness:platform/gitOpsRepoCred:GitOpsRepoCred example <organization_id>/<project_id>/<agent_id>/<repocred_id>
        ```

        :param str resource_name: The name of the resource.
        :param GitOpsRepoCredArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(GitOpsRepoCredArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_id: Optional[pulumi.Input[str]] = None,
                 agent_id: Optional[pulumi.Input[str]] = None,
                 creds: Optional[pulumi.Input[Sequence[pulumi.Input[Union['GitOpsRepoCredCredArgs', 'GitOpsRepoCredCredArgsDict']]]]] = None,
                 identifier: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 upsert: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = GitOpsRepoCredArgs.__new__(GitOpsRepoCredArgs)

            if account_id is None and not opts.urn:
                raise TypeError("Missing required property 'account_id'")
            __props__.__dict__["account_id"] = account_id
            if agent_id is None and not opts.urn:
                raise TypeError("Missing required property 'agent_id'")
            __props__.__dict__["agent_id"] = agent_id
            __props__.__dict__["creds"] = creds
            if identifier is None and not opts.urn:
                raise TypeError("Missing required property 'identifier'")
            __props__.__dict__["identifier"] = identifier
            __props__.__dict__["org_id"] = org_id
            __props__.__dict__["project_id"] = project_id
            __props__.__dict__["upsert"] = upsert
        super(GitOpsRepoCred, __self__).__init__(
            'harness:platform/gitOpsRepoCred:GitOpsRepoCred',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            account_id: Optional[pulumi.Input[str]] = None,
            agent_id: Optional[pulumi.Input[str]] = None,
            creds: Optional[pulumi.Input[Sequence[pulumi.Input[Union['GitOpsRepoCredCredArgs', 'GitOpsRepoCredCredArgsDict']]]]] = None,
            identifier: Optional[pulumi.Input[str]] = None,
            org_id: Optional[pulumi.Input[str]] = None,
            project_id: Optional[pulumi.Input[str]] = None,
            upsert: Optional[pulumi.Input[bool]] = None) -> 'GitOpsRepoCred':
        """
        Get an existing GitOpsRepoCred resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_id: Account identifier of the Repository Credentials.
        :param pulumi.Input[str] agent_id: Agent identifier of the Repository Credentials.
        :param pulumi.Input[Sequence[pulumi.Input[Union['GitOpsRepoCredCredArgs', 'GitOpsRepoCredCredArgsDict']]]] creds: credential details.
        :param pulumi.Input[str] identifier: Identifier of the Repository Credentials.
        :param pulumi.Input[str] org_id: Organization identifier of the Repository Credentials.
        :param pulumi.Input[str] project_id: Project identifier of the Repository Credentials.
        :param pulumi.Input[bool] upsert: Indicates if the GitOps repository credential should be updated if existing and inserted if not.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _GitOpsRepoCredState.__new__(_GitOpsRepoCredState)

        __props__.__dict__["account_id"] = account_id
        __props__.__dict__["agent_id"] = agent_id
        __props__.__dict__["creds"] = creds
        __props__.__dict__["identifier"] = identifier
        __props__.__dict__["org_id"] = org_id
        __props__.__dict__["project_id"] = project_id
        __props__.__dict__["upsert"] = upsert
        return GitOpsRepoCred(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> pulumi.Output[str]:
        """
        Account identifier of the Repository Credentials.
        """
        return pulumi.get(self, "account_id")

    @property
    @pulumi.getter(name="agentId")
    def agent_id(self) -> pulumi.Output[str]:
        """
        Agent identifier of the Repository Credentials.
        """
        return pulumi.get(self, "agent_id")

    @property
    @pulumi.getter
    def creds(self) -> pulumi.Output[Sequence['outputs.GitOpsRepoCredCred']]:
        """
        credential details.
        """
        return pulumi.get(self, "creds")

    @property
    @pulumi.getter
    def identifier(self) -> pulumi.Output[str]:
        """
        Identifier of the Repository Credentials.
        """
        return pulumi.get(self, "identifier")

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> pulumi.Output[Optional[str]]:
        """
        Organization identifier of the Repository Credentials.
        """
        return pulumi.get(self, "org_id")

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> pulumi.Output[Optional[str]]:
        """
        Project identifier of the Repository Credentials.
        """
        return pulumi.get(self, "project_id")

    @property
    @pulumi.getter
    def upsert(self) -> pulumi.Output[Optional[bool]]:
        """
        Indicates if the GitOps repository credential should be updated if existing and inserted if not.
        """
        return pulumi.get(self, "upsert")


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
    'AwsAssumeCrossAccountRole',
    'AwsUsageScope',
    'DatacenterUsageScope',
    'GcpUsageScope',
    'KubernetesAuthentication',
    'KubernetesAuthenticationOidc',
    'KubernetesAuthenticationServiceAccount',
    'KubernetesAuthenticationUsernamePassword',
    'KubernetesUsageScope',
]

@pulumi.output_type
class AwsAssumeCrossAccountRole(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "roleArn":
            suggest = "role_arn"
        elif key == "externalId":
            suggest = "external_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AwsAssumeCrossAccountRole. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AwsAssumeCrossAccountRole.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AwsAssumeCrossAccountRole.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 role_arn: str,
                 external_id: Optional[str] = None):
        """
        :param str role_arn: This is an IAM role in the target deployment AWS account.
        :param str external_id: If the administrator of the account to which the role belongs provided you with an external ID, then enter that value.
        """
        pulumi.set(__self__, "role_arn", role_arn)
        if external_id is not None:
            pulumi.set(__self__, "external_id", external_id)

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> str:
        """
        This is an IAM role in the target deployment AWS account.
        """
        return pulumi.get(self, "role_arn")

    @property
    @pulumi.getter(name="externalId")
    def external_id(self) -> Optional[str]:
        """
        If the administrator of the account to which the role belongs provided you with an external ID, then enter that value.
        """
        return pulumi.get(self, "external_id")


@pulumi.output_type
class AwsUsageScope(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "applicationId":
            suggest = "application_id"
        elif key == "environmentFilterType":
            suggest = "environment_filter_type"
        elif key == "environmentId":
            suggest = "environment_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AwsUsageScope. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AwsUsageScope.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AwsUsageScope.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 application_id: Optional[str] = None,
                 environment_filter_type: Optional[str] = None,
                 environment_id: Optional[str] = None):
        """
        :param str application_id: Id of the application to scope to. If empty then this scope applies to all applications.
        :param str environment_filter_type: Type of environment filter applied. Cannot be used with `environment_id`. Valid options are NON*PRODUCTION*ENVIRONMENTS, PRODUCTION_ENVIRONMENTS.
        :param str environment_id: Id of the id of the specific environment to scope to. Cannot be used with `environment_filter_type`.
        """
        if application_id is not None:
            pulumi.set(__self__, "application_id", application_id)
        if environment_filter_type is not None:
            pulumi.set(__self__, "environment_filter_type", environment_filter_type)
        if environment_id is not None:
            pulumi.set(__self__, "environment_id", environment_id)

    @property
    @pulumi.getter(name="applicationId")
    def application_id(self) -> Optional[str]:
        """
        Id of the application to scope to. If empty then this scope applies to all applications.
        """
        return pulumi.get(self, "application_id")

    @property
    @pulumi.getter(name="environmentFilterType")
    def environment_filter_type(self) -> Optional[str]:
        """
        Type of environment filter applied. Cannot be used with `environment_id`. Valid options are NON*PRODUCTION*ENVIRONMENTS, PRODUCTION_ENVIRONMENTS.
        """
        return pulumi.get(self, "environment_filter_type")

    @property
    @pulumi.getter(name="environmentId")
    def environment_id(self) -> Optional[str]:
        """
        Id of the id of the specific environment to scope to. Cannot be used with `environment_filter_type`.
        """
        return pulumi.get(self, "environment_id")


@pulumi.output_type
class DatacenterUsageScope(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "applicationId":
            suggest = "application_id"
        elif key == "environmentFilterType":
            suggest = "environment_filter_type"
        elif key == "environmentId":
            suggest = "environment_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in DatacenterUsageScope. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        DatacenterUsageScope.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        DatacenterUsageScope.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 application_id: Optional[str] = None,
                 environment_filter_type: Optional[str] = None,
                 environment_id: Optional[str] = None):
        """
        :param str application_id: Id of the application to scope to. If empty then this scope applies to all applications.
        :param str environment_filter_type: Type of environment filter applied. Cannot be used with `environment_id`. Valid options are NON*PRODUCTION*ENVIRONMENTS, PRODUCTION_ENVIRONMENTS.
        :param str environment_id: Id of the id of the specific environment to scope to. Cannot be used with `environment_filter_type`.
        """
        if application_id is not None:
            pulumi.set(__self__, "application_id", application_id)
        if environment_filter_type is not None:
            pulumi.set(__self__, "environment_filter_type", environment_filter_type)
        if environment_id is not None:
            pulumi.set(__self__, "environment_id", environment_id)

    @property
    @pulumi.getter(name="applicationId")
    def application_id(self) -> Optional[str]:
        """
        Id of the application to scope to. If empty then this scope applies to all applications.
        """
        return pulumi.get(self, "application_id")

    @property
    @pulumi.getter(name="environmentFilterType")
    def environment_filter_type(self) -> Optional[str]:
        """
        Type of environment filter applied. Cannot be used with `environment_id`. Valid options are NON*PRODUCTION*ENVIRONMENTS, PRODUCTION_ENVIRONMENTS.
        """
        return pulumi.get(self, "environment_filter_type")

    @property
    @pulumi.getter(name="environmentId")
    def environment_id(self) -> Optional[str]:
        """
        Id of the id of the specific environment to scope to. Cannot be used with `environment_filter_type`.
        """
        return pulumi.get(self, "environment_id")


@pulumi.output_type
class GcpUsageScope(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "applicationId":
            suggest = "application_id"
        elif key == "environmentFilterType":
            suggest = "environment_filter_type"
        elif key == "environmentId":
            suggest = "environment_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in GcpUsageScope. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        GcpUsageScope.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        GcpUsageScope.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 application_id: Optional[str] = None,
                 environment_filter_type: Optional[str] = None,
                 environment_id: Optional[str] = None):
        """
        :param str application_id: Id of the application to scope to. If empty then this scope applies to all applications.
        :param str environment_filter_type: Type of environment filter applied. Cannot be used with `environment_id`. Valid options are NON*PRODUCTION*ENVIRONMENTS, PRODUCTION_ENVIRONMENTS.
        :param str environment_id: Id of the id of the specific environment to scope to. Cannot be used with `environment_filter_type`.
        """
        if application_id is not None:
            pulumi.set(__self__, "application_id", application_id)
        if environment_filter_type is not None:
            pulumi.set(__self__, "environment_filter_type", environment_filter_type)
        if environment_id is not None:
            pulumi.set(__self__, "environment_id", environment_id)

    @property
    @pulumi.getter(name="applicationId")
    def application_id(self) -> Optional[str]:
        """
        Id of the application to scope to. If empty then this scope applies to all applications.
        """
        return pulumi.get(self, "application_id")

    @property
    @pulumi.getter(name="environmentFilterType")
    def environment_filter_type(self) -> Optional[str]:
        """
        Type of environment filter applied. Cannot be used with `environment_id`. Valid options are NON*PRODUCTION*ENVIRONMENTS, PRODUCTION_ENVIRONMENTS.
        """
        return pulumi.get(self, "environment_filter_type")

    @property
    @pulumi.getter(name="environmentId")
    def environment_id(self) -> Optional[str]:
        """
        Id of the id of the specific environment to scope to. Cannot be used with `environment_filter_type`.
        """
        return pulumi.get(self, "environment_id")


@pulumi.output_type
class KubernetesAuthentication(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "delegateSelectors":
            suggest = "delegate_selectors"
        elif key == "serviceAccount":
            suggest = "service_account"
        elif key == "usernamePassword":
            suggest = "username_password"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in KubernetesAuthentication. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        KubernetesAuthentication.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        KubernetesAuthentication.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 delegate_selectors: Optional[Sequence[str]] = None,
                 oidc: Optional['outputs.KubernetesAuthenticationOidc'] = None,
                 service_account: Optional['outputs.KubernetesAuthenticationServiceAccount'] = None,
                 username_password: Optional['outputs.KubernetesAuthenticationUsernamePassword'] = None):
        """
        :param Sequence[str] delegate_selectors: Delegate selectors to inherit the GCP credentials from.
        :param 'KubernetesAuthenticationOidcArgs' oidc: Service account configuration for connecting to the Kubernetes cluster
        :param 'KubernetesAuthenticationServiceAccountArgs' service_account: Username and password for authentication to the cluster
        :param 'KubernetesAuthenticationUsernamePasswordArgs' username_password: Username and password for authentication to the cluster
        """
        if delegate_selectors is not None:
            pulumi.set(__self__, "delegate_selectors", delegate_selectors)
        if oidc is not None:
            pulumi.set(__self__, "oidc", oidc)
        if service_account is not None:
            pulumi.set(__self__, "service_account", service_account)
        if username_password is not None:
            pulumi.set(__self__, "username_password", username_password)

    @property
    @pulumi.getter(name="delegateSelectors")
    def delegate_selectors(self) -> Optional[Sequence[str]]:
        """
        Delegate selectors to inherit the GCP credentials from.
        """
        return pulumi.get(self, "delegate_selectors")

    @property
    @pulumi.getter
    def oidc(self) -> Optional['outputs.KubernetesAuthenticationOidc']:
        """
        Service account configuration for connecting to the Kubernetes cluster
        """
        return pulumi.get(self, "oidc")

    @property
    @pulumi.getter(name="serviceAccount")
    def service_account(self) -> Optional['outputs.KubernetesAuthenticationServiceAccount']:
        """
        Username and password for authentication to the cluster
        """
        return pulumi.get(self, "service_account")

    @property
    @pulumi.getter(name="usernamePassword")
    def username_password(self) -> Optional['outputs.KubernetesAuthenticationUsernamePassword']:
        """
        Username and password for authentication to the cluster
        """
        return pulumi.get(self, "username_password")


@pulumi.output_type
class KubernetesAuthenticationOidc(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "clientIdSecretName":
            suggest = "client_id_secret_name"
        elif key == "identityProviderUrl":
            suggest = "identity_provider_url"
        elif key == "masterUrl":
            suggest = "master_url"
        elif key == "passwordSecretName":
            suggest = "password_secret_name"
        elif key == "clientSecretSecretName":
            suggest = "client_secret_secret_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in KubernetesAuthenticationOidc. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        KubernetesAuthenticationOidc.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        KubernetesAuthenticationOidc.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 client_id_secret_name: str,
                 identity_provider_url: str,
                 master_url: str,
                 password_secret_name: str,
                 username: str,
                 client_secret_secret_name: Optional[str] = None,
                 scopes: Optional[Sequence[str]] = None):
        """
        :param str client_id_secret_name: Name of the Harness secret containing the client ID for the cluster.
        :param str identity_provider_url: URL of the identity provider to use.
        :param str master_url: URL of the Kubernetes master to connect to.
        :param str password_secret_name: Name of the Harness secret containing the password for the cluster.
        :param str username: Username for authentication to the cluster. This can be the username itself or the ID of a harness secret.
        :param str client_secret_secret_name: Name of the Harness secret containing the client secret for the cluster.
        :param Sequence[str] scopes: Scopes to request from the identity provider.
        """
        pulumi.set(__self__, "client_id_secret_name", client_id_secret_name)
        pulumi.set(__self__, "identity_provider_url", identity_provider_url)
        pulumi.set(__self__, "master_url", master_url)
        pulumi.set(__self__, "password_secret_name", password_secret_name)
        pulumi.set(__self__, "username", username)
        if client_secret_secret_name is not None:
            pulumi.set(__self__, "client_secret_secret_name", client_secret_secret_name)
        if scopes is not None:
            pulumi.set(__self__, "scopes", scopes)

    @property
    @pulumi.getter(name="clientIdSecretName")
    def client_id_secret_name(self) -> str:
        """
        Name of the Harness secret containing the client ID for the cluster.
        """
        return pulumi.get(self, "client_id_secret_name")

    @property
    @pulumi.getter(name="identityProviderUrl")
    def identity_provider_url(self) -> str:
        """
        URL of the identity provider to use.
        """
        return pulumi.get(self, "identity_provider_url")

    @property
    @pulumi.getter(name="masterUrl")
    def master_url(self) -> str:
        """
        URL of the Kubernetes master to connect to.
        """
        return pulumi.get(self, "master_url")

    @property
    @pulumi.getter(name="passwordSecretName")
    def password_secret_name(self) -> str:
        """
        Name of the Harness secret containing the password for the cluster.
        """
        return pulumi.get(self, "password_secret_name")

    @property
    @pulumi.getter
    def username(self) -> str:
        """
        Username for authentication to the cluster. This can be the username itself or the ID of a harness secret.
        """
        return pulumi.get(self, "username")

    @property
    @pulumi.getter(name="clientSecretSecretName")
    def client_secret_secret_name(self) -> Optional[str]:
        """
        Name of the Harness secret containing the client secret for the cluster.
        """
        return pulumi.get(self, "client_secret_secret_name")

    @property
    @pulumi.getter
    def scopes(self) -> Optional[Sequence[str]]:
        """
        Scopes to request from the identity provider.
        """
        return pulumi.get(self, "scopes")


@pulumi.output_type
class KubernetesAuthenticationServiceAccount(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "masterUrl":
            suggest = "master_url"
        elif key == "serviceAccountTokenSecretName":
            suggest = "service_account_token_secret_name"
        elif key == "caCertificateSecretName":
            suggest = "ca_certificate_secret_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in KubernetesAuthenticationServiceAccount. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        KubernetesAuthenticationServiceAccount.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        KubernetesAuthenticationServiceAccount.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 master_url: str,
                 service_account_token_secret_name: str,
                 ca_certificate_secret_name: Optional[str] = None):
        """
        :param str master_url: URL of the Kubernetes master to connect to.
        :param str service_account_token_secret_name: Name of the Harness secret containing the service account token for the cluster.
        :param str ca_certificate_secret_name: Name of the Harness secret containing the CA certificate for the cluster.
        """
        pulumi.set(__self__, "master_url", master_url)
        pulumi.set(__self__, "service_account_token_secret_name", service_account_token_secret_name)
        if ca_certificate_secret_name is not None:
            pulumi.set(__self__, "ca_certificate_secret_name", ca_certificate_secret_name)

    @property
    @pulumi.getter(name="masterUrl")
    def master_url(self) -> str:
        """
        URL of the Kubernetes master to connect to.
        """
        return pulumi.get(self, "master_url")

    @property
    @pulumi.getter(name="serviceAccountTokenSecretName")
    def service_account_token_secret_name(self) -> str:
        """
        Name of the Harness secret containing the service account token for the cluster.
        """
        return pulumi.get(self, "service_account_token_secret_name")

    @property
    @pulumi.getter(name="caCertificateSecretName")
    def ca_certificate_secret_name(self) -> Optional[str]:
        """
        Name of the Harness secret containing the CA certificate for the cluster.
        """
        return pulumi.get(self, "ca_certificate_secret_name")


@pulumi.output_type
class KubernetesAuthenticationUsernamePassword(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "masterUrl":
            suggest = "master_url"
        elif key == "passwordSecretName":
            suggest = "password_secret_name"
        elif key == "usernameSecretName":
            suggest = "username_secret_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in KubernetesAuthenticationUsernamePassword. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        KubernetesAuthenticationUsernamePassword.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        KubernetesAuthenticationUsernamePassword.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 master_url: str,
                 password_secret_name: str,
                 username: Optional[str] = None,
                 username_secret_name: Optional[str] = None):
        """
        :param str master_url: URL of the Kubernetes master to connect to.
        :param str password_secret_name: Name of the Harness secret containing the password for the cluster.
        :param str username: Username for authentication to the cluster
        :param str username_secret_name: Name of the Harness secret containing the username for authentication to the cluster
        """
        pulumi.set(__self__, "master_url", master_url)
        pulumi.set(__self__, "password_secret_name", password_secret_name)
        if username is not None:
            pulumi.set(__self__, "username", username)
        if username_secret_name is not None:
            pulumi.set(__self__, "username_secret_name", username_secret_name)

    @property
    @pulumi.getter(name="masterUrl")
    def master_url(self) -> str:
        """
        URL of the Kubernetes master to connect to.
        """
        return pulumi.get(self, "master_url")

    @property
    @pulumi.getter(name="passwordSecretName")
    def password_secret_name(self) -> str:
        """
        Name of the Harness secret containing the password for the cluster.
        """
        return pulumi.get(self, "password_secret_name")

    @property
    @pulumi.getter
    def username(self) -> Optional[str]:
        """
        Username for authentication to the cluster
        """
        return pulumi.get(self, "username")

    @property
    @pulumi.getter(name="usernameSecretName")
    def username_secret_name(self) -> Optional[str]:
        """
        Name of the Harness secret containing the username for authentication to the cluster
        """
        return pulumi.get(self, "username_secret_name")


@pulumi.output_type
class KubernetesUsageScope(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "applicationId":
            suggest = "application_id"
        elif key == "environmentFilterType":
            suggest = "environment_filter_type"
        elif key == "environmentId":
            suggest = "environment_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in KubernetesUsageScope. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        KubernetesUsageScope.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        KubernetesUsageScope.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 application_id: Optional[str] = None,
                 environment_filter_type: Optional[str] = None,
                 environment_id: Optional[str] = None):
        """
        :param str application_id: Id of the application to scope to. If empty then this scope applies to all applications.
        :param str environment_filter_type: Type of environment filter applied. Cannot be used with `environment_id`. Valid options are NON*PRODUCTION*ENVIRONMENTS, PRODUCTION_ENVIRONMENTS.
        :param str environment_id: Id of the id of the specific environment to scope to. Cannot be used with `environment_filter_type`.
        """
        if application_id is not None:
            pulumi.set(__self__, "application_id", application_id)
        if environment_filter_type is not None:
            pulumi.set(__self__, "environment_filter_type", environment_filter_type)
        if environment_id is not None:
            pulumi.set(__self__, "environment_id", environment_id)

    @property
    @pulumi.getter(name="applicationId")
    def application_id(self) -> Optional[str]:
        """
        Id of the application to scope to. If empty then this scope applies to all applications.
        """
        return pulumi.get(self, "application_id")

    @property
    @pulumi.getter(name="environmentFilterType")
    def environment_filter_type(self) -> Optional[str]:
        """
        Type of environment filter applied. Cannot be used with `environment_id`. Valid options are NON*PRODUCTION*ENVIRONMENTS, PRODUCTION_ENVIRONMENTS.
        """
        return pulumi.get(self, "environment_filter_type")

    @property
    @pulumi.getter(name="environmentId")
    def environment_id(self) -> Optional[str]:
        """
        Id of the id of the specific environment to scope to. Cannot be used with `environment_filter_type`.
        """
        return pulumi.get(self, "environment_id")



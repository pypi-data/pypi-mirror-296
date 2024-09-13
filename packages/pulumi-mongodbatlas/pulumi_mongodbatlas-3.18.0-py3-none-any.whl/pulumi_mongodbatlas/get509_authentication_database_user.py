# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
from . import outputs

__all__ = [
    'Get509AuthenticationDatabaseUserResult',
    'AwaitableGet509AuthenticationDatabaseUserResult',
    'get509_authentication_database_user',
    'get509_authentication_database_user_output',
]

warnings.warn("""mongodbatlas.index/get509authenticationdatabaseuser.get509AuthenticationDatabaseUser has been deprecated in favor of mongodbatlas.index/getx509authenticationdatabaseuser.getX509AuthenticationDatabaseUser""", DeprecationWarning)

@pulumi.output_type
class Get509AuthenticationDatabaseUserResult:
    """
    A collection of values returned by get509AuthenticationDatabaseUser.
    """
    def __init__(__self__, certificates=None, customer_x509_cas=None, id=None, project_id=None, username=None):
        if certificates and not isinstance(certificates, list):
            raise TypeError("Expected argument 'certificates' to be a list")
        pulumi.set(__self__, "certificates", certificates)
        if customer_x509_cas and not isinstance(customer_x509_cas, str):
            raise TypeError("Expected argument 'customer_x509_cas' to be a str")
        pulumi.set(__self__, "customer_x509_cas", customer_x509_cas)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if project_id and not isinstance(project_id, str):
            raise TypeError("Expected argument 'project_id' to be a str")
        pulumi.set(__self__, "project_id", project_id)
        if username and not isinstance(username, str):
            raise TypeError("Expected argument 'username' to be a str")
        pulumi.set(__self__, "username", username)

    @property
    @pulumi.getter
    def certificates(self) -> Sequence['outputs.Get509AuthenticationDatabaseUserCertificateResult']:
        """
        Array of objects where each details one unexpired database user certificate.
        """
        return pulumi.get(self, "certificates")

    @property
    @pulumi.getter(name="customerX509Cas")
    def customer_x509_cas(self) -> str:
        return pulumi.get(self, "customer_x509_cas")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> str:
        return pulumi.get(self, "project_id")

    @property
    @pulumi.getter
    def username(self) -> Optional[str]:
        return pulumi.get(self, "username")


class AwaitableGet509AuthenticationDatabaseUserResult(Get509AuthenticationDatabaseUserResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return Get509AuthenticationDatabaseUserResult(
            certificates=self.certificates,
            customer_x509_cas=self.customer_x509_cas,
            id=self.id,
            project_id=self.project_id,
            username=self.username)


def get509_authentication_database_user(project_id: Optional[str] = None,
                                        username: Optional[str] = None,
                                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGet509AuthenticationDatabaseUserResult:
    """
    ## # Data Source: X509AuthenticationDatabaseUser

    `X509AuthenticationDatabaseUser` describes a X509 Authentication Database User. This represents a X509 Authentication Database User.

    > **NOTE:** Groups and projects are synonymous terms. You may find group_id in the official documentation.

    ## Example Usage

    ### S

    ### Example Usage: Save a customer-managed X.509 configuration for an Atlas project
    ```python
    import pulumi
    import pulumi_mongodbatlas as mongodbatlas

    test_x509_authentication_database_user = mongodbatlas.X509AuthenticationDatabaseUser("test",
        project_id="<PROJECT-ID>",
        customer_x509_cas=\"\"\"-----BEGIN CERTIFICATE-----
    MIICmTCCAgICCQDZnHzklxsT9TANBgkqhkiG9w0BAQsFADCBkDELMAkGA1UEBhMC
    VVMxDjAMBgNVBAgMBVRleGFzMQ8wDQYDVQQHDAZBdXN0aW4xETAPBgNVBAoMCHRl
    c3QuY29tMQ0wCwYDVQQLDARUZXN0MREwDwYDVQQDDAh0ZXN0LmNvbTErMCkGCSqG
    SIb3DQEJARYcbWVsaXNzYS5wbHVua2V0dEBtb25nb2RiLmNvbTAeFw0yMDAyMDQy
    MDQ2MDFaFw0yMTAyMDMyMDQ2MDFaMIGQMQswCQYDVQQGEwJVUzEOMAwGA1UECAwF
    VGV4YXMxDzANBgNVBAcMBkF1c3RpbjERMA8GA1UECgwIdGVzdC5jb20xDTALBgNV
    BAsMBFRlc3QxETAPBgNVBAMMCHRlc3QuY29tMSswKQYJKoZIhvcNAQkBFhxtZWxp
    c3NhLnBsdW5rZXR0QG1vbmdvZGIuY29tMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCB
    iQKBgQCf1LRqr1zftzdYx2Aj9G76tb0noMPtj6faGLlPji1+m6Rn7RWD9L0ntWAr
    cURxvypa9jZ9MXFzDtLevvd3tHEmfrUT3ukNDX6+Jtc4kWm+Dh2A70Pd+deKZ2/O
    Fh8audEKAESGXnTbeJCeQa1XKlIkjqQHBNwES5h1b9vJtFoLJwIDAQABMA0GCSqG
    SIb3DQEBCwUAA4GBADMUncjEPV/MiZUcVNGmktP6BPmEqMXQWUDpdGW2+Tg2JtUA
    7MMILtepBkFzLO+GlpZxeAlXO0wxiNgEmCRONgh4+t2w3e7a8GFijYQ99FHrAC5A
    iul59bdl18gVqXia1Yeq/iK7Ohfy/Jwd7Hsm530elwkM/ZEkYDjBlZSXYdyz
    -----END CERTIFICATE-----"
    \"\"\")
    test = mongodbatlas.get_x509_authentication_database_user_output(project_id=test_x509_authentication_database_user.project_id)
    ```


    :param str project_id: Identifier for the Atlas project associated with the X.509 configuration.
    :param str username: Username of the database user to create a certificate for.
    """
    pulumi.log.warn("""get509_authentication_database_user is deprecated: mongodbatlas.index/get509authenticationdatabaseuser.get509AuthenticationDatabaseUser has been deprecated in favor of mongodbatlas.index/getx509authenticationdatabaseuser.getX509AuthenticationDatabaseUser""")
    __args__ = dict()
    __args__['projectId'] = project_id
    __args__['username'] = username
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('mongodbatlas:index/get509AuthenticationDatabaseUser:get509AuthenticationDatabaseUser', __args__, opts=opts, typ=Get509AuthenticationDatabaseUserResult).value

    return AwaitableGet509AuthenticationDatabaseUserResult(
        certificates=pulumi.get(__ret__, 'certificates'),
        customer_x509_cas=pulumi.get(__ret__, 'customer_x509_cas'),
        id=pulumi.get(__ret__, 'id'),
        project_id=pulumi.get(__ret__, 'project_id'),
        username=pulumi.get(__ret__, 'username'))


@_utilities.lift_output_func(get509_authentication_database_user)
def get509_authentication_database_user_output(project_id: Optional[pulumi.Input[str]] = None,
                                               username: Optional[pulumi.Input[Optional[str]]] = None,
                                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[Get509AuthenticationDatabaseUserResult]:
    """
    ## # Data Source: X509AuthenticationDatabaseUser

    `X509AuthenticationDatabaseUser` describes a X509 Authentication Database User. This represents a X509 Authentication Database User.

    > **NOTE:** Groups and projects are synonymous terms. You may find group_id in the official documentation.

    ## Example Usage

    ### S

    ### Example Usage: Save a customer-managed X.509 configuration for an Atlas project
    ```python
    import pulumi
    import pulumi_mongodbatlas as mongodbatlas

    test_x509_authentication_database_user = mongodbatlas.X509AuthenticationDatabaseUser("test",
        project_id="<PROJECT-ID>",
        customer_x509_cas=\"\"\"-----BEGIN CERTIFICATE-----
    MIICmTCCAgICCQDZnHzklxsT9TANBgkqhkiG9w0BAQsFADCBkDELMAkGA1UEBhMC
    VVMxDjAMBgNVBAgMBVRleGFzMQ8wDQYDVQQHDAZBdXN0aW4xETAPBgNVBAoMCHRl
    c3QuY29tMQ0wCwYDVQQLDARUZXN0MREwDwYDVQQDDAh0ZXN0LmNvbTErMCkGCSqG
    SIb3DQEJARYcbWVsaXNzYS5wbHVua2V0dEBtb25nb2RiLmNvbTAeFw0yMDAyMDQy
    MDQ2MDFaFw0yMTAyMDMyMDQ2MDFaMIGQMQswCQYDVQQGEwJVUzEOMAwGA1UECAwF
    VGV4YXMxDzANBgNVBAcMBkF1c3RpbjERMA8GA1UECgwIdGVzdC5jb20xDTALBgNV
    BAsMBFRlc3QxETAPBgNVBAMMCHRlc3QuY29tMSswKQYJKoZIhvcNAQkBFhxtZWxp
    c3NhLnBsdW5rZXR0QG1vbmdvZGIuY29tMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCB
    iQKBgQCf1LRqr1zftzdYx2Aj9G76tb0noMPtj6faGLlPji1+m6Rn7RWD9L0ntWAr
    cURxvypa9jZ9MXFzDtLevvd3tHEmfrUT3ukNDX6+Jtc4kWm+Dh2A70Pd+deKZ2/O
    Fh8audEKAESGXnTbeJCeQa1XKlIkjqQHBNwES5h1b9vJtFoLJwIDAQABMA0GCSqG
    SIb3DQEBCwUAA4GBADMUncjEPV/MiZUcVNGmktP6BPmEqMXQWUDpdGW2+Tg2JtUA
    7MMILtepBkFzLO+GlpZxeAlXO0wxiNgEmCRONgh4+t2w3e7a8GFijYQ99FHrAC5A
    iul59bdl18gVqXia1Yeq/iK7Ohfy/Jwd7Hsm530elwkM/ZEkYDjBlZSXYdyz
    -----END CERTIFICATE-----"
    \"\"\")
    test = mongodbatlas.get_x509_authentication_database_user_output(project_id=test_x509_authentication_database_user.project_id)
    ```


    :param str project_id: Identifier for the Atlas project associated with the X.509 configuration.
    :param str username: Username of the database user to create a certificate for.
    """
    pulumi.log.warn("""get509_authentication_database_user is deprecated: mongodbatlas.index/get509authenticationdatabaseuser.get509AuthenticationDatabaseUser has been deprecated in favor of mongodbatlas.index/getx509authenticationdatabaseuser.getX509AuthenticationDatabaseUser""")
    ...

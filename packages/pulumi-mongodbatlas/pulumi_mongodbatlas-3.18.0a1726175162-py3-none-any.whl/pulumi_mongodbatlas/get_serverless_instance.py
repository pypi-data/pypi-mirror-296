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
from ._inputs import *

__all__ = [
    'GetServerlessInstanceResult',
    'AwaitableGetServerlessInstanceResult',
    'get_serverless_instance',
    'get_serverless_instance_output',
]

@pulumi.output_type
class GetServerlessInstanceResult:
    """
    A collection of values returned by getServerlessInstance.
    """
    def __init__(__self__, auto_indexing=None, connection_strings_private_endpoint_srvs=None, connection_strings_standard_srv=None, continuous_backup_enabled=None, create_date=None, id=None, links=None, mongo_db_version=None, name=None, project_id=None, provider_settings_backing_provider_name=None, provider_settings_provider_name=None, provider_settings_region_name=None, state_name=None, tags=None, termination_protection_enabled=None):
        if auto_indexing and not isinstance(auto_indexing, bool):
            raise TypeError("Expected argument 'auto_indexing' to be a bool")
        pulumi.set(__self__, "auto_indexing", auto_indexing)
        if connection_strings_private_endpoint_srvs and not isinstance(connection_strings_private_endpoint_srvs, list):
            raise TypeError("Expected argument 'connection_strings_private_endpoint_srvs' to be a list")
        pulumi.set(__self__, "connection_strings_private_endpoint_srvs", connection_strings_private_endpoint_srvs)
        if connection_strings_standard_srv and not isinstance(connection_strings_standard_srv, str):
            raise TypeError("Expected argument 'connection_strings_standard_srv' to be a str")
        pulumi.set(__self__, "connection_strings_standard_srv", connection_strings_standard_srv)
        if continuous_backup_enabled and not isinstance(continuous_backup_enabled, bool):
            raise TypeError("Expected argument 'continuous_backup_enabled' to be a bool")
        pulumi.set(__self__, "continuous_backup_enabled", continuous_backup_enabled)
        if create_date and not isinstance(create_date, str):
            raise TypeError("Expected argument 'create_date' to be a str")
        pulumi.set(__self__, "create_date", create_date)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if links and not isinstance(links, list):
            raise TypeError("Expected argument 'links' to be a list")
        pulumi.set(__self__, "links", links)
        if mongo_db_version and not isinstance(mongo_db_version, str):
            raise TypeError("Expected argument 'mongo_db_version' to be a str")
        pulumi.set(__self__, "mongo_db_version", mongo_db_version)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if project_id and not isinstance(project_id, str):
            raise TypeError("Expected argument 'project_id' to be a str")
        pulumi.set(__self__, "project_id", project_id)
        if provider_settings_backing_provider_name and not isinstance(provider_settings_backing_provider_name, str):
            raise TypeError("Expected argument 'provider_settings_backing_provider_name' to be a str")
        pulumi.set(__self__, "provider_settings_backing_provider_name", provider_settings_backing_provider_name)
        if provider_settings_provider_name and not isinstance(provider_settings_provider_name, str):
            raise TypeError("Expected argument 'provider_settings_provider_name' to be a str")
        pulumi.set(__self__, "provider_settings_provider_name", provider_settings_provider_name)
        if provider_settings_region_name and not isinstance(provider_settings_region_name, str):
            raise TypeError("Expected argument 'provider_settings_region_name' to be a str")
        pulumi.set(__self__, "provider_settings_region_name", provider_settings_region_name)
        if state_name and not isinstance(state_name, str):
            raise TypeError("Expected argument 'state_name' to be a str")
        pulumi.set(__self__, "state_name", state_name)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if termination_protection_enabled and not isinstance(termination_protection_enabled, bool):
            raise TypeError("Expected argument 'termination_protection_enabled' to be a bool")
        pulumi.set(__self__, "termination_protection_enabled", termination_protection_enabled)

    @property
    @pulumi.getter(name="autoIndexing")
    def auto_indexing(self) -> bool:
        """
        Flag that indicates whether the serverless instance uses [Serverless Auto Indexing](https://www.mongodb.com/docs/atlas/performance-advisor/auto-index-serverless/).
        """
        return pulumi.get(self, "auto_indexing")

    @property
    @pulumi.getter(name="connectionStringsPrivateEndpointSrvs")
    def connection_strings_private_endpoint_srvs(self) -> Sequence[str]:
        """
        List of Serverless Private Endpoint Connections
        """
        return pulumi.get(self, "connection_strings_private_endpoint_srvs")

    @property
    @pulumi.getter(name="connectionStringsStandardSrv")
    def connection_strings_standard_srv(self) -> str:
        """
        Public `mongodb+srv://` connection string that you can use to connect to this serverless instance.
        """
        return pulumi.get(self, "connection_strings_standard_srv")

    @property
    @pulumi.getter(name="continuousBackupEnabled")
    def continuous_backup_enabled(self) -> bool:
        """
        Flag that indicates whether the serverless instance uses Serverless Continuous Backup.
        """
        return pulumi.get(self, "continuous_backup_enabled")

    @property
    @pulumi.getter(name="createDate")
    def create_date(self) -> str:
        return pulumi.get(self, "create_date")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Unique 24-hexadecimal digit string that identifies the serverless instance.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def links(self) -> Sequence['outputs.GetServerlessInstanceLinkResult']:
        return pulumi.get(self, "links")

    @property
    @pulumi.getter(name="mongoDbVersion")
    def mongo_db_version(self) -> str:
        """
        Version of MongoDB that the serverless instance runs, in `<major version>`.`<minor version>` format.
        """
        return pulumi.get(self, "mongo_db_version")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> str:
        return pulumi.get(self, "project_id")

    @property
    @pulumi.getter(name="providerSettingsBackingProviderName")
    def provider_settings_backing_provider_name(self) -> str:
        """
        Cloud service provider on which MongoDB Cloud provisioned the serverless instance.
        """
        return pulumi.get(self, "provider_settings_backing_provider_name")

    @property
    @pulumi.getter(name="providerSettingsProviderName")
    def provider_settings_provider_name(self) -> str:
        """
        Cloud service provider that applies to the provisioned the serverless instance.
        """
        return pulumi.get(self, "provider_settings_provider_name")

    @property
    @pulumi.getter(name="providerSettingsRegionName")
    def provider_settings_region_name(self) -> str:
        """
        Human-readable label that identifies the physical location of your MongoDB serverless instance. The region you choose can affect network latency for clients accessing your databases.
        """
        return pulumi.get(self, "provider_settings_region_name")

    @property
    @pulumi.getter(name="stateName")
    def state_name(self) -> str:
        """
        Stage of deployment of this serverless instance when the resource made its request.
        """
        return pulumi.get(self, "state_name")

    @property
    @pulumi.getter
    def tags(self) -> Sequence['outputs.GetServerlessInstanceTagResult']:
        """
        Set that contains key-value pairs between 1 to 255 characters in length for tagging and categorizing the cluster. See below.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="terminationProtectionEnabled")
    def termination_protection_enabled(self) -> bool:
        """
        Flag that indicates whether termination protection is enabled on the cluster. If set to true, MongoDB Cloud won't delete the cluster. If set to false, MongoDB Cloud will delete the cluster.
        """
        return pulumi.get(self, "termination_protection_enabled")


class AwaitableGetServerlessInstanceResult(GetServerlessInstanceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetServerlessInstanceResult(
            auto_indexing=self.auto_indexing,
            connection_strings_private_endpoint_srvs=self.connection_strings_private_endpoint_srvs,
            connection_strings_standard_srv=self.connection_strings_standard_srv,
            continuous_backup_enabled=self.continuous_backup_enabled,
            create_date=self.create_date,
            id=self.id,
            links=self.links,
            mongo_db_version=self.mongo_db_version,
            name=self.name,
            project_id=self.project_id,
            provider_settings_backing_provider_name=self.provider_settings_backing_provider_name,
            provider_settings_provider_name=self.provider_settings_provider_name,
            provider_settings_region_name=self.provider_settings_region_name,
            state_name=self.state_name,
            tags=self.tags,
            termination_protection_enabled=self.termination_protection_enabled)


def get_serverless_instance(auto_indexing: Optional[bool] = None,
                            continuous_backup_enabled: Optional[bool] = None,
                            links: Optional[Sequence[Union['GetServerlessInstanceLinkArgs', 'GetServerlessInstanceLinkArgsDict']]] = None,
                            name: Optional[str] = None,
                            project_id: Optional[str] = None,
                            state_name: Optional[str] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetServerlessInstanceResult:
    """
    ## # Data Source: ServerlessInstance

    `ServerlessInstance` describes a single serverless instance. This represents a single serverless instance that have been created.
    > **NOTE:**  Serverless instances do not support some Atlas features at this time.
    For a full list of unsupported features, see [Serverless Instance Limitations](https://docs.atlas.mongodb.com/reference/serverless-instance-limitations/).

    > **NOTE:** Groups and projects are synonymous terms. You may find `groupId` in the official documentation.

    ## Example Usage

    ### Basic
    ```python
    import pulumi
    import pulumi_mongodbatlas as mongodbatlas

    test_two = mongodbatlas.get_serverless_instance(name="<SERVERLESS_INSTANCE_NAME>",
        project_id="<PROJECT_ID >")
    ```

    **NOTE:**  `ServerlessInstance` and `PrivatelinkEndpointServiceServerless` resources have a circular dependency in some respects.\\
    That is, the `serverless_instance` must exist before the `privatelink_endpoint_service` can be created,\\
    and the `privatelink_endpoint_service` must exist before the `serverless_instance` gets its respective `connection_strings_private_endpoint_srv` values.

    Because of this, the `serverless_instance` data source has particular value as a source of the `connection_strings_private_endpoint_srv`.\\
    When using the data_source in-tandem with the afforementioned resources, we can create and retrieve the `connection_strings_private_endpoint_srv` in a single `pulumi up`.

    Follow this example to setup private connection to a serverless instance using aws vpc and get the connection strings in a single `pulumi up`


    :param bool auto_indexing: Flag that indicates whether the serverless instance uses [Serverless Auto Indexing](https://www.mongodb.com/docs/atlas/performance-advisor/auto-index-serverless/).
    :param bool continuous_backup_enabled: Flag that indicates whether the serverless instance uses Serverless Continuous Backup.
    :param str name: Human-readable label that identifies your serverless instance.
    :param str project_id: Unique 24-hexadecimal digit string that identifies the project that contains your serverless instance.
    :param str state_name: Stage of deployment of this serverless instance when the resource made its request.
    """
    __args__ = dict()
    __args__['autoIndexing'] = auto_indexing
    __args__['continuousBackupEnabled'] = continuous_backup_enabled
    __args__['links'] = links
    __args__['name'] = name
    __args__['projectId'] = project_id
    __args__['stateName'] = state_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('mongodbatlas:index/getServerlessInstance:getServerlessInstance', __args__, opts=opts, typ=GetServerlessInstanceResult).value

    return AwaitableGetServerlessInstanceResult(
        auto_indexing=pulumi.get(__ret__, 'auto_indexing'),
        connection_strings_private_endpoint_srvs=pulumi.get(__ret__, 'connection_strings_private_endpoint_srvs'),
        connection_strings_standard_srv=pulumi.get(__ret__, 'connection_strings_standard_srv'),
        continuous_backup_enabled=pulumi.get(__ret__, 'continuous_backup_enabled'),
        create_date=pulumi.get(__ret__, 'create_date'),
        id=pulumi.get(__ret__, 'id'),
        links=pulumi.get(__ret__, 'links'),
        mongo_db_version=pulumi.get(__ret__, 'mongo_db_version'),
        name=pulumi.get(__ret__, 'name'),
        project_id=pulumi.get(__ret__, 'project_id'),
        provider_settings_backing_provider_name=pulumi.get(__ret__, 'provider_settings_backing_provider_name'),
        provider_settings_provider_name=pulumi.get(__ret__, 'provider_settings_provider_name'),
        provider_settings_region_name=pulumi.get(__ret__, 'provider_settings_region_name'),
        state_name=pulumi.get(__ret__, 'state_name'),
        tags=pulumi.get(__ret__, 'tags'),
        termination_protection_enabled=pulumi.get(__ret__, 'termination_protection_enabled'))


@_utilities.lift_output_func(get_serverless_instance)
def get_serverless_instance_output(auto_indexing: Optional[pulumi.Input[Optional[bool]]] = None,
                                   continuous_backup_enabled: Optional[pulumi.Input[Optional[bool]]] = None,
                                   links: Optional[pulumi.Input[Optional[Sequence[Union['GetServerlessInstanceLinkArgs', 'GetServerlessInstanceLinkArgsDict']]]]] = None,
                                   name: Optional[pulumi.Input[str]] = None,
                                   project_id: Optional[pulumi.Input[str]] = None,
                                   state_name: Optional[pulumi.Input[Optional[str]]] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetServerlessInstanceResult]:
    """
    ## # Data Source: ServerlessInstance

    `ServerlessInstance` describes a single serverless instance. This represents a single serverless instance that have been created.
    > **NOTE:**  Serverless instances do not support some Atlas features at this time.
    For a full list of unsupported features, see [Serverless Instance Limitations](https://docs.atlas.mongodb.com/reference/serverless-instance-limitations/).

    > **NOTE:** Groups and projects are synonymous terms. You may find `groupId` in the official documentation.

    ## Example Usage

    ### Basic
    ```python
    import pulumi
    import pulumi_mongodbatlas as mongodbatlas

    test_two = mongodbatlas.get_serverless_instance(name="<SERVERLESS_INSTANCE_NAME>",
        project_id="<PROJECT_ID >")
    ```

    **NOTE:**  `ServerlessInstance` and `PrivatelinkEndpointServiceServerless` resources have a circular dependency in some respects.\\
    That is, the `serverless_instance` must exist before the `privatelink_endpoint_service` can be created,\\
    and the `privatelink_endpoint_service` must exist before the `serverless_instance` gets its respective `connection_strings_private_endpoint_srv` values.

    Because of this, the `serverless_instance` data source has particular value as a source of the `connection_strings_private_endpoint_srv`.\\
    When using the data_source in-tandem with the afforementioned resources, we can create and retrieve the `connection_strings_private_endpoint_srv` in a single `pulumi up`.

    Follow this example to setup private connection to a serverless instance using aws vpc and get the connection strings in a single `pulumi up`


    :param bool auto_indexing: Flag that indicates whether the serverless instance uses [Serverless Auto Indexing](https://www.mongodb.com/docs/atlas/performance-advisor/auto-index-serverless/).
    :param bool continuous_backup_enabled: Flag that indicates whether the serverless instance uses Serverless Continuous Backup.
    :param str name: Human-readable label that identifies your serverless instance.
    :param str project_id: Unique 24-hexadecimal digit string that identifies the project that contains your serverless instance.
    :param str state_name: Stage of deployment of this serverless instance when the resource made its request.
    """
    ...

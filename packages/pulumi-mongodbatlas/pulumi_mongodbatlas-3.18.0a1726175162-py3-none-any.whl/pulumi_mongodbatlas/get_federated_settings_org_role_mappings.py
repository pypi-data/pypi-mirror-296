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
    'GetFederatedSettingsOrgRoleMappingsResult',
    'AwaitableGetFederatedSettingsOrgRoleMappingsResult',
    'get_federated_settings_org_role_mappings',
    'get_federated_settings_org_role_mappings_output',
]

@pulumi.output_type
class GetFederatedSettingsOrgRoleMappingsResult:
    """
    A collection of values returned by getFederatedSettingsOrgRoleMappings.
    """
    def __init__(__self__, federation_settings_id=None, id=None, items_per_page=None, org_id=None, page_num=None, results=None):
        if federation_settings_id and not isinstance(federation_settings_id, str):
            raise TypeError("Expected argument 'federation_settings_id' to be a str")
        pulumi.set(__self__, "federation_settings_id", federation_settings_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if items_per_page and not isinstance(items_per_page, int):
            raise TypeError("Expected argument 'items_per_page' to be a int")
        pulumi.set(__self__, "items_per_page", items_per_page)
        if org_id and not isinstance(org_id, str):
            raise TypeError("Expected argument 'org_id' to be a str")
        pulumi.set(__self__, "org_id", org_id)
        if page_num and not isinstance(page_num, int):
            raise TypeError("Expected argument 'page_num' to be a int")
        pulumi.set(__self__, "page_num", page_num)
        if results and not isinstance(results, list):
            raise TypeError("Expected argument 'results' to be a list")
        pulumi.set(__self__, "results", results)

    @property
    @pulumi.getter(name="federationSettingsId")
    def federation_settings_id(self) -> str:
        return pulumi.get(self, "federation_settings_id")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="itemsPerPage")
    def items_per_page(self) -> Optional[int]:
        return pulumi.get(self, "items_per_page")

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> str:
        return pulumi.get(self, "org_id")

    @property
    @pulumi.getter(name="pageNum")
    def page_num(self) -> Optional[int]:
        return pulumi.get(self, "page_num")

    @property
    @pulumi.getter
    def results(self) -> Sequence['outputs.GetFederatedSettingsOrgRoleMappingsResultResult']:
        """
        Includes cloudProviderSnapshot object for each item detailed in the results array section.
        * `totalCount` - Count of the total number of items in the result set. It may be greater than the number of objects in the results array if the entire result set is paginated.
        """
        return pulumi.get(self, "results")


class AwaitableGetFederatedSettingsOrgRoleMappingsResult(GetFederatedSettingsOrgRoleMappingsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetFederatedSettingsOrgRoleMappingsResult(
            federation_settings_id=self.federation_settings_id,
            id=self.id,
            items_per_page=self.items_per_page,
            org_id=self.org_id,
            page_num=self.page_num,
            results=self.results)


def get_federated_settings_org_role_mappings(federation_settings_id: Optional[str] = None,
                                             items_per_page: Optional[int] = None,
                                             org_id: Optional[str] = None,
                                             page_num: Optional[int] = None,
                                             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetFederatedSettingsOrgRoleMappingsResult:
    """
    ## # Data Source: get_federated_settings_org_role_mappings

    `get_federated_settings_org_role_mappings` provides an Federated Settings Org Role Mapping datasource. Atlas Cloud Federated Settings Org Role Mapping provides federated settings outputs for the configured Org Role Mapping.


    :param str federation_settings_id: Unique 24-hexadecimal digit string that identifies the federated authentication configuration.
    :param int items_per_page: Number of items to return per page, up to a maximum of 500. Defaults to `100`.
    :param str org_id: Unique 24-hexadecimal digit string that identifies the organization that contains your projects.
    :param int page_num: The page to return. Defaults to `1`.
    """
    __args__ = dict()
    __args__['federationSettingsId'] = federation_settings_id
    __args__['itemsPerPage'] = items_per_page
    __args__['orgId'] = org_id
    __args__['pageNum'] = page_num
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('mongodbatlas:index/getFederatedSettingsOrgRoleMappings:getFederatedSettingsOrgRoleMappings', __args__, opts=opts, typ=GetFederatedSettingsOrgRoleMappingsResult).value

    return AwaitableGetFederatedSettingsOrgRoleMappingsResult(
        federation_settings_id=pulumi.get(__ret__, 'federation_settings_id'),
        id=pulumi.get(__ret__, 'id'),
        items_per_page=pulumi.get(__ret__, 'items_per_page'),
        org_id=pulumi.get(__ret__, 'org_id'),
        page_num=pulumi.get(__ret__, 'page_num'),
        results=pulumi.get(__ret__, 'results'))


@_utilities.lift_output_func(get_federated_settings_org_role_mappings)
def get_federated_settings_org_role_mappings_output(federation_settings_id: Optional[pulumi.Input[str]] = None,
                                                    items_per_page: Optional[pulumi.Input[Optional[int]]] = None,
                                                    org_id: Optional[pulumi.Input[str]] = None,
                                                    page_num: Optional[pulumi.Input[Optional[int]]] = None,
                                                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetFederatedSettingsOrgRoleMappingsResult]:
    """
    ## # Data Source: get_federated_settings_org_role_mappings

    `get_federated_settings_org_role_mappings` provides an Federated Settings Org Role Mapping datasource. Atlas Cloud Federated Settings Org Role Mapping provides federated settings outputs for the configured Org Role Mapping.


    :param str federation_settings_id: Unique 24-hexadecimal digit string that identifies the federated authentication configuration.
    :param int items_per_page: Number of items to return per page, up to a maximum of 500. Defaults to `100`.
    :param str org_id: Unique 24-hexadecimal digit string that identifies the organization that contains your projects.
    :param int page_num: The page to return. Defaults to `1`.
    """
    ...

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
    'GetAtlasUsersResult',
    'AwaitableGetAtlasUsersResult',
    'get_atlas_users',
    'get_atlas_users_output',
]

@pulumi.output_type
class GetAtlasUsersResult:
    """
    A collection of values returned by getAtlasUsers.
    """
    def __init__(__self__, id=None, items_per_page=None, org_id=None, page_num=None, project_id=None, results=None, team_id=None, total_count=None):
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
        if project_id and not isinstance(project_id, str):
            raise TypeError("Expected argument 'project_id' to be a str")
        pulumi.set(__self__, "project_id", project_id)
        if results and not isinstance(results, list):
            raise TypeError("Expected argument 'results' to be a list")
        pulumi.set(__self__, "results", results)
        if team_id and not isinstance(team_id, str):
            raise TypeError("Expected argument 'team_id' to be a str")
        pulumi.set(__self__, "team_id", team_id)
        if total_count and not isinstance(total_count, int):
            raise TypeError("Expected argument 'total_count' to be a int")
        pulumi.set(__self__, "total_count", total_count)

    @property
    @pulumi.getter
    @_utilities.deprecated("""Please use each user's id attribute instead""")
    def id(self) -> str:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="itemsPerPage")
    def items_per_page(self) -> Optional[int]:
        return pulumi.get(self, "items_per_page")

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> Optional[str]:
        return pulumi.get(self, "org_id")

    @property
    @pulumi.getter(name="pageNum")
    def page_num(self) -> Optional[int]:
        return pulumi.get(self, "page_num")

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> Optional[str]:
        return pulumi.get(self, "project_id")

    @property
    @pulumi.getter
    def results(self) -> Sequence['outputs.GetAtlasUsersResultResult']:
        """
        A list where each element contains a Atlas User.
        """
        return pulumi.get(self, "results")

    @property
    @pulumi.getter(name="teamId")
    def team_id(self) -> Optional[str]:
        return pulumi.get(self, "team_id")

    @property
    @pulumi.getter(name="totalCount")
    def total_count(self) -> int:
        """
        Count of the total number of items in the result set. It may be greater than the number of objects in the results array if the entire result set is paginated.
        """
        return pulumi.get(self, "total_count")


class AwaitableGetAtlasUsersResult(GetAtlasUsersResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAtlasUsersResult(
            id=self.id,
            items_per_page=self.items_per_page,
            org_id=self.org_id,
            page_num=self.page_num,
            project_id=self.project_id,
            results=self.results,
            team_id=self.team_id,
            total_count=self.total_count)


def get_atlas_users(items_per_page: Optional[int] = None,
                    org_id: Optional[str] = None,
                    page_num: Optional[int] = None,
                    project_id: Optional[str] = None,
                    team_id: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAtlasUsersResult:
    """
    ## # Data Source: atlas_users

    `atlas_users` provides Atlas Users associated with a specified Organization, Project, or Team.

    > **NOTE:** Groups and projects are synonymous terms. You may find `groupId` in the official documentation.

    ## Example Usage

    ### Using org_id attribute to query Organization Atlas Users

    ```python
    import pulumi
    import pulumi_mongodbatlas as mongodbatlas

    test = mongodbatlas.get_atlas_users(org_id="<ORG_ID>")
    ```

    ### Using project_id attribute to query Project Atlas Users

    ```python
    import pulumi
    import pulumi_mongodbatlas as mongodbatlas

    test = mongodbatlas.get_atlas_users(project_id="<PROJECT_ID>")
    ```

    ### Using team_id and org_id attribute to query Team Atlas Users

    ```python
    import pulumi
    import pulumi_mongodbatlas as mongodbatlas

    test = mongodbatlas.get_atlas_users(team_id="<TEAM_ID>",
        org_id="<ORG_ID>")
    ```


    :param int items_per_page: Number of items that the response returns per page, up to a maximum of `500`. Defaults to `100`.
           
           > **IMPORTANT:** Either `org_id`, `project_id`, or `team_id` with `org_id` must be configurated.
    :param str org_id: Unique 24-hexadecimal digit string that identifies the organization whose users you want to return. Also needed when `team_id` attributes is defined.
    :param int page_num: Number of the page that displays the current set of the total objects that the response returns. Defaults to `1`.
    :param str project_id: Unique 24-hexadecimal digit string that identifies the project whose users you want to return.
    :param str team_id: Unique 24-hexadecimal digit string that identifies the team whose users you want to return.
    """
    __args__ = dict()
    __args__['itemsPerPage'] = items_per_page
    __args__['orgId'] = org_id
    __args__['pageNum'] = page_num
    __args__['projectId'] = project_id
    __args__['teamId'] = team_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('mongodbatlas:index/getAtlasUsers:getAtlasUsers', __args__, opts=opts, typ=GetAtlasUsersResult).value

    return AwaitableGetAtlasUsersResult(
        id=pulumi.get(__ret__, 'id'),
        items_per_page=pulumi.get(__ret__, 'items_per_page'),
        org_id=pulumi.get(__ret__, 'org_id'),
        page_num=pulumi.get(__ret__, 'page_num'),
        project_id=pulumi.get(__ret__, 'project_id'),
        results=pulumi.get(__ret__, 'results'),
        team_id=pulumi.get(__ret__, 'team_id'),
        total_count=pulumi.get(__ret__, 'total_count'))


@_utilities.lift_output_func(get_atlas_users)
def get_atlas_users_output(items_per_page: Optional[pulumi.Input[Optional[int]]] = None,
                           org_id: Optional[pulumi.Input[Optional[str]]] = None,
                           page_num: Optional[pulumi.Input[Optional[int]]] = None,
                           project_id: Optional[pulumi.Input[Optional[str]]] = None,
                           team_id: Optional[pulumi.Input[Optional[str]]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAtlasUsersResult]:
    """
    ## # Data Source: atlas_users

    `atlas_users` provides Atlas Users associated with a specified Organization, Project, or Team.

    > **NOTE:** Groups and projects are synonymous terms. You may find `groupId` in the official documentation.

    ## Example Usage

    ### Using org_id attribute to query Organization Atlas Users

    ```python
    import pulumi
    import pulumi_mongodbatlas as mongodbatlas

    test = mongodbatlas.get_atlas_users(org_id="<ORG_ID>")
    ```

    ### Using project_id attribute to query Project Atlas Users

    ```python
    import pulumi
    import pulumi_mongodbatlas as mongodbatlas

    test = mongodbatlas.get_atlas_users(project_id="<PROJECT_ID>")
    ```

    ### Using team_id and org_id attribute to query Team Atlas Users

    ```python
    import pulumi
    import pulumi_mongodbatlas as mongodbatlas

    test = mongodbatlas.get_atlas_users(team_id="<TEAM_ID>",
        org_id="<ORG_ID>")
    ```


    :param int items_per_page: Number of items that the response returns per page, up to a maximum of `500`. Defaults to `100`.
           
           > **IMPORTANT:** Either `org_id`, `project_id`, or `team_id` with `org_id` must be configurated.
    :param str org_id: Unique 24-hexadecimal digit string that identifies the organization whose users you want to return. Also needed when `team_id` attributes is defined.
    :param int page_num: Number of the page that displays the current set of the total objects that the response returns. Defaults to `1`.
    :param str project_id: Unique 24-hexadecimal digit string that identifies the project whose users you want to return.
    :param str team_id: Unique 24-hexadecimal digit string that identifies the team whose users you want to return.
    """
    ...

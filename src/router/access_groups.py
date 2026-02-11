"""Endpoints for the access groups."""

from fastapi import APIRouter, status

from src.schema.access_groups import AccessGroupRequest, AccessGroupResponse
from src.service.access_groups import AccessGroupsService

access_groups_router = APIRouter(prefix="/access-groups")


@access_groups_router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=AccessGroupResponse
)
async def create_group_access(request: AccessGroupRequest) -> AccessGroupResponse:
    """Create a new group access.

    Args:
        request (AccessGroupRequest): The group access data.

    Returns:
        AccessGroupResponse: The created access groups.
    """
    return await AccessGroupsService.create_access_group(request)


@access_groups_router.get(
    "/", status_code=status.HTTP_200_OK, response_model=list[AccessGroupResponse]
)
async def get_all() -> list[AccessGroupResponse]:
    """Get all access groups.

    Returns:
        list[AccessGroupResponse]: The access groups retrieved.
    """
    return await AccessGroupsService.get_all()


@access_groups_router.get(
    "/by-id", status_code=status.HTTP_200_OK, response_model=AccessGroupResponse
)
async def get_by_id(id: str) -> AccessGroupResponse:
    """Get an access group data by id.

    Args:
        id (str): The access group id.

    Returns:
        AccessGroupResponse: The access group data.
    """
    return await AccessGroupsService.get_by_id(id)

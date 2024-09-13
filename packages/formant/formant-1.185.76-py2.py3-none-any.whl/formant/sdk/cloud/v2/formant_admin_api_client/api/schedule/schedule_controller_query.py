from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ...client import AuthenticatedClient
from ...models.schedule_list_response import ScheduleListResponse
from ...models.schedules_query import SchedulesQuery
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: SchedulesQuery,
) -> Dict[str, Any]:
    url = "{}/schedules/query".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[ScheduleListResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ScheduleListResponse.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[ScheduleListResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: SchedulesQuery,
) -> Response[ScheduleListResponse]:
    """Query

     Query schedules
    Resource: schedules
    Authorized roles: viewer

    Args:
        json_body (SchedulesQuery):

    Returns:
        Response[ScheduleListResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: SchedulesQuery,
) -> Optional[ScheduleListResponse]:
    """Query

     Query schedules
    Resource: schedules
    Authorized roles: viewer

    Args:
        json_body (SchedulesQuery):

    Returns:
        Response[ScheduleListResponse]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: SchedulesQuery,
) -> Response[ScheduleListResponse]:
    """Query

     Query schedules
    Resource: schedules
    Authorized roles: viewer

    Args:
        json_body (SchedulesQuery):

    Returns:
        Response[ScheduleListResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: SchedulesQuery,
) -> Optional[ScheduleListResponse]:
    """Query

     Query schedules
    Resource: schedules
    Authorized roles: viewer

    Args:
        json_body (SchedulesQuery):

    Returns:
        Response[ScheduleListResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed

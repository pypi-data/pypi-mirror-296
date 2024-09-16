from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    dataset_path: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/api/v1/dataset/down/{dataset_path}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = response.json()
        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    dataset_path: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, HTTPValidationError]]:
    """Dataset Download

     数据集文件下载,(内部从 github 仓库获取数据集文件)

    Args:
        dataset_path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        dataset_path=dataset_path,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    dataset_path: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, HTTPValidationError]]:
    """Dataset Download

     数据集文件下载,(内部从 github 仓库获取数据集文件)

    Args:
        dataset_path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return sync_detailed(
        dataset_path=dataset_path,
        client=client,
    ).parsed


async def asyncio_detailed(
    dataset_path: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, HTTPValidationError]]:
    """Dataset Download

     数据集文件下载,(内部从 github 仓库获取数据集文件)

    Args:
        dataset_path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        dataset_path=dataset_path,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    dataset_path: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, HTTPValidationError]]:
    """Dataset Download

     数据集文件下载,(内部从 github 仓库获取数据集文件)

    Args:
        dataset_path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            dataset_path=dataset_path,
            client=client,
        )
    ).parsed

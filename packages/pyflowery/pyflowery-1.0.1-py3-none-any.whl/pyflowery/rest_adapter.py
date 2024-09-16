"""This module contains the RestAdapter class, which is used to make requests to the Flowery API."""""
from json import JSONDecodeError

import aiohttp

from pyflowery.models import FloweryAPIConfig, Result


class RestAdapter:
    """Constructor for RestAdapter

    Args:
        config (FloweryAPIConfig): Configuration object for the FloweryAPI class

    Raises:
        ValueError: Raised when the keyword arguments passed to the class constructor conflict.
    """
    def __init__(self, config = FloweryAPIConfig):
        self._url = "https://api.flowery.pw/v1"
        self._user_agent = config.user_agent
        self._logger = config.logger

    async def _do(self, http_method: str, endpoint: str, params: dict = None, timeout: float = 60):
        """Internal method to make a request to the Flowery API. You shouldn't use this directly.

        Args:
            http_method (str): The [HTTP method](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods) to use
            endpoint (str): The endpoint to make the request to.
            params (dict): Python dictionary of query parameters to send with the request.
            timeout (float): Number of seconds to wait for the request to complete.

        Returns:
            Result: A Result object containing the status code, message, and data from the request.
        """
        full_url = self._url + endpoint
        headers = {
            'User-Agent': self._user_agent,
        }
        sanitized_params = {k: str(v) if isinstance(v, bool) else v for k, v in params.items()} if params else None
        self._logger.debug("Making %s request to %s with params %s", http_method, full_url, sanitized_params)

        async with aiohttp.ClientSession() as session:
            async with session.request(method=http_method, url=full_url, params=sanitized_params, headers=headers, timeout=timeout) as response:
                try:
                    data = await response.json()
                except (JSONDecodeError, aiohttp.ContentTypeError):
                    data = await response.read()

                result = Result(
                    success=response.status in range(200, 299),
                    status_code=response.status,
                    message=response.reason,
                    data=data,
                )
                self._logger.debug("Received response: %s %s", response.status, response.reason)
                return result

    async def get(self, endpoint: str, params: dict = None, timeout: float = 60) -> Result:
        """Make a GET request to the Flowery API. You should almost never have to use this directly.

        Args:
            endpoint (str): The endpoint to make the request to.
            params (dict): Python dictionary of query parameters to send with the request.
            timeout (float): Number of seconds to wait for the request to complete.

        Returns:
            Result: A Result object containing the status code, message, and data from the request.
        """
        return await self._do(http_method='GET', endpoint=endpoint, params=params, timeout=timeout)

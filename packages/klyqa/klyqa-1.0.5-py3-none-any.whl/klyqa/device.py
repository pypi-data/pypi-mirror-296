import asyncio
import logging
import socket
from typing import Any, TypedDict

from aiohttp.client import ClientError, ClientSession
from aiohttp.hdrs import METH_GET, METH_PUT
from yarl import URL
import json

from .exceptions import KlyqaConnectionError, KlyqaAuthenticationError, KlyqaError
from .models import Info, RGBColor, State  # , PowerOnBehavior, Settings

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.DEBUG)

# formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# console_handler.setFormatter(formatter)

# if not _LOGGER.handlers:
#     _LOGGER.addHandler(console_handler)


class KlyqaDevice:
    BASE_URL_TEMPLATE = "http://{ip}:{port}/api/v1/"

    host: str
    port: int = 3333
    request_timeout: int = 8
    access_token: str
    session: ClientSession | None = None

    _close_session: bool = False

    def __init__(self, host, port, access_token, session) -> None:
        """Init for Klyqa devices"""
        self.host = host
        self.port = port
        self.access_token = access_token

        self.session = session
        self.base_url = self.BASE_URL_TEMPLATE.format(ip=self.host, port=self.port)
        self.headers = {"Authorization": f"{self.access_token}"}
        self._state = {}  # Shadow state to store the device state

        _LOGGER.info(f"Device access token {self.access_token}")

        # Update the shadow state on initialization
        asyncio.create_task(self._update_state())

    async def _send_request(self, method, endpoint, json_payload=None) -> str:
        """Helper function to send HTTP requests."""
        url = self.base_url + endpoint
        async with self.session.request(
            method, url, json=json_payload, headers=self.headers
        ) as resp:
            if resp.status == 200:
                return await resp.json()
            if resp.status == 401:
                raise KlyqaAuthenticationError(
                    f"Request failed with status code {resp.status} for endpoint {endpoint}"
                )
            raise KlyqaError("Error in sending request to device")

    async def _request(
        self,
        uri: str,
        *,
        method: str = METH_GET,
        data: dict[str, Any] | None = None,
    ) -> str:
        """Handle a request to a Klyqa Light device.

        A generic method for sending/handling HTTP requests done against
        the Klyqa Light API.

        Args:
        ----
            uri: Request URI, without '/api/v1/', for example, 'info'
            method: HTTP Method to use.
            data: Dictionary of data to send to the Klyqa Light.

        Returns:
        -------
            A Python string (JSON) with the response from the Klyqa Light API.

        Raises:
        ------
            KlyqaConnectionError: An error occurred while communicating with
                the Klyqa Light.
            KlyqaError: Received an unexpected response from the Klyqa Light
                API.

        """
        url = URL.build(
            scheme="http",
            host=self.host,
            port=self.port,
            path="/api/v1/",
        ).join(URL(uri))

        headers = {
            "Authorization": self.access_token,
            "User-Agent": "PythonKlyqa",
            "Accept": "application/json, text/plain, */*",
        }

        if self.session is None:
            self.session = ClientSession()
            self._close_session = True

        try:
            async with asyncio.timeout(self.request_timeout):
                response = await self.session.request(
                    method,
                    url,
                    json=data,
                    headers=headers,
                )
                response.raise_for_status()
        except TimeoutError as exception:
            msg = "Timeout occurred while connecting to Klyqa Light device"
            raise KlyqaConnectionError(msg) from exception
        except (
            ClientError,
            socket.gaierror,
        ) as exception:
            msg = "Error occurred while communicating with Klyqa Light device"
            raise KlyqaConnectionError(msg) from exception

        return await response.text()

    async def _request_command(
        self,
        uri: str,
        *,
        method: str = METH_GET,
        data: dict[str, Any] | None = None,
    ) -> str:
        """Handle a command request to a Klyqa Light device.

        A generic method for sending/handling HTTP command requests done against
        the Klyqa Light API.

        Args:
        ----
            uri: Request URI, without '/api/v1/', for example, 'info'
            method: HTTP Method to use.
            data: Dictionary of data to send to the Klyqa Light.

        Returns:
        -------
            A Python string (JSON) with the response from the Klyqa Light API.

        Raises:
        ------
            KlyqaConnectionError: An error occurred while communicating with
                the Klyqa Light.
            KlyqaError: Received an unexpected response from the Klyqa Light
                API.

        """
        url = URL.build(
            scheme="http",
            host=self.host,
            port=self.port,
            path="/api/v1/",
        ).join(URL(uri))

        headers = {
            "Authorization": self.access_token,
            "User-Agent": "PythonKlyqa",
            "Accept": "application/json, text/plain, */*",
        }

        send_data = {"command": data}

        if self.session is None:
            self.session = ClientSession()
            self._close_session = True

        try:
            async with asyncio.timeout(self.request_timeout):
                response = await self.session.request(
                    method,
                    url,
                    json=send_data,
                    headers=headers,
                )
                response.raise_for_status()
        except TimeoutError as exception:
            msg = "Timeout occurred while connecting to Klyqa Light device"
            raise KlyqaConnectionError(msg) from exception
        except (
            ClientError,
            socket.gaierror,
        ) as exception:
            msg = "Error occurred while communicating with Klyqa Light device"
            raise KlyqaConnectionError(msg) from exception

        return await response.text()

    async def _update_state(self) -> None:
        """Update the shadow state by fetching the current state from the device."""
        self._state = await self._send_request(
            "PUT", "system/command", json_payload={"command": {"type": "request"}}
        )
        _LOGGER.info("Device state updated!")
        _LOGGER.debug("Device state: %s", self._state)

    async def info(self) -> Info:
        """Get devices information from Klyqa Light device.

        Returns
        -------
            A Info object, with information about the Klyqa Light device.

        """
        data = await self._request("system/info")
        return Info.from_json(data)

    async def state(self) -> State:
        """Get the current state of Klyqa Light device.

        Returns
        -------
            A State object, with the current Klyqa Light state.

        """
        data = await self._request_command(
            "system/command", method=METH_PUT, data={"type": "request"}
        )
        # pylint: disable-next=no-member
        return State.from_json(data)

    # pylint: disable-next=too-many-arguments
    async def light(
        self,
        *,
        on: bool | None = None,
        brightness: int | None = None,
        color: RGBColor | None = None,
        temperature: int | None = None,
    ) -> None:
        """Change state of an Klyqa Light device.

        Args:
        ----
            on: A boolean, true to turn the light on, false otherwise.
            brightness: The brightness of the light, between 0 and 255.
            color: RGBColor
            temperature: The white temperature of the light, in kelvin.

        Raises:
        ------
            KlyqaError: The provided values are invalid.

        """
        if temperature and (color):
            msg = "Cannot set temperature together with color"
            raise KlyqaError(msg)

        class LightState(TypedDict, total=False):
            """Describe state dictionary that can be set on a light."""

            brightness: int
            color: RGBColor
            status: str
            temperature: int

        state: LightState = {}

        state["type"] = "request"

        if on is not None:
            if on:
                state["status"] = "on"
            else:
                state["status"] = "off"

        if brightness is not None:
            if not 0 <= brightness <= 100:
                msg = "Brightness not between 0 and 100"
                raise KlyqaError(msg)
            state["brightness"] = {"percentage": brightness}

        if color is not None:
            state["color"] = {
                "red": color.red,
                "green": color.green,
                "blue": color.blue,
            }

        if temperature is not None:
            if not 2200 <= temperature <= 7500:
                msg = "White temperature out of range"
                raise KlyqaError(msg)
            state["temperature"] = temperature

        if not state:
            msg = "No parameters to set, light not adjusted"
            raise KlyqaError(msg)

        _LOGGER.info(f"Device state {state}")

        await self._request_command(
            "system/command",
            method=METH_PUT,
            data=state,
        )

    async def close(self) -> None:
        """Close the session."""
        await self.session.close()

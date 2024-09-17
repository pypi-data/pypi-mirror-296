import logging

import aiohttp

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.DEBUG)  # Setze den Level des Handlers auf DEBUG

# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# console_handler.setFormatter(formatter)

# if not _LOGGER.handlers:
#     _LOGGER.addHandler(console_handler)


class KlyqaCloud:
    BASE_URL = "https://app-api.test.qconnex.io"

    def __init__(self, email, password) -> None:
        self.email = email
        self.password = password
        self.api_key = None
        self.session = aiohttp.ClientSession()

    async def login(self) -> str:
        """Login to the cloud and retrieve the API key."""
        login_url = self.BASE_URL + "/auth/login"
        _LOGGER.debug("Trying to login at %s", login_url)
        payload = {"email": self.email, "password": self.password}

        async with self.session.post(login_url, json=payload, timeout=10) as resp:
            if resp.status == 201:
                data = await resp.json()
                self.api_key = data.get("accountToken")
                _LOGGER.debug("Login successful, API Key: %s", self.api_key)
                return self.api_key
            raise Exception(f"Login failed with status code: {resp.status}")

    def get_api_key(self) -> str:
        """Get the API Key."""
        return self.api_key

    async def get_devices(self) -> str:
        """Fetch devices from the cloud."""
        if not self.api_key:
            raise Exception("Not logged in. Call login() first.")

        devices_url = self.BASE_URL + "/settings"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        async with self.session.get(devices_url, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                devices = data.get("devices", [])
                return devices
            raise Exception(f"Failed to fetch devices with status code: {resp.status}")

    async def get_device_access_token(self, local_device_id) -> str:
        """Retrieve access token for a specific local device."""
        devices = await self.get_devices()
        for device in devices:
            if device.get("localDeviceId") == local_device_id:
                return device.get("accessToken")
        raise Exception(f"Device with localDeviceId {local_device_id} not found.")

    async def get_device_name(self, local_device_id) -> str:
        """Retrieve access token for a specific local device."""
        devices = await self.get_devices()
        for device in devices:
            if device.get("localDeviceId") == local_device_id:
                return device.get("name")
        raise Exception(f"Device with localDeviceId {local_device_id} not found.")

    async def close(self) -> None:
        await self.session.close()

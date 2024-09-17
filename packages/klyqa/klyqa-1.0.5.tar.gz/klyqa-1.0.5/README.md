# klyqa

`klyqa` is a Python library for interacting with Klyqa REST-enabled devices. It allows users to manage and control Klyqa smart devices, such as smart bulbs, by interfacing with the Klyqa cloud and directly with devices on the local network.

## Installation

You can install the library directly from the source:

```bash
pip install klyqa
```

## Requirements

- Python 3.12+
- zeroconf
- aiohttp
- orjson
- mashumaro

## Features

- Connect to the Klyqa Cloud to manage devices.
- Fetch device details such as name and access token.
- Control device state (turn on/off, adjust color, brightness, etc.).
- Fetch device information (e.g., firmware version, mode, etc.).

## Usage

### 1. Interacting with the Klyqa Cloud

The library provides functionality to log in to the Klyqa Cloud and retrieve device details:

```python
import asyncio
from klyqa.cloud import KlyqaCloud

async def cloud_interaction():
    # Login to the Klyqa Cloud
    cloud = KlyqaCloud("email@example.com", "your_password")
    await cloud.login()

    # Fetch devices from the cloud
    devices = await cloud.get_devices()
    print("Devices:", devices)

    # Get access token for a device
    local_device_id = "012345678901"
    access_token = await cloud.get_device_access_token(local_device_id)
    print("Access Token:", access_token)

    await cloud.close()

asyncio.run(cloud_interaction())
```

### 2. Controlling a Local Device

Once you have the access token from the cloud, you can control a device on the local network:

```python
import asyncio
from aiohttp.client import ClientSession
from klyqa.device import KlyqaDevice
from klyqa.models import RGBColor

async def control_device():
    # Device connection details
    local_device_id = "012345678901"
    device_ip = "192.168.1.100"
    port = 3333

    # Use the access token fetched from the cloud
    access_token = "your_access_token"

    async with ClientSession() as session:
        # Connect to the local device
        device = KlyqaDevice(device_ip, port, access_token, session)

        # Turn the device on, set to blue color, and full brightness
        await device.light(on=True, color=RGBColor(red=0, green=0, blue=255), brightness=100)

        await device.close()

asyncio.run(control_device())
```

### 3. Fetching Device Info and State

You can also retrieve information about the device, such as its firmware version and current state:

```python
import asyncio
from aiohttp.client import ClientSession
from klyqa.device import KlyqaDevice
from klyqa.models import Info, State

async def fetch_device_info():
    local_device_id = "012345678901"
    device_ip = "192.168.1.100"
    port = 3333
    access_token = "your_access_token"

    async with ClientSession() as session:
        device = KlyqaDevice(device_ip, port, access_token, session)

        # Get device info
        info: Info = await device.info()
        print("Device Info:", info)

        # Get device state
        state: State = await device.state()
        print("Device State:", state)

        await device.close()

asyncio.run(fetch_device_info())
```

## Contributing

Bug reports and pull requests are welcome on GitHub at [python-klyqa GitHub issues](https://github.com/ninharp/python-klyqa/issues).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

- **Michael Sauer** - [zukunpht@gmail.com](mailto:zukunpht@gmail.com)

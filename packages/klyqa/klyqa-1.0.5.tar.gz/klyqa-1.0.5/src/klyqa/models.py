"""Asynchronous Python client for Klyqa Lights."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum
from typing import Optional

from mashumaro import field_options
from mashumaro.config import BaseConfig
from mashumaro.mixins.orjson import DataClassORJSONMixin
from mashumaro.types import SerializationStrategy


class IntegerIsBoolean(SerializationStrategy):
    """Boolean serialization strategy for integers."""

    def serialize(self, value: bool) -> int:  # noqa: FBT001
        """Serialize a boolean to an integer."""
        return int(value)

    def deserialize(self, value: int) -> bool:
        """Deserialize an integer to a boolean."""
        return bool(value)


class BaseModel(DataClassORJSONMixin):
    """Base model for all Klyqa models."""

    # pylint: disable-next=too-few-public-methods
    class Config(BaseConfig):
        """Mashumaro configuration."""

        omit_none = True
        serialization_strategy = {bool: IntegerIsBoolean()}  # noqa: RUF012
        serialize_by_alias = True


@dataclass
class Wifi(BaseModel):
    """Object holding the Klyqa device Wi-Fi information.

    This object holds wireles information about the Klyqa device.

    Attributes
    ----------
        security: The security setting of the Wi-Fi network connected.
        rssi: The signal strength in dBm of the Wi-Fi network connected.
        channel: The channel of the Wi-Fi network the device is connected to.

    """

    security: str
    rssi: int
    channel: int


@dataclass
class ChipInfo(BaseModel):
    """Object holding the Klyqa device chip information.

    This object holds information about the Klyqa device chip.

    Attributes
    ----------
        version: The version of the chip
        model: The model of the chip.
        features: The chip features.

    """

    version: str
    model: str
    features: str


# @dataclass
# class CloudSettings(BaseModel):
#     """Object holding the Klyqa Device settings in cloud.

#     Attributes
#     ----------
#         device_name: Name of the device in the cloud

#     """

#     device_name: str


@dataclass
class CloudInfo(BaseModel):
    """Object holding the Klyqa device cloud information.

    This object holds information about the Klyqa device cloud
    connection.

    Attributes
    ----------
        host: The host the device connects to
        port: The port the device connects to
        enabled: The flag to disable the cloud feature.

    """

    host: str
    port: int
    enabled: bool


@dataclass
class GeoInfo(BaseModel):
    """Object holding the Klyqa device geo information.

    This object holds information about the Klyqa device geo
    settings.

    Attributes
    ----------
        timezone: The Posix timezone string
        lat: The latitude of the device
        lon: The longitude of the device.

    """

    timezone: str
    lat: float
    lon: float


@dataclass
# pylint: disable-next=too-many-instance-attributes
class Info(BaseModel):
    """Object holding the Klyqa Light device information.

    This object holds information about the Klyqa Light.

    Attributes
    ----------
        firmware_date: Date where this firmware was build.
        firmware_branch: A string with the branch of the firmware.
        firmware_version: String containing the firmware version.
        sdk_version: String containing the SDK version.
        hardware_revision: An integer indicating the board revision.
        product_id: The product name.
        device_id: Device ID of the Klyqa Light.
        service_name: Service name of the Klyqa Light.
        device_group: Device group string of the Klyqa Light.
        device_order: Device order number of the Klyqa Light.
        chip_info: Chip information of the Klyqa Light.
        cloud: Cloud information of the Klyqa Light.
        geo: Geo information of the Klyqa Light.

    """

    firmware_version: str = field(metadata=field_options(alias="app_ver"))
    firmware_date: str = field(metadata=field_options(alias="build_date"))
    firmware_branch: str = field(metadata=field_options(alias="branch"))
    sdk_version: str = field(metadata=field_options(alias="sdk_ver"))
    hardware_revision: int = field(metadata=field_options(alias="hw_revision"))
    product_id: str = field(metadata=field_options(alias="product_id"))
    device_id: str = field(metadata=field_options(alias="device_id"))
    service_name: str = field(metadata=field_options(alias="service_name"))
    device_order: int = field(metadata=field_options(alias="order"))

    chip_info: ChipInfo = field(metadata=field_options(alias="chip_info"))
    cloud: CloudInfo = field(metadata=field_options(alias="cloud"))
    geo: GeoInfo = field(metadata=field_options(alias="geo"))

    device_group: str | None = field(
        metadata=field_options(alias="group"), default=None
    )


class PowerOnBehavior(IntEnum):
    """Enum for the power on behavior of the Klyqa Light."""

    UNKNOWN = 0
    RESTORE_LAST = 1
    USE_DEFAULTS = 2


@dataclass
class FadeDuration:
    """Class to store switch fading duration values."""

    fadein: int = field(metadata=field_options(alias="in"))
    fadeout: int = field(metadata=field_options(alias="out"))


@dataclass
class RGBColor:
    """Class to store RGB color values."""

    red: int  # Value between 0 and 255
    green: int  # Value between 0 and 255
    blue: int  # Value between 0 and 255

    def __post_init__(self):
        # Ensure RGB values are within range.
        assert 0 <= self.red <= 255, "Red value must be between 0 and 255"
        assert 0 <= self.green <= 255, "Green value must be between 0 and 255"
        assert 0 <= self.blue <= 255, "Blue value must be between 0 and 255"


@dataclass
class Brightness:
    """Class to store Brgihtness percentage value."""

    percentage: int  # Value between 0 and 100

    def __post_init__(self) -> None:
        assert 0 <= self.percentage <= 100, "Red value must be between 0 and 255"


@dataclass
class ExternalConfig:
    """Class to store External Configuration values."""

    port: int
    channel: int
    universe: int
    autoreset: int
    mode: str


@dataclass
class State(BaseModel):
    """Object holding the Klyqa Light state.

    Represents a visible state of an Klyqa Light.

    Attributes
    ----------
        on: A boolean indicating the if the light if on or off.
        brightness: An integer between 0 and 100, representing the brightness.
        rgb: A tuple representing RGB color values.
        temperature: An integer representing the color temperature in mireds.

    """

    on: str = field(metadata=field_options(alias="status"))
    mode: str
    brightness: Brightness
    power_on_behaviour: int = field(metadata=field_options(alias="power_on"))
    active_command: int
    active_scene: str

    wifi_parameters: Wifi
    color: Optional[RGBColor] = None
    fade: FadeDuration | None = field(default=None)
    external: ExternalConfig | None = field(default=None)
    temperature: int | None = field(default=None)
    open_slots: int | None = field(default=None)

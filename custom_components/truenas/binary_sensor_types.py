"""Definitions for TrueNAS binary sensor entities."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List
from homeassistant.components.binary_sensor import (
    BinarySensorEntityDescription,
)

DEVICE_ATTRIBUTES_POOL = [
    "path",
    "status",
    "healthy",
    "is_decrypted",
    "autotrim",
    "scrub_state",
    "scrub_start",
    "scrub_end",
    "scrub_secs_left",
    "available_gib",
    "total_gib",
]

@dataclass
class TrueNASBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Class describing entities."""

    icon_enabled: str | None = None
    icon_disabled: str | None = None
    ha_group: str | None = None
    ha_connection: str | None = None
    ha_connection_value: str | None = None
    data_path: str | None = None
    data_is_on: str = "available"
    data_name: str | None = None
    data_uid: str | None = None
    data_reference: str | None = None
    data_attributes_list: List = field(default_factory=lambda: [])
    func: str = "TrueNASBinarySensor"

SENSOR_TYPES: tuple[BinarySensorEntityDescription, ...] = (
    TrueNASBinarySensorEntityDescription(
        key="pool_healthy",
        name="healthy",
        icon_enabled="mdi:database",
        icon_disabled="mdi:database-off",
        device_class=None,
        entity_category=None,
        ha_group="System",
        data_path="pool",
        data_is_on="healthy",
        data_name="name",
        data_uid="",
        data_reference="guid",
        data_attributes_list=DEVICE_ATTRIBUTES_POOL,
    ),
)

SENSOR_SERVICES = []

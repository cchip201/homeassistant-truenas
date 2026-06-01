"""Definitions for TrueNAS button entities."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from homeassistant.components.button import (
    ButtonEntityDescription,
    ButtonDeviceClass,
)
from homeassistant.helpers.entity import EntityCategory

@dataclass
class TrueNASButtonEntityDescription(ButtonEntityDescription):
    """Class describing entities."""

    ha_group: str | None = None
    data_path: str | None = None
    data_name: str | None = None
    data_uid: str | None = None
    data_reference: str | None = None
    data_attribute: str | None = None
    data_attributes_list: List = field(default_factory=lambda: [])
    func: str = "TrueNASButton"


SENSOR_TYPES: tuple[TrueNASButtonEntityDescription, ...] = (
    TrueNASButtonEntityDescription(
        key="system_reboot",
        name="Reboot",
        icon="mdi:restart",
        device_class=ButtonDeviceClass.RESTART,
        entity_category=EntityCategory.CONFIG,
        ha_group="System",
        data_path="system_info",
        data_name="",
        data_uid="",
        data_reference="",
        data_attribute="hostname",
        func="TrueNASRebootButton",
    ),
    TrueNASButtonEntityDescription(
        key="system_shutdown",
        name="Shutdown",
        icon="mdi:power",
        device_class=None,
        entity_category=EntityCategory.CONFIG,
        ha_group="System",
        data_path="system_info",
        data_name="",
        data_uid="",
        data_reference="",
        data_attribute="hostname",
        func="TrueNASShutdownButton",
    ),
)

SENSOR_SERVICES = []


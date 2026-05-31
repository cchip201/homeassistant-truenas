"""Definitions for TrueNAS switch entities."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List
from homeassistant.components.switch import (
    SwitchEntityDescription,
    SwitchDeviceClass,
)

DEVICE_ATTRIBUTES_JAIL = [
    "comment",
    "jail_zfs_dataset",
    "last_started",
    "ip4_addr",
    "ip6_addr",
    "release",
    "type",
    "plugin_name",
]

DEVICE_ATTRIBUTES_VM = [
    "description",
    "vcpus",
    "memory",
    "autostart",
    "cores",
    "threads",
]

DEVICE_ATTRIBUTES_SERVICE = [
    "enable",
    "state",
]

DEVICE_ATTRIBUTES_APP = [
    "name",
    "version",
    "human_version",
    "update_available",
    "image_updates_available",
    "portal",
]

@dataclass
class TrueNASSwitchEntityDescription(SwitchEntityDescription):
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
    func: str = "TrueNASSwitch"

SWITCH_TYPES: tuple[TrueNASSwitchEntityDescription, ...] = (
    TrueNASSwitchEntityDescription(
        key="jail",
        name="",
        icon_enabled="mdi:layers",
        icon_disabled="mdi:layers-off",
        device_class=SwitchDeviceClass.SWITCH,
        entity_category=None,
        ha_group="Jails",
        data_path="jail",
        data_is_on="state",
        data_name="host_hostname",
        data_uid="",
        data_reference="id",
        data_attributes_list=DEVICE_ATTRIBUTES_JAIL,
        func="TrueNASJailSwitch",
    ),
    TrueNASSwitchEntityDescription(
        key="vm",
        name="",
        icon_enabled="mdi:server",
        icon_disabled="mdi:server-off",
        device_class=SwitchDeviceClass.SWITCH,
        entity_category=None,
        ha_group="VMs",
        data_path="vm",
        data_is_on="running",
        data_name="name",
        data_uid="",
        data_reference="id",
        data_attributes_list=DEVICE_ATTRIBUTES_VM,
        func="TrueNASVMSwitch",
    ),
    TrueNASSwitchEntityDescription(
        key="service",
        name="",
        icon_enabled="mdi:cog",
        icon_disabled="mdi:cog-off",
        device_class=SwitchDeviceClass.SWITCH,
        entity_category=None,
        ha_group="Services",
        data_path="service",
        data_is_on="running",
        data_name="service",
        data_uid="",
        data_reference="id",
        data_attributes_list=DEVICE_ATTRIBUTES_SERVICE,
        func="TrueNASServiceSwitch",
    ),
    TrueNASSwitchEntityDescription(
        key="app",
        name="",
        icon_enabled="mdi:server",
        icon_disabled="mdi:server-off",
        device_class=SwitchDeviceClass.SWITCH,
        entity_category=None,
        ha_group="Apps",
        data_path="app",
        data_is_on="running",
        data_name="name",
        data_uid="",
        data_reference="id",
        data_attributes_list=DEVICE_ATTRIBUTES_APP,
        func="TrueNASAppSwitch",
    ),
)

"""TrueNAS switch platform."""

from __future__ import annotations
from logging import getLogger
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .switch_types import SENSOR_TYPES, SENSOR_SERVICES
from .entity import TrueNASEntity, async_add_entities

_LOGGER = getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    _async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up switch platform."""
    dispatcher = {
        "TrueNASSwitch": TrueNASSwitch,
        "TrueNASJailSwitch": TrueNASJailSwitch,
        "TrueNASVMSwitch": TrueNASVMSwitch,
        "TrueNASServiceSwitch": TrueNASServiceSwitch,
        "TrueNASAppSwitch": TrueNASAppSwitch,
    }
    await async_add_entities(hass, config_entry, dispatcher)

class TrueNASSwitch(TrueNASEntity, SwitchEntity):
    """Define an TrueNAS Switch."""

    @property
    def is_on(self) -> bool:
        """Return true if device is on."""
        return bool(self._data.get(self.entity_description.data_is_on))

    @property
    def icon(self) -> str:
        """Return the icon."""
        if self.entity_description.icon_enabled:
            if self.is_on:
                return self.entity_description.icon_enabled
            else:
                return self.entity_description.icon_disabled
        return super().icon

class TrueNASJailSwitch(TrueNASSwitch):
    """Define a TrueNAS Jail Switch."""

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Start a Jail."""
        tmp_jail = await self.hass.async_add_executor_job(
            self.coordinator.api.query, f"jail/id/{self._data['id']}"
        )
        if "state" not in tmp_jail or tmp_jail["state"] != "down":
            _LOGGER.warning("Jail %s (%s) is not down", self._data["comment"], self._data["id"])
            return
        await self.hass.async_add_executor_job(
            self.coordinator.api.query, "jail/start", "post", self._data["id"]
        )
        await self.coordinator.async_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Stop a Jail."""
        tmp_jail = await self.hass.async_add_executor_job(
            self.coordinator.api.query, f"jail/id/{self._data['id']}"
        )
        if "state" not in tmp_jail or tmp_jail["state"] != "up":
            _LOGGER.warning("Jail %s (%s) is not up", self._data["comment"], self._data["id"])
            return
        await self.hass.async_add_executor_job(
            self.coordinator.api.query, "jail/stop", "post", {"jail": self._data["id"]}
        )
        await self.coordinator.async_refresh()

class TrueNASVMSwitch(TrueNASSwitch):
    """Define a TrueNAS VM Switch."""

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Start a VM."""
        tmp_vm = await self.hass.async_add_executor_job(
            self.coordinator.api.query, f"vm/id/{self._data['id']}"
        )
        if "status" not in tmp_vm or tmp_vm["status"]["state"] != "STOPPED":
            _LOGGER.warning("VM %s (%s) is not stopped", self._data["name"], self._data["id"])
            return
        await self.hass.async_add_executor_job(
            self.coordinator.api.query,
            f"vm/id/{self._data['id']}/start",
            "post",
            {"overcommit": False},
        )
        await self.coordinator.async_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Stop a VM."""
        tmp_vm = await self.hass.async_add_executor_job(
            self.coordinator.api.query, f"vm/id/{self._data['id']}"
        )
        if "status" not in tmp_vm or tmp_vm["status"]["state"] != "RUNNING":
            _LOGGER.warning("VM %s (%s) is not running", self._data["name"], self._data["id"])
            return
        await self.hass.async_add_executor_job(
            self.coordinator.api.query, f"vm/id/{self._data['id']}/stop", "post"
        )
        await self.coordinator.async_refresh()

class TrueNASServiceSwitch(TrueNASSwitch):
    """Define a TrueNAS Service Switch."""

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Start a Service."""
        tmp_service = await self.hass.async_add_executor_job(
            self.coordinator.api.query, f"service/id/{self._data['id']}"
        )
        if "state" not in tmp_service or tmp_service["state"] != "STOPPED":
            _LOGGER.warning("Service %s (%s) is not stopped", self._data["service"], self._data["id"])
            return
        await self.hass.async_add_executor_job(
            self.coordinator.api.query,
            "service/start",
            "post",
            {"service": self._data["service"]},
        )
        await self.coordinator.async_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Stop a Service."""
        tmp_service = await self.hass.async_add_executor_job(
            self.coordinator.api.query, f"service/id/{self._data['id']}"
        )
        if "state" not in tmp_service or tmp_service["state"] == "STOPPED":
            _LOGGER.warning("Service %s (%s) is not running", self._data["service"], self._data["id"])
            return
        await self.hass.async_add_executor_job(
            self.coordinator.api.query,
            "service/stop",
            "post",
            {"service": self._data["service"]},
        )
        await self.coordinator.async_refresh()

class TrueNASAppSwitch(TrueNASSwitch):
    """Define a TrueNAS Applications Switch."""

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Start an App."""
        tmp_vm = await self.hass.async_add_executor_job(
            self.coordinator.api.query, f"/chart/release/id/{self._data['id']}"
        )
        if "status" not in tmp_vm or tmp_vm["status"] == "ACTIVE":
            _LOGGER.warning("App %s (%s) is already running", self._data["name"], self._data["id"])
            return
        await self.hass.async_add_executor_job(
            self.coordinator.api.query,
            "/chart/release/scale",
            "post",
            {"release_name": self._data["id"], "scale_options": {"replica_count": 1}},
        )
        await self.coordinator.async_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Stop an App."""
        tmp_vm = await self.hass.async_add_executor_job(
            self.coordinator.api.query, f"/chart/release/id/{self._data['id']}"
        )
        if "status" not in tmp_vm or tmp_vm["status"] != "ACTIVE":
            _LOGGER.warning("App %s (%s) is not running", self._data["name"], self._data["id"])
            return
        await self.hass.async_add_executor_job(
            self.coordinator.api.query,
            "/chart/release/scale",
            "post",
            {"release_name": self._data["id"], "scale_options": {"replica_count": 0}},
        )
        await self.coordinator.async_refresh()

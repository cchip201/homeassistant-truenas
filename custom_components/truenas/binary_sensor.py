"""TrueNAS binary sensor platform."""

from __future__ import annotations
from logging import getLogger

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .binary_sensor_types import (
    SENSOR_SERVICES,
    SENSOR_TYPES,
)
from .entity import TrueNASEntity, async_add_entities

_LOGGER = getLogger(__name__)


# ---------------------------
#   async_setup_entry
# ---------------------------
async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    _async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up device tracker for OpenMediaVault component."""
    dispatcher = {
        "TrueNASBinarySensor": TrueNASBinarySensor,
    }
    await async_add_entities(hass, config_entry, dispatcher)


# ---------------------------
#   TrueNASBinarySensor
# ---------------------------
class TrueNASBinarySensor(TrueNASEntity, BinarySensorEntity):
    """Define an TrueNAS Binary Sensor."""

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

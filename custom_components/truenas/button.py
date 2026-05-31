"""TrueNAS button platform."""

from __future__ import annotations

from logging import getLogger

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import TrueNASCoordinator
from .entity import TrueNASEntity, async_add_entities
from .button_types import BUTTON_TYPES

_LOGGER = getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    _async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up entry for TrueNAS component."""
    dispatcher = {
        "TrueNASButton": TrueNASButton,
        "TrueNASRebootButton": TrueNASRebootButton,
        "TrueNASShutdownButton": TrueNASShutdownButton,
    }
    await async_add_entities(hass, config_entry, dispatcher)

class TrueNASButton(TrueNASEntity, ButtonEntity):
    """Define a TrueNAS button."""

class TrueNASRebootButton(TrueNASButton):
    """Define a TrueNAS Reboot button."""
    async def async_press(self) -> None:
        """Handle the button press."""
        await self.hass.async_add_executor_job(
            self.coordinator.api.query,
            "system/reboot",
            "post",
        )

class TrueNASShutdownButton(TrueNASButton):
    """Define a TrueNAS Shutdown button."""
    async def async_press(self) -> None:
        """Handle the button press."""
        await self.hass.async_add_executor_job(
            self.coordinator.api.query,
            "system/shutdown",
            "post",
        )

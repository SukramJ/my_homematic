"""number for my_homematic."""
from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.components.number import NumberEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .generic_pull_entity import HaHomematicGenericPullEntity

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=30)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the number platform."""
    add_entities([PullNumber(hass=hass, config=config)])


class PullNumber(HaHomematicGenericPullEntity, NumberEntity):
    """Representation of a number."""

    def __init__(self, hass: HomeAssistant, config: ConfigType) -> None:
        super().__init__(hass=hass, config=config)
        self._attr_value = 0.0

    async def async_update(self) -> None:
        """Fetch new state data for the number.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._attr_value = await self._get_data() * self._multiplicator

    async def async_set_value(self, value: float) -> None:
        """Update the current value."""
        self._attr_value = value
        if value == 0:
            await self._send_data(0)
        else:
            await self._send_data(value/self._multiplicator)


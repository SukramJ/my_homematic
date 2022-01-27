"""binary_sensor for my_homematic."""
from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.components.binary_sensor import BinarySensorEntity
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
    """Set up the binary sensor platform."""
    add_entities([PullBinarySensor(hass=hass, config=config)])


class PullBinarySensor(HaHomematicGenericPullEntity, BinarySensorEntity):
    """Representation of a binary sensor."""

    def __init__(self, hass: HomeAssistant, config: ConfigType) -> None:
        super().__init__(hass=hass, config=config)

    async def async_update(self) -> None:
        """Fetch new state data for the binary sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._attr_is_on = bool(await self._get_data())

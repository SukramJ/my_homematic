"""sensor for my_homematic."""
from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.components.sensor import SensorEntity
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
    """Set up the sensor platform."""
    add_entities([PullSensor(hass=hass, config=config)])


class PullSensor(HaHomematicGenericPullEntity, SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, hass: HomeAssistant, config: ConfigType) -> None:
        super().__init__(hass=hass, config=config)
        self._attr_native_unit_of_measurement = config.get("unit")

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._attr_native_value = await self._get_data()

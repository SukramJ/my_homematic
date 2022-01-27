""" Generic pull entity."""
from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

import hahomematic.client as hm_client

from homeassistant.const import (
    CONF_ADDRESS,
    CONF_DEVICE_CLASS,
    CONF_NAME,
    CONF_UNIQUE_ID,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import PARENT_DOMAIN

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=30)

CONF_INTERFACE_ID = "interface_id"
CONF_PARAMETER = "parameter"
CONF_PARAMSET_KEY = "paramset_key"
CONF_STATE_CLASS = "state_class"
DEFAULT_PARAMSET_KEY = "VALUES"


class HaHomematicGenericPullEntity:
    """Generic base class for pull entities."""

    def __init__(self, hass: HomeAssistant, config: ConfigType) -> None:
        """Initialize the generic pull entity."""
        self._hass = hass
        self._config = config
        self._attr_name = config[CONF_NAME]
        if unique_id := config.get(CONF_UNIQUE_ID):
            self._attr_unique_id = unique_id
        self._interface_id = config[CONF_INTERFACE_ID]
        self._address = config[CONF_ADDRESS]
        self._parameter = config[CONF_PARAMETER]
        self._paramset_key = config.get(CONF_PARAMSET_KEY, DEFAULT_PARAMSET_KEY)
        if device_class := config.get(CONF_DEVICE_CLASS):
            self._attr_device_class = device_class
        if state_class := config.get(CONF_STATE_CLASS):
            self._attr_state_class = state_class
        self._client: hm_client.Client | None = None

    async def _get_data(self) -> Any:
        """Get data from CCU."""
        if (client := self._get_client()) is None:
            _LOGGER.debug("Client is not available")
            return None
        paramset = await client.get_paramset(self._address, self._paramset_key)
        if (value := paramset.get(self._parameter)) is not None:
            return value
        return None

    async def _send_data(self, value: Any) -> None:
        """Send data to CCU."""
        paramset = {self._parameter: value}
        if client := self._get_client():
            await client.put_paramset(
                channel_address=self._address,
                paramset_key=self._paramset_key,
                value=paramset,
            )
        else:
            _LOGGER.warning("Client is not available")

    def _get_client(self) -> hm_client.Client | None:
        """get client from central unit by interface_id."""
        if self._client is None:
            for control_unit in self._hass.data[PARENT_DOMAIN].values():
                if client := control_unit.central.get_client_by_interface_id(
                    self._interface_id
                ):
                    self._client = client
                    break
        return self._client

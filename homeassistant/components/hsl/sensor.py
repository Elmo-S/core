"""Sensor entity thing."""
from datetime import timedelta
import logging

import async_timeout

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=60)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Config entry."""
    my_api = hass.data[DOMAIN][entry.entry_id]
    coordinator = MyCoordinator(hass, my_api)

    await coordinator.async_config_entry_first_refresh()

    async_add_entities(
        [
            MyEntity(coordinator=coordinator, idx=idx, name="Boink")
            for idx, ent in enumerate(coordinator.data)
        ],
        True,
    )


class PublicTransportSensor(SensorEntity):
    """HSL transport integration class."""

    def __init__(self, name, station):
        """Initialize the sensor."""
        self._name = name
        self._station = station

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return self._name


class MyCoordinator(DataUpdateCoordinator):
    """Testing."""

    def __init__(self, hass, my_api):
        """Initialize the coordinator."""
        super().__init__(
            hass, _LOGGER, name="Namer", update_interval=timedelta(seconds=60)
        )
        self.my_api = my_api

    async def _async_update_data(self):
        """Play fetch."""
        async with async_timeout.timeout(10):
            return await self.my_api.fetch_data()


class MyEntity(CoordinatorEntity, SensorEntity):
    """Testing the tests."""

    def __init__(self, coordinator, idx, name):
        """Pass the coordinator to CoordinatorEntity."""
        super().__init__(coordinator)
        self.idx = idx
        self._name = name

    @property
    def name(self) -> str:
        """Return name."""
        return self._name

    @property
    def native_value(self):
        """Set state of entity."""
        return "buuuuuip"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""
        self._attr_state = self.coordinator.data[self.idx]["state"]
        self.async_write_ha_state()

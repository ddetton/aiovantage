"""Asynchronous Python library for controlling Vantage InFusion controllers."""

import asyncio
from collections.abc import Callable, Iterator
from ssl import SSLContext
from types import TracebackType
from typing import Any, TypeVar, cast

from typing_extensions import Self

from ._connection import BaseConnection
from ._controllers.events import EventCallback, VantageEvent
from ._logger import logger
from .command_client import CommandClient, EventStream
from .config_client import ConfigClient
from .controllers import (
    AnemoSensorsController,
    AreasController,
    BackBoxesController,
    BaseController,
    BlindGroupsController,
    BlindsController,
    ButtonsController,
    DryContactsController,
    GMemController,
    LightSensorsController,
    LoadGroupsController,
    LoadsController,
    MastersController,
    ModulesController,
    OmniSensorsController,
    PortDevicesController,
    PowerProfilesController,
    RGBLoadsController,
    StationsController,
    TasksController,
    TemperatureSensorsController,
    ThermostatsController,
)
from .objects import SystemObject

__all__ = ["Vantage", "VantageEvent", "logger"]

ControllerT = TypeVar("ControllerT", bound=BaseController[Any])


class Vantage:
    """Main client for interacting with Vantage systems.

    The Vantage class manages the various connections to a Vantage system, as well as
    exposing "controllers" for fetching and interacting with objects in the system.
    """

    def __init__(
        self,
        host: str,
        username: str | None = None,
        password: str | None = None,
        *,
        ssl: SSLContext | bool = True,
        config_port: int | None = None,
        command_port: int | None = None,
    ) -> None:
        """Initialize the Vantage instance.

        Args:
            host: The hostname or IP address of the Vantage controller.
            username: The username to use for authentication.
            password: The password to use for authentication.
            ssl: The SSL context to use. True will use the default context, False will disable SSL.
            config_port: The port to use for the config client.
            command_port: The port to use for the command client.
        """
        # Set up clients
        self._host = host
        self._config_client = ConfigClient(
            host, username, password, ssl=ssl, port=config_port
        )

        self._command_client = CommandClient(
            host, username, password, ssl=ssl, port=command_port
        )

        self._event_stream = EventStream(
            host, username, password, ssl=ssl, port=command_port
        )

        # Set up controllers
        def add_controller(controller_cls: type[ControllerT]) -> ControllerT:
            controller = controller_cls(self)
            self._controllers.add(controller)
            return controller

        self._controllers: set[BaseController[Any]] = set()
        self._anemo_sensors = add_controller(AnemoSensorsController)
        self._areas = add_controller(AreasController)
        self._back_boxes = add_controller(BackBoxesController)
        self._blind_groups = add_controller(BlindGroupsController)
        self._blinds = add_controller(BlindsController)
        self._buttons = add_controller(ButtonsController)
        self._dry_contacts = add_controller(DryContactsController)
        self._gmem = add_controller(GMemController)
        self._light_sensors = add_controller(LightSensorsController)
        self._load_groups = add_controller(LoadGroupsController)
        self._loads = add_controller(LoadsController)
        self._masters = add_controller(MastersController)
        self._modules = add_controller(ModulesController)
        self._rgb_loads = add_controller(RGBLoadsController)
        self._omni_sensors = add_controller(OmniSensorsController)
        self._port_devices = add_controller(PortDevicesController)
        self._power_profiles = add_controller(PowerProfilesController)
        self._stations = add_controller(StationsController)
        self._tasks = add_controller(TasksController)
        self._temperature_sensors = add_controller(TemperatureSensorsController)
        self._thermostats = add_controller(ThermostatsController)

    def __getitem__(self, vid: int) -> SystemObject:
        """Return the object with the given Vantage ID."""
        for controller in self._controllers:
            if vid in controller:
                return cast(SystemObject, controller[vid])
        raise KeyError(vid)

    def __contains__(self, vid: int) -> bool:
        """Is the given Vantage ID known by any controller."""
        return any(vid in controller for controller in self._controllers)

    def __iter__(self) -> Iterator[SystemObject]:
        """Iterate over all objects known by the controllers."""
        for controller in self._controllers:
            yield from controller

    async def __aenter__(self) -> Self:
        """Return context manager."""
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Exit context manager."""
        self.close()
        if exc_val:
            raise exc_val

    @property
    def host(self) -> str:
        """The hostname or IP address of the Vantage controller."""
        return self._host

    @property
    def config_client(self) -> ConfigClient:
        """The config client instance."""
        return self._config_client

    @property
    def command_client(self) -> CommandClient:
        """The command client instance."""
        return self._command_client

    @property
    def event_stream(self) -> EventStream:
        """The event stream instance."""
        return self._event_stream

    @property
    def anemo_sensors(self) -> AnemoSensorsController:
        """Controller for interacting with wind speed sensors."""
        return self._anemo_sensors

    @property
    def areas(self) -> AreasController:
        """Controller for interacting with areas."""
        return self._areas

    @property
    def back_boxes(self) -> BackBoxesController:
        """Controller for interacting with back boxes."""
        return self._back_boxes

    @property
    def blinds(self) -> BlindsController:
        """Controller for interacting with blinds."""
        return self._blinds

    @property
    def blind_groups(self) -> BlindGroupsController:
        """Controller for interacting with groups of blinds."""
        return self._blind_groups

    @property
    def buttons(self) -> ButtonsController:
        """Controller for interacting with keypad buttons."""
        return self._buttons

    @property
    def dry_contacts(self) -> DryContactsController:
        """Controller for interacting with dry contacts."""
        return self._dry_contacts

    @property
    def gmem(self) -> GMemController:
        """Controller for interacting with variables."""
        return self._gmem

    @property
    def light_sensors(self) -> LightSensorsController:
        """Controller for interacting with light sensors."""
        return self._light_sensors

    @property
    def loads(self) -> LoadsController:
        """Controller for interacting with loads (lights, fans, etc)."""
        return self._loads

    @property
    def load_groups(self) -> LoadGroupsController:
        """Controller for interacting with groups of loads."""
        return self._load_groups

    @property
    def masters(self) -> MastersController:
        """Controller for interacting with Vantage Controllers."""
        return self._masters

    @property
    def modules(self) -> ModulesController:
        """Controller for interacting with dimmer modules."""
        return self._modules

    @property
    def omni_sensors(self) -> OmniSensorsController:
        """Controller for interacting with "omni" sensors."""
        return self._omni_sensors

    @property
    def port_devices(self) -> PortDevicesController:
        """Controller for interacting with port devices."""
        return self._port_devices

    @property
    def power_profiles(self) -> PowerProfilesController:
        """Controller for interacting with power profiles."""
        return self._power_profiles

    @property
    def rgb_loads(self) -> RGBLoadsController:
        """Controller for interacting with RGB loads."""
        return self._rgb_loads

    @property
    def stations(self) -> StationsController:
        """Controller for interacting with stations (keypads, etc)."""
        return self._stations

    @property
    def tasks(self) -> TasksController:
        """Controller for interacting with tasks."""
        return self._tasks

    @property
    def temperature_sensors(self) -> TemperatureSensorsController:
        """Controller for interacting with temperature sensors."""
        return self._temperature_sensors

    @property
    def thermostats(self) -> ThermostatsController:
        """Controller for interacting with thermostats."""
        return self._thermostats

    def get(self, vid: int) -> SystemObject | None:
        """Return the object with the given Vantage ID, or None if not found."""
        try:
            return self[vid]
        except KeyError:
            return None

    def close(self) -> None:
        """Close all client connections."""
        self.config_client.close()
        self.command_client.close()
        self.event_stream.stop()

    async def initialize(
        self, *, fetch_state: bool = True, monitor_state: bool = True
    ) -> None:
        """Initialize all controllers.

        Args:
            fetch_state: Whether to fetch the state of stateful objects.
            monitor_state: Whether to keep the state of stateful objects up-to-date.
        """
        # Initialize all controllers
        await asyncio.gather(
            *[
                controller.initialize(
                    fetch_state=fetch_state,
                    monitor_state=monitor_state,
                )
                for controller in self._controllers
            ]
        )

    def subscribe(self, callback: EventCallback[SystemObject]) -> Callable[[], None]:
        """Subscribe to state changes for every controller.

        Args:
            callback: The callback to call when an object changes.

        Returns:
            A function to unsubscribe.
        """
        unsubscribes = [
            controller.subscribe(callback) for controller in self._controllers
        ]

        def unsubscribe() -> None:
            for unsub in unsubscribes:
                unsub()

        return unsubscribe

    @classmethod
    def set_ssl_context_factory(cls, factory: Callable[[], SSLContext]) -> None:
        """Set the SSL context factory for all instances."""
        BaseConnection.ssl_context_factory = factory

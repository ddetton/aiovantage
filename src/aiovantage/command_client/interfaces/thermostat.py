"""Interface for querying and controlling thermostats."""

from decimal import Decimal
from enum import IntEnum

from .base import Interface


class ThermostatInterface(Interface):
    """Interface for querying and controlling thermostats."""

    class OperationMode(IntEnum):
        """The operation mode of the thermostat."""

        Off = 0
        Cool = 1
        Heat = 2
        Auto = 3
        Unknown = 4

    class FanMode(IntEnum):
        """The fan mode of the thermostat."""

        Off = 0
        On = 1
        Unknown = 2

    class DayMode(IntEnum):
        """The day mode of the thermostat."""

        Day = 0
        Night = 1
        Unknown = 2
        Standby = 3

    class HoldMode(IntEnum):
        """The hold mode of the thermostat."""

        Normal = 0
        Hold = 1
        Unknown = 2

    class Status(IntEnum):
        """The status of the thermostat."""

        Off = 0
        Cooling = 1
        Heating = 2
        Offline = 3

    async def get_indoor_temperature(self, vid: int) -> Decimal:
        """Get the current indoor temperature.

        Args:
            vid: The Vantage ID of the thermostat.
        """
        # INVOKE <id> Thermostat.GetIndoorTemperature
        # -> R:INVOKE <id> <temp> Thermostat.GetIndoorTemperature
        response = await self.invoke(vid, "Thermostat.GetIndoorTemperature")
        temp = Decimal(response.args[1])

        return temp

    async def get_outdoor_temperature(self, vid: int) -> Decimal:
        """Get the current outdoor temperature.

        Args:
            vid: The Vantage ID of the thermostat.
        """
        # INVOKE <id> Thermostat.GetOutdoorTemperature
        # -> R:INVOKE <id> <temp> Thermostat.GetOutdoorTemperature
        response = await self.invoke(vid, "Thermostat.GetOutdoorTemperature")
        temp = Decimal(response.args[1])

        return temp

    async def get_heat_set_point(self, vid: int) -> Decimal:
        """Get the current heat set point.

        Args:
            vid: The Vantage ID of the thermostat.

        Returns:
            The heat set point of the thermostat, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.GetHeatSetPoint
        # -> R:INVOKE <id> <temp> Thermostat.GetHeatSetPoint
        response = await self.invoke(vid, "Thermostat.GetHeatSetPoint")
        temp = Decimal(response.args[1])

        return temp

    async def set_heat_set_point(self, vid: int, temp: float) -> None:
        """Set the current heat set point.

        Args:
            vid: The Vantage ID of the thermostat.
            temp: The heat set point to set, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.SetHeatSetPoint <temp>
        # -> R:INVOKE <id> Thermostat.SetHeatSetPoint <temp>
        await self.invoke(vid, "Thermostat.SetHeatSetPoint", temp)

    async def get_cool_set_point(self, vid: int) -> Decimal:
        """Get the current cool set point.

        Args:
            vid: The Vantage ID of the thermostat.

        Returns:
            The cool set point of the thermostat, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.GetCoolSetPoint
        # -> R:INVOKE <id> <temp> Thermostat.GetCoolSetPoint
        response = await self.invoke(vid, "Thermostat.GetCoolSetPoint")
        temp = Decimal(response.args[1])

        return temp

    async def set_cool_set_point(self, vid: int, temp: float) -> None:
        """Set the current cool set point.

        Args:
            vid: The Vantage ID of the thermostat.
            temp: The cool set point to set, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.SetCoolSetPoint <temp>
        # -> R:INVOKE <id> Thermostat.SetCoolSetPoint <temp>
        await self.invoke(vid, "Thermostat.SetCoolSetPoint", temp)

    async def get_operation_mode(self, vid: int) -> OperationMode:
        """Get the current operation mode.

        Args:
            vid: The Vantage ID of the thermostat.

        Returns:
            The operation mode of the thermostat.
        """
        # INVOKE <id> Thermostat.GetOperationMode
        # -> R:INVOKE <id> <mode> Thermostat.GetOperationMode
        response = await self.invoke(vid, "Thermostat.GetOperationMode")
        mode = self.OperationMode[response.args[1]]

        return mode

    async def set_operation_mode(self, vid: int, mode: OperationMode) -> None:
        """Set the current operation mode.

        Args:
            vid: The Vantage ID of the thermostat.
            mode: The operation mode to set.
        """
        # INVOKE <id> Thermostat.SetOperationMode <mode>
        # -> R:INVOKE <id> Thermostat.SetOperationMode <mode>
        await self.invoke(vid, "Thermostat.SetOperationMode", mode)

    async def get_fan_mode(self, vid: int) -> FanMode:
        """Get the current fan mode.

        Args:
            vid: The Vantage ID of the thermostat.

        Returns:
            The fan mode of the thermostat.
        """
        # INVOKE <id> Thermostat.GetFanMode
        # -> R:INVOKE <id> <mode> Thermostat.GetFanMode
        response = await self.invoke(vid, "Thermostat.GetFanMode")
        mode = self.FanMode[response.args[1]]

        return mode

    async def set_fan_mode(self, vid: int, mode: FanMode) -> None:
        """Set the current fan mode.

        Args:
            vid: The Vantage ID of the thermostat.
            mode: The fan mode to set.
        """
        # INVOKE <id> Thermostat.SetFanMode <mode>
        # -> R:INVOKE <id> Thermostat.SetFanMode <mode>
        await self.invoke(vid, "Thermostat.SetFanMode", mode)

    async def get_day_mode(self, vid: int) -> DayMode:
        """Get the current day mode.

        Args:
            vid: The Vantage ID of the thermostat.

        Returns:
            The day mode of the thermostat.
        """
        # INVOKE <id> Thermostat.GetDayMode
        # -> R:INVOKE <id> <mode> Thermostat.GetDayMode
        response = await self.invoke(vid, "Thermostat.GetDayMode")
        mode = self.DayMode[response.args[1]]

        return mode

    async def set_day_mode(self, vid: int, mode: DayMode) -> None:
        """Set the current day mode.

        Args:
            vid: The Vantage ID of the thermostat.
            mode: The day mode to set.
        """
        # INVOKE <id> Thermostat.SetDayMode <mode>
        # -> R:INVOKE <id> Thermostat.SetDayMode <mode>
        await self.invoke(vid, "Thermostat.SetDayMode", mode)

    async def get_hold_mode(self, vid: int) -> HoldMode:
        """Get the current hold mode.

        Args:
            vid: The Vantage ID of the thermostat.

        Returns:
            The hold mode of the thermostat.
        """
        # INVOKE <id> Thermostat.GetHoldMode
        # -> R:INVOKE <id> <mode> Thermostat.GetHoldMode
        response = await self.invoke(vid, "Thermostat.GetHoldMode")
        mode = self.HoldMode[response.args[1]]

        return mode

    async def set_hold_mode(self, vid: int, mode: HoldMode) -> None:
        """Set the current hold mode.

        Args:
            vid: The Vantage ID of the thermostat.
            mode: The hold mode to set.
        """
        # INVOKE <id> Thermostat.SetHoldMode <mode>
        # -> R:INVOKE <id> Thermostat.SetHoldMode <mode>
        await self.invoke(vid, "Thermostat.SetHoldMode", mode)

    async def get_status(self, vid: int) -> Status:
        """Get the current status.

        Args:
            vid: The Vantage ID of the thermostat.

        Returns:
            The status of the thermostat.
        """
        # INVOKE <id> Thermostat.GetStatus
        # -> R:INVOKE <id> <status> Thermostat.GetStatus
        response = await self.invoke(vid, "Thermostat.GetStatus")
        status = self.Status[response.args[1]]

        return status

    async def get_auto_set_point(self, vid: int) -> Decimal:
        """Get the current auto set point.

        Args:
            vid: The Vantage ID of the thermostat.

        Returns:
            The auto set point of the thermostat, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.GetAutoSetPoint
        # -> R:INVOKE <id> <temp> Thermostat.GetAutoSetPoint
        response = await self.invoke(vid, "Thermostat.GetAutoSetPoint")
        temp = Decimal(response.args[1])

        return temp

    async def set_auto_set_point(self, vid: int, temp: float) -> None:
        """Set the current auto set point.

        Args:
            vid: The Vantage ID of the thermostat.
            temp: The auto set point to set, in degrees Celsius.
        """
        # INVOKE <id> Thermostat.SetAutoSetPoint <temp>
        # -> R:INVOKE <id> Thermostat.SetAutoSetPoint <temp>
        await self.invoke(vid, "Thermostat.SetAutoSetPoint", temp)

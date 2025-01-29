"""Interface for querying and controlling current sensors."""

from decimal import Decimal

from typing_extensions import override

from .base import Interface, method


class CurrentSensorInterface(Interface):
    """Interface for querying and controlling current sensors."""

    interface_name = "CurrentSensor"

    # Properties
    current: Decimal | None = None

    # Methods
    @method("GetCurrent", "GetCurrentHW", property="current")
    async def get_current(self, *, hw: bool = False) -> Decimal:
        """Get the value of a current sensor.

        Args:
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The value of the current sensor, in Amps.
        """
        # INVOKE <id> CurrentSensor.GetCurrent
        # -> R:INVOKE <id> <level> CurrentSensor.GetCurrent
        return await self.invoke(
            "CurrentSensor.GetCurrentHW" if hw else "CurrentSensor.GetCurrent"
        )

    @method("SetCurrent", "SetCurrentSW")
    async def set_current(self, value: Decimal, *, sw: bool = False) -> None:
        """Set the value of a current sensor.

        Args:
            value: The value to set, in Amps.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> CurrentSensor.SetCurrent <level>
        # -> R:INVOKE <id> <rcode> CurrentSensor.SetCurrent <level>
        await self.invoke(
            "CurrentSensor.SetCurrentSW" if sw else "CurrentSensor.SetCurrent",
            value,
        )

    @override
    def handle_category_status(self, category: str, *args: str) -> str | None:
        # STATUS CURRENT
        # -> S:CURRENT <id> <current>
        if category == "CURRENT":
            return self.update_property("current", Decimal(args[0]))

"""Controller holding and managing Vantage temperature sensors."""

from decimal import Decimal

from typing_extensions import override

from aiovantage.objects import Temperature

from .base import BaseController


class TemperatureSensorsController(BaseController[Temperature]):
    """Controller holding and managing Vantage temperature sensors."""

    vantage_types = ("Temperature",)
    """The Vantage object types that this controller will fetch."""

    status_types = ("TEMP",)
    """Which Vantage 'STATUS' types this controller handles, if any."""

    @override
    def handle_category_status(self, obj: Temperature, status: str, *args: str) -> None:
        """Handle simple status message from the event stream."""
        if status != "TEMP":
            return

        # STATUS TEMP
        # -> S:TEMP <id> <temp>
        state = {
            "value": Decimal(args[0]),
        }

        self.update_state(obj, state)

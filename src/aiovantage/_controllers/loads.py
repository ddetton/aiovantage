from aiovantage._controllers.query import QuerySet
from aiovantage.objects import Load

from .base import BaseController


class LoadsController(BaseController[Load]):
    """Loads controller."""

    vantage_types = ("Load",)

    @property
    def on(self) -> QuerySet[Load]:
        """Return a queryset of all loads that are turned on."""
        return self.filter(lambda load: load.is_on)

    @property
    def off(self) -> QuerySet[Load]:
        """Return a queryset of all loads that are turned off."""
        return self.filter(lambda load: not load.is_on)

    @property
    def relays(self) -> QuerySet[Load]:
        """Return a queryset of all loads that are relays."""
        return self.filter(lambda load: load.is_relay)

    @property
    def motors(self) -> QuerySet[Load]:
        """Return a queryset of all loads that are motors."""
        return self.filter(lambda load: load.is_motor)

    @property
    def lights(self) -> QuerySet[Load]:
        """Return a queryset of all loads that are lights."""
        return self.filter(lambda load: load.is_light)

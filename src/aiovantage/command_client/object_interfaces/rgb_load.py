"""Interface for querying and controlling RGB loads."""

import struct
from decimal import Decimal
from enum import IntEnum
from typing import Tuple, Union, cast

from .base import Interface, InterfaceResponse


def parse_color_channel_response(response: InterfaceResponse) -> Tuple[int, int]:
    """Parse a 'RGBLoad.GetRGB', 'RGBLoad.GetRGBW' or 'RGBLoad.GetHSL' response."""
    # -> R:INVOKE <id> <value> RGBLoad.GetRGB <channel>
    # -> S:STATUS <id> RGBLoad.GetRGB <value> <channel>
    # -> EL: <id> RGBLoad.GetRGB <value> <channel>
    value = int(response.result)
    channel = int(response.args[0])

    return channel, value


def parse_packed_color_response(response: InterfaceResponse) -> Tuple[int, ...]:
    """Parse a 'RGBLoad.GetColor' response."""
    # -> R:INVOKE <id> <color> RGBLoad.GetColor
    # -> S:STATUS <id> RGBLoad.GetColor <color>
    # -> EL: <id> RGBLoad.GetColor <color>
    return tuple(struct.pack(">i", int(response.result)))


class RGBLoadInterface(Interface):
    """Interface for querying and controlling RGB loads."""

    class RGBChannel(IntEnum):
        """The RGB color channels."""

        Red = 0
        Green = 1
        Blue = 2
        White = 3

    class HSLAttribute(IntEnum):
        """The HSL color attributes."""

        Hue = 0
        Saturation = 1
        Lightness = 2

    async def set_rgb(self, vid: int, red: int, green: int, blue: int) -> None:
        """Set the color of an RGB load.

        Args:
            vid: The Vantage ID of the RGB load.
            red: The red value of the color, (0-255)
            green: The green value of the color, (0-255)
            blue: The blue value of the color, (0-255)
        """
        # Clamp levels to 0-255
        red = max(min(red, 255), 0)
        green = max(min(green, 255), 0)
        blue = max(min(blue, 255), 0)

        # INVOKE <id> RGBLoad.SetRGB <red> <green> <blue>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetRGB <red> <green> <blue>
        await self.invoke(vid, "RGBLoad.SetRGB", red, green, blue)

    async def get_rgb(self, vid: int, channel: int) -> int:
        """Get a single RGB color channel of a load from the controller.

        Args:
            vid: The Vantage ID of the RGB load.
            channel: The channel to get the color of.

        Returns:
            The value of the RGB channel, 0-255.
        """
        # INVOKE <id> RGBLoad.GetRGB <channel>
        response = await self.invoke(vid, "RGBLoad.GetRGB", channel)
        _, value = self.parse_get_rgb_response(response)

        return value

    async def set_hsl(
        self,
        vid: int,
        hue: int,
        saturation: Union[float, Decimal],
        lightness: Union[float, Decimal],
    ) -> None:
        """Set the color of an HSL load.

        Args:
            vid: The Vantage ID of the RGB load.
            hue: The hue value of the color, in degrees (0-360).
            saturation: The saturation value of the color, in percent (0-100).
            lightness: The lightness value of the color, in percent (0-100).
        """
        # Clamp levels to 0-360, 0-100
        hue = max(min(hue, 360), 0)
        saturation = max(min(saturation, 100), 0)
        lightness = max(min(lightness, 100), 0)

        # INVOKE <id> RGBLoad.SetHSL <hue> <saturation> <lightness>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetHSL <hue> <saturation> <lightness>
        await self.invoke(vid, "RGBLoad.SetHSL", hue, saturation, lightness)

    async def get_hsl(self, vid: int, attribute: int) -> int:
        """Get a single HSL color attribute of a load from the controller.

        Args:
            vid: The Vantage ID of the RGB load.
            attribute: The attribute to get the value of.

        Returns:
            The value of the HSL attribute, 0-360 for hue, 0-100 for saturation and
            lightness.
        """
        # INVOKE <id> RGBLoad.GetHSL <attribute>
        response = await self.invoke(vid, "RGBLoad.GetHSL", attribute)
        _, value = self.parse_get_hsl_response(response)

        return value

    async def dissolve_rgb(
        self, vid: int, red: float, green: float, blue: float, rate: float
    ) -> None:
        """Transition the color of an RGB load over a number of seconds.

        Args:
            vid: The Vantage ID of the RGB load.
            red: The new red value of the color, (0-255)
            green: The new green value of the color, (0-255)
            blue: The new blue value of the color, (0-255)
            rate: The number of seconds the transition should take.
        """
        # Clamp levels to 0-255, ensure they're integers
        red = int(max(min(red, 255), 0))
        green = int(max(min(green, 255), 0))
        blue = int(max(min(blue, 255), 0))

        # INVOKE <id> RGBLoad.DissolveRGB <red> <green> <blue> <rate>
        # -> R:INVOKE <id> <rcode> RGBLoad.DissolveRGB <red> <green> <blue> <rate>
        await self.invoke(vid, "RGBLoad.DissolveRGB", red, green, blue, rate)

    async def dissolve_hsl(
        self, vid: int, hue: float, saturation: float, lightness: float, rate: float
    ) -> None:
        """Transition the color of an HSL load over a number of seconds.

        Args:
            vid: The Vantage ID of the RGB load.
            hue: The new hue value of the color, in degrees (0-360).
            saturation: The new saturation value of the color, in percent (0-100).
            lightness: The new lightness value of the color, in percent (0-100).
            rate: The number of seconds the transition should take.
        """
        # Clamp levels to 0-360, 0-100, ensure they're integers
        hue = int(max(min(hue, 360), 0))
        saturation = int(max(min(saturation, 100), 0))
        lightness = int(max(min(lightness, 100), 0))

        # INVOKE <id> RGBLoad.DissolveHSL <hue> <saturation> <lightness> <rate>
        # -> R:INVOKE <id> <rcode> RGBLoad.DissolveHSL <hue> <saturation> <lightness> <rate>
        await self.invoke(vid, "RGBLoad.DissolveHSL", hue, saturation, lightness, rate)

    async def set_rgb_component(
        self, vid: int, channel: RGBChannel, value: int
    ) -> None:
        """Set a single RGB(W) color channel of a load.

        Args:
            vid: The Vantage ID of the RGB load.
            channel: The channel to set the color of.
            value: The value to set the channel to, 0-255.
        """
        # Clamp value to 0-255
        value = max(min(value, 255), 0)

        # INVOKE <id> RGBLoad.SetRGBComponent <channel> <value>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetRGBComponent <channel> <value>
        await self.invoke(vid, "RGBLoad.SetRGBComponent", channel, value)

    async def set_hsl_attribute(
        self, vid: int, attribute: HSLAttribute, value: int
    ) -> None:
        """Set a single HSL color attribute of a load.

        Args:
            vid: The Vantage ID of the RGB load.
            attribute: The attribute to set the value of.
            value: The value to set the attribute to, 0-360 for hue, 0-100 for
                saturation and lightness.
        """
        # Clamp value to 0-360, 0-100
        if attribute == self.HSLAttribute.Hue:
            value = max(min(value, 360), 0)
        else:
            value = max(min(value, 100), 0)

        # INVOKE <id> RGBLoad.SetHSLAttribute <attribute> <value>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetHSLAttribute <attribute> <value>
        await self.invoke(vid, "RGBLoad.SetHSLAttribute", attribute, value)

    async def get_color(self, vid: int) -> Tuple[int, ...]:
        """Get the RGB/RGBW color of a load from the controller.

        Args:
            vid: The Vantage ID of the RGB load.

        Returns:
            The value of the RGB/RGBW color as a bytearray.
        """
        # INVOKE <id> RGBLoad.GetColor
        response = await self.invoke(vid, "RGBLoad.GetColor")
        return self.parse_get_color_response(response)

    async def set_rgbw(
        self, vid: int, red: float, green: float, blue: float, white: float
    ) -> None:
        """Set the color of an RGBW load.

        Args:
            vid: The Vantage ID of the RGB load.
            red: The red value of the color, (0-255)
            green: The green value of the color, (0-255)
            blue: The blue value of the color, (0-255)
            white: The white value of the color, (0-255)
        """
        # Clamp levels to 0-255
        red = int(max(min(red, 255), 0))
        green = int(max(min(green, 255), 0))
        blue = int(max(min(blue, 255), 0))
        white = int(max(min(white, 255), 0))

        # INVOKE <id> RGBLoad.SetRGBW <red> <green> <blue> <white>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetRGBW <red> <green> <blue> <white>
        await self.invoke(vid, "RGBLoad.SetRGBW", red, green, blue, white)

    async def get_rgbw(self, vid: int, channel: int) -> int:
        """Get a single RGBW color channel of a load from the controller.

        Args:
            vid: The Vantage ID of the RGB load.
            channel: The channel to get the color of.

        Returns:
            The value of the RGBW channel, 0-255.
        """
        # INVOKE <id> RGBLoad.GetRGB <channel>
        # -> R:INVOKE <id> <value> RGBLoad.GetRGB <channel>
        response = await self.invoke(vid, "RGBLoad.GetRGBW", channel)
        _, value = self.parse_get_rgbw_response(response)

        return value

    async def get_rgb_color(self, vid: int) -> Tuple[int, int, int]:
        """Get the RGB color of a load from the controller.

        Args:
            vid: The Vantage ID of the RGB load.

        Returns:
            The value of the RGB color as a tuple of (red, green, blue).
        """
        color = await self.get_color(vid)
        return cast(Tuple[int, int, int], color[:3])

    async def get_rgbw_color(self, vid: int) -> Tuple[int, int, int, int]:
        """Get the RGBW color of a load from the controller.

        Args:
            vid: The Vantage ID of the RGB load.

        Returns:
            The value of the RGBW color as a tuple of (red, green, blue, white).
        """
        return cast(
            Tuple[int, int, int, int],
            tuple([await self.get_rgbw(vid, chan) for chan in self.RGBChannel]),
        )

    async def get_hsl_color(self, vid: int) -> Tuple[int, int, int]:
        """Get the HSL color of a load from the controller.

        Args:
            vid: The Vantage ID of the RGB load.

        Returns:
            The value of the HSL color as a tuple of (hue, saturation, lightness).
        """
        return cast(
            Tuple[int, int, int],
            tuple([await self.get_hsl(vid, attr) for attr in self.HSLAttribute]),
        )

    @classmethod
    def parse_get_rgb_response(cls, response: InterfaceResponse) -> Tuple[int, int]:
        """Parse a 'RGBLoad.GetRGB' response."""
        # -> R:INVOKE <id> <value> RGBLoad.GetRGB <channel>
        # -> S:STATUS <id> RGBLoad.GetRGB <value> <channel>
        # -> EL: <id> RGBLoad.GetRGB <value> <channel>
        return parse_color_channel_response(response)

    @classmethod
    def parse_get_hsl_response(cls, response: InterfaceResponse) -> Tuple[int, int]:
        """Parse a 'RGBLoad.GetRGB' response."""
        # -> R:INVOKE <id> <value> RGBLoad.GetHSL <attribute>
        # -> S:STATUS <id> RGBLoad.GetHSL <value> <attribute>
        # -> EL: <id> RGBLoad.GetHSL <value> <attribute>
        return parse_color_channel_response(response)

    @classmethod
    def parse_get_rgbw_response(cls, response: InterfaceResponse) -> Tuple[int, int]:
        """Parse a 'RGBLoad.GetRGBW' response."""
        # -> R:INVOKE <id> <value> RGBLoad.GetRGBW <channel>
        # -> S:STATUS <id> RGBLoad.GetRGBW <value> <channel>
        # -> EL: <id> RGBLoad.GetRGBW <value> <channel>
        return parse_color_channel_response(response)

    @classmethod
    def parse_get_color_response(cls, response: InterfaceResponse) -> Tuple[int, ...]:
        """Parse a 'RGBLoad.GetColor' response."""
        # -> R:INVOKE <id> <color> RGBLoad.GetColor
        # -> S:STATUS <id> RGBLoad.GetColor <color>
        # -> EL: <id> RGBLoad.GetColor <color>
        return parse_packed_color_response(response)

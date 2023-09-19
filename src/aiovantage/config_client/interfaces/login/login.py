"""ILogin.Login method definition."""

from dataclasses import dataclass, field
from typing import ClassVar


@dataclass
class Login:
    """ILogin.Login method definition."""

    @dataclass
    class Params:
        """ILogin.Login method parameters."""

        user: str = field(
            metadata={
                "name": "User",
            }
        )

        password: str = field(
            metadata={
                "name": "Password",
            }
        )

    interface: ClassVar[str] = "ILogin"
    call: Params | None = field(default=None)
    return_value: bool | None = field(
        default=None,
        metadata={
            "name": "return",
        },
    )

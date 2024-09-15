"""
This file is part of VexilPy (elemenom/vexilpy).

VexilPy is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

VexilPy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with VexilPy. If not, see <https://www.gnu.org/licenses/>.
"""

from typing import Any

from ..safety.uselessobject import UselessObject
from ..safety.handler import handle

logger_literal: Any = NotImplementedError

@handle
def logger() -> Any:
    if not logger_literal:
        from ..app.blankslateobject import new

        print("ERROR | VexilPy tried to interact with the logger, but access was denied.\n"
              "Logger has been either destroyed, or not yet initialised.\n"
              "Attempting to retrieve log type and contents (marked as 'PSEUDO-LOGGER'):")

        return new("UselessObjectWithPrinter", (UselessObject,),
            __getattribute__ = \
                lambda item:
                    lambda value:
                        print(f"PSEUDO-LOGGER | {item.upper()} | {value}")
        )()

    return logger_literal

def init_logger(logger_: Any) -> None:
    global logger_literal

    logger_literal = logger_
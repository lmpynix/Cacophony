# core.py
# Part of Cacophony, a Python Discord client.
# Released under the terms of the BSD 3-clause license.  Read LICENSE.txt

import sys
import os
import asyncio
from enum import IntEnum

# Define a constant enum thingy.  This is not really a class.
class InterpType(IntEnum):
    DEFAULT = 0
    ONLY_COMMAND = 1
    ONLY_FORMAT = 2
class InterpOrder(IntEnum):
    AS_WRITTEN = 0
    COMMANDS_FIRST = 1
    MESSAGES_FIRST = 2
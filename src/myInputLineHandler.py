from typing import List, Any

import itertools

from src import core


class MyInputLineHandler(object):
    """
    Put me in between your input and output so I can execute things like slash commands.
    
    Constructor arguments:
    enum core.InterpType type = 'DEFAULT' : Sets the mode of the interpreter.
        Enum values are DEFAULT, ONLY_COMMAND, and ONLY_FORMAT.
    [string, string...] default_sigils = ('/') : Default command triggers.  
        If a line begins with any of these characters, it will be parsed as a command.
    """

    def __init__(self, interp_type : core.InterpType, default_sigils : List) -> None:
        self.mode = interp_type
        self.global_sigils = []
        self.global_sigils = default_sigils
        self.command_registry = {}
        self.interp_order = core.InterpOrder.AS_WRITTEN

    def registerSigil(self, sigil : str) -> bool:
        """
        Register a sigil, so it's interpreted as a command trigger.

        Argument: 
        str sigil : Must be single character (len(sigil)==1)
            TypeError is thrown if this is not the case.
        
        Returns:
        bool is_present : If sigil was already registered, returns True.
        """
        # Make sure input sigil is in fact a single character.
        if not (isinstance(sigil, str) and len(sigil) == 1):
            raise TypeError("Argument sigil must be single character")
        # Check to see if the sigil is already in the registry.
        if sigil in self.global_sigils:
            return True
        # Otherwise put the sigil in the registry.
        else:
            self.global_sigils.append(sigil)
            return False

    async def handleInputLine(self, input_line : str) -> None:
        """
        Starts the line handling process.

        Arguments:
            str input_line: The line to be processed by the handler.
        """
        # Make sure our input line is in fact a string and not something else.
        if not isinstance(input_line, str):
            raise TypeError("Input line must be a string.")
        # Split the input at semicolons, allowing for multiple operations.
        input_strings = input_line.split(sep = ';')
        # Strip leading whitespace from each segment.
        input_strings = [no_ws.lstrip() for no_ws in input_strings]
        # Now we need to check and see what we should be doing with these chunks.
        if self.mode is core.InterpType.ONLY_FORMAT:
            self.formatAndSend(input_strings)
            return
            # Do nothing else because we shouldn't.
        else:
            # Make some flags so we can tell which chunks are commands or not.
            is_command_flags = [(line[0] in self.global_sigils) for line in input_strings]
            # Make a list of all of the commands.
            commands = list(itertools.compress(input_strings, is_command_flags))
            for idx, input_chunk in enumerate(input_strings):
                if self.interp_order is core.InterpOrder.AS_WRITTEN:
                    if is_command_flags[idx]:
                        # This is a command, so we will pass it off to the command handler.
                        await self.handleCommand(input_chunk)
                    else:
                        # This is not a command so we will pass it off to the formatter IF we are supposed to.
                        if self.mode is not core.InterpType.ONLY_COMMAND:
                            self.formatAndSend(input_chunk)
                elif self.interp_order is core.InterpOrder.COMMANDS_FIRST:
                    # Run all of the commands sequentially
                    for command in commands:
                        await self.handleCommand(command)
                    if self.mode is not core.InterpType.ONLY_COMMAND:
                        # It seems like there oughta be a better way to do this...
                        for chunk in input_strings:
                            if chunk not in commands:
                                self.formatAndSend(chunk)
                else: # Must be in messages first order
                    if self.mode is not core.InterpType.ONLY_COMMAND:
                        # It seems like there oughta be a better way to do this...
                        for chunk in input_strings:
                            if chunk not in commands:
                                self.formatAndSend(chunk)
                    for command in commands:
                        await self.handleCommand(command)



    async def formatAndSend(self, what_to_format: (str, list)) -> Tuple[int, int]:
        """
        Format and send a message or set of messages.

        :param what_to_format: either a string or a list of strings.
        :return: Results of formatMsg and _sendMsg.
        """
        formatted, format_ret = self.formatMsg(what_to_format)
        sendmsg_ret = await self._sendMsg(formatted)
        return format_ret, sendmsg_ret

    async def handleCommand(self, string_to_execute: str) -> int:
        pass


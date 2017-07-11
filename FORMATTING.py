# +--------------------------------------------------+
# | Logan's Python Formatting Guidelines, Revision 1 |
# +--------------------------------------------------+

#    An indent is four spaces.

# Comments begin with a space.
#	If your comment is > 80 characters, use a tab for level 2.

import sys
# Group your import statements like so:
## Library Imports:
from typing import Optional, Callable, Any

## Project Imports:

# Variable naming:
variable_name = int()
CONSTANT_NAME = 3
list_name = list()
dict_name = dict()
tuple_name = tuple()

# Other types of object and their conventions:
class ClassName(object):
    # Base classes must explicitly inherit from object.
    """
    Classes must have a docstring.

    A short description is the second line of a docstring.
    Leave a line, then type a long description.

    Arguments to constructor:
        str string1 = '' : A description of what that argument does and its
            anticipated type, with the default value if there is one.
        (str) string2 = None : An optional argument can be denoted with parens.
            This means this argument CAN be None.

    Note: We're assuming that the IDE will tell us about methods and variables.
    """
    
    # This is an intentionally shared variable.
    shared_var = int()

    def __init__(self, string1 : str, string2 : Optional) -> None:
        # A constructor is documented in its class's docstring.
        # Note that all function defs need to use typing-module type checking.
        # First argument must always be "self".

        # Initialize variables in __init__, not anywhere else.
        self.value1 = string1
        self.value2 = string2

    def CallableObject(self, AnotherCallable : Callable) -> Any:
        """
        Callable objects must have a docstring.

        This docstring is formatted similarly to the one for a class.

        Arguments:
        Fx AnotherCallable : A function or a method.
        """
        try:
            AnotherCallable.__call__()
        except AttributeError as err:
            print(err, file=sys.stderr)
        finally:
            print("Done!")
from exceptions import BinutilGenError
from re import compile as rx
from re import search, match

class ArgType(object):
    """ This decides and provides the argument's properties
    """

    def __init__(self, regex=None, bitfield_symbol=None, arg_type=None, modifier=None, prefix=""):
        """Matching the regex defines bitfield_symbol and arg_type of the
        OpcodeArg. An argument value none is discarded.

        - bitfield_symbol: The symbol expeced to be seen on the
          bitfield.

        - arg_type: The argument type string. This overwrites the
          previous one.  If arg_type is an int replace it with the
          corresponding group of the matched regex.

        - modifier: This is an arbitrary callable that accepts the
          opcode arg as a single argument. This does things like
          correct case of arguments etc.

        """
        self.regex = regex
        self.bitfield_symbol = bitfield_symbol
        self.arg_type = arg_type
        self.modifier = modifier
        self.immediate = False
        self.prefix = prefix

        if prefix is not None and regex is None:
            self.regex = rx(r"^%s" % prefix)

        if prefix != "" and arg_type is None:
            raise BinutilGenError("Argument has prefix but lacks arg_type.")

        if arg_type is not None and (search(r"[)( !@#$%^&*\t\n]", arg_type) or match("^[0-9]", arg_type)):
            raise BinutilGenError("arg_type should be a valid C variable name.")

    def __call__(self, opcode_arg):
        """Fill in the opcode_arg property. Return true if matched. Do nothing
        if not matched."""

        match = self.regex.match(opcode_arg.syntax_token)

        if not match:
            return None

        if self.bitfield_symbol is not None:
            if type(self.bitfield_symbol) is int:
                bf_sym = match.group(self.bitfield_symbol)
            else:
                bf_sym = self.bitfield_symbol

            opcode_arg.bitfield_symbol = bf_sym

        if self.arg_type is not None:
            opcode_arg.arg_type = self.arg_type
            opcode_arg.typemacro = self.macroname()

        if self.modifier is not None:
            self.modifier(opcode_arg)

        return True

    def macroname(self):
        return "ARG_TYPE_%s" % self.arg_type.upper()

    def macro_check(self):
        return "%s_TYPE" % self.name.upper()

    @property
    def name(self):
        return self.arg_type


def turn_immediate(arg):
    """Inform argument that it is an immediate."""
    arg.immediate = True


def turn_ignored(arg):
    """Inform argument that it is invalid"""
    arg.ignore = True

def capitalize_symbol(arg):
    """Capitalize the bitfield symbol."""
    if arg.bitfield_symbol is None:
        raise ISAError("Command %s, arg %s: Dont try to capitalize a symbol before you have defined it. Please rearrange your bitfield properties." % (arg.command, arg))

    arg.bitfield_symbol = arg.bitfield_symbol.upper()

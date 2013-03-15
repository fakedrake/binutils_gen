import re

from config import BITFIELD_PROPERTIES


class NemaWeaverOpcodeArg(object):
    """This is an interface to get an argument"""

    def __init__(self, syntax_token, bitfield, cmd, argument_properties=BITFIELD_PROPERTIES):
        """To return the information the class needs to know which
        argument it is refering to (syntax_token) and the syntax of the resulting
        bitfield (bstr)"""
        self.command = cmd
        self.syntax_token = syntax_token
        self.bitfield_symbol = None
        self.bitfield = bitfield
        self.immediate = False
        self.ignore = False

        for p in argument_properties:
            p(self)

        if self.ignore:
            return

        if self.bitfield_symbol is None:
            raise ISAError("Could not determine bitfield symbol: %s argument of %s." % (syntax_token, self.command))
        if self.arg_type is None:
            raise ISAError("Could not determine argument type: %s argument of %s." % (syntax_token, self.command))

        if self.bitfield_symbol not in bitfield:
            raise ISAError("Symbol '%c' expected in bitfield '%s' : %s argument of %s." % (self.bitfield_symbol, bitfield, syntax_token, self.command))


    def __nonzero__(self):
        return not self.ignore

    def __str__(self):
        return self.syntax_token

    @property
    def mask_length(self):
        """The length of the mask. Note that it does not check if the mask is
        conscutive. It just counts how many mask bits there are.
        """

        mask_size = self.bitfield.mask(self.bitfield_symbol).ones()
        if mask_size == 0:
            raise ISAError("Could not find argument symbol %c in bitfield '%s'", self.symbol, str(self.bitfield))

        return mask_size

    @property
    def type(self):
        """Return the type of the bitfield as a string.

        """
        # XXX: Maybe try to determine it if arg_type is None. For now
        # this wont happen
        return self.arg_type

    @property
    def shift(self):
        """How much should we shift to get to the correct place."""
        for i, c in enumerate( reversed( str(self.bitfield))):
            if c == self.bitfield_symbol:
                return i

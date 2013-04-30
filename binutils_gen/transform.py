class Transform(object):
    """ This represents an opcode transformation. We dont actually use the
 relaxation mechanism but that is essentially what happens in the binutils.
    """

    def __init__(self, from_opcode, opcodes):
        """From the opcode objects extract the relationship. If there is no
        alias in the from_opcode mark this as invalid.

        """
        self.from_opcode = from_opcode
        self.invalid = from_opcode.transform_opcode() is None

        if self.invalid:
            return

        for o  in  opcodes:
            if o.name == from_opcode.transform_opcode():
                self.to_opcode = o
                break

        if self.to_opcode is None:
            raise IndexError("Transformation opcode %s of %s not found in ISA file." % (from_opcode.name, from_opcode.transform_opcode().name))

        if self.to_opcode.opc_mask != self.from_opcode.opc_mask:
            raise IndexError("Opcode %s and %s do not have the same constant mask." % (from_opcode.name, from_opcode.transform_opcode()))

    def __str__(self):
        """The struct to insert in the c code. We have enough info to make the
        entire thing but fix that later.

        """

        return "{%s, %s, NULL, NULL}," % (self.from_opcode.vname(), self.to_opcode.vname())

def transforms(opcodes):
    """Generate the opcode transform map."""

    for o in opcodes:
        t = Transform(o, opcodes)

        if not t.invalid:
            yield str(t)

from itertools import izip_longest

from argument_types import ArgumentTypes
from arguments import NemaWeaverOpcodeArg
from bitfield import ParametricBitfield
from config import ISAError

class NemaWeaverOpcode(object):
    """Provides all information/formats needed for opcode
    representation compatible with binutils"""
    def __init__(self, row, sanity_check=True):
        self.name = row["opcode"]

        # Validity check
        if row["N"] in ['0', '']:
            self.valid = False
            return
        else:
            self.valid = True

        self.bitfield = ParametricBitfield(row["MAJOR"], length=6)
        self.bitfield.append(row["pattern"], None, True)
        self.bitfield.append(row['MINOR'], length=6)

        self.jump = row["JUMP"]
        self.major = int(row['MAJOR'])

        self.args = [NemaWeaverOpcodeArg(i.strip(), self.bitfield, self.name) for i in row["syntax"].split(',') if i != '']
        self.args = filter(bool, self.args)

        # Sanity check
        syntax_err, bit_err = self.bitfield.mismatches(set([i.bitfield_symbol for i in self.args]))

        for c in bit_err:
            raise ISAError("Unexpected symbol '%c' in bitfield of %s '%s', arguments are %s" % (c, self.name, str(self.bitfield), self.args))

        for c in syntax_err:
            raise ISAError("Unused syntax argument '%s' of command %s" % ([s.name for s in self.args if s.symbol == c][0], self.name))

    def _build5(self, vals, fillvalue=0):
        """Retrurn a OP_BUILD5(args) call with values filled with fillvalue"""
        if len(vals) > 5:
            raise ISAError("Too many arguments provided for opcode %s." % self.name)

        return "OP_BUILD5({0}, {1}, {2}, {3}, {4})".format( *[v for i,v in izip_longest(range(5), vals, fillvalue=0)] )

    def vname(self):
        """Name in a c-variable-friendly mode, aka no '.'s, receded
        with nwop_"""
        return "nwop_"+self.name.replace(".", "_")

    @property
    def shifts(self):
        """The string of the shifts attribute."""
        return self._build5([a.shift for a in self.args])

    @property
    def masks(self):
        """The entirety of the masks attribute."""
        return self._build5([a.mask_length for a in self.args])

    @property
    def types(self):
        """The entirety of the types attributes."""
        return self._build5([ArgumentTypes.macroname(a.type) for a in self.args])

    @property
    def imm_arg(self):
        """The index of the immediate if any."""
        for i,a in enumerate(self.args):
            if a.immediate:
                return str(i)

        return str(-1)

    @property
    def inst_type(self):
        """The instruction type. Anyware_inst should do for now"""
        return "anyware_inst"

    @property
    def opc_mask(self):
        """The mast of the static part of the opcode field"""
        return hex(int(self.bitfield.mask()))


    @property
    def bit_seq(self):
        """The binary bit seq"""
        return hex( int(self.bitfield))

    @property
    def delay_slots(self):
        """How many delay slots do we need after this? This should be removed as it is always 0"""
        return str(0)

    @property
    def offset_type(self):
        """Offset from PC? This is 1 for branches."""
        return self.pc_relative()

    def pc_relative(self):
        """Is the immediate pc-relative
        """
        if "reljmp" in self.jump or "pcrela" in self.jump:
            return "INST_PC_OFFSET"
        else:
            return "INST_NO_OFFSET"

    def __str__(self):
        """The struct representation."""
        inner = ', '.join(['"%s"' % self.name, self.masks, self.shifts, self.types, self.offset_type, self.delay_slots, self.imm_arg, self.bit_seq, self.opc_mask, self.vname(), self.inst_type])
        return "{%s}," % inner

    def __eq__(self, target):
        try:
            return self.bitfield == target.bitfield
        except:
            import ipdb; ipdb.set_trace()


def check_duplicates(opc_list):
    for i,o in enumerate(opc_list):
        for op in opc_list[i+1:]:
            if op == o:
                raise ISAError("Opcodes '%s' and '%s' match" % (op.name,o.name))

            if op.name == o.name:
                raise ISAError("Duplicate opcode name '%s'" % op.name)

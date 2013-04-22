from pyrametros import CFile

class ArgumentTypeManager(object):
    """ Manage and export argument types.
    """

    def __init__(self, arg_types, offset, arg_type_groups):
        self.arg_types = [t for t in arg_types if t.arg_type is not None]
        self.arg_type_groups = arg_type_groups
        self.offset = offset

        if len(arg_types) + offset > 0x1f:
            raise ISAError("You have defined too many types. I found %d different types (they can't be more than %d)." % (len(arg_types), 0x1f-offset))


    def type_constant_macros(self):
        """Insert the values."""

        for i,t in enumerate(self.arg_types):
            yield "#define %s %s" % (t.macroname(), hex(i + self.offset))


    def type_check_macros(self):
        """Insert the macro function."""

        for t in self.arg_types:
            yield "#define %s(t) ((t) == %s)" % (t.macro_check(), t.macroname())


    def type_group_macros(self):
        """Create macros to check the groups."""

        for g in self.arg_type_groups:
            expression  = ["%s(t)" % t.macro_check() for t in g.types(self.arg_types)]
            if not expression:
                expression = [g.hard_predicate]

            yield "#define %s_TYPE(t) (%s)" % (g.name.upper(), " || ".join(expression))

    def argument_group_macros(self):
        """Macros to check the group of an argument."""

        for g in self.arg_type_groups:
            yield "#define %(group_name)s_ARG(arg_i, opcode) (%(group_name)s_TYPE( OP_BREAD5((arg_i), (opcode)->arg_type) ))" % dict(group_name=g.name.upper())


    def _prefixed_types(self):
        """A list of types that are prefixed."""

        return [t for t in self.arg_types if t.prefix is not None]

    def prefix_variables(self):
        """Generate prefix variables."""
        for t in self._prefixed_types():
            yield "static char %s_prefix[] __attribute__ ((unused)) = \"%s\";" % (t.name, t.prefix)

    def prefix_selector_code(self):
        """Generate c code that for unsiged t returns a pointer to the correct
        prefix.

        """

        for t in self._prefixed_types():
            yield "if (%s(t))\n\treturn %s_prefix;" % (t.macro_check(), t.name)

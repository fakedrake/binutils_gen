from config import ISAError


class ArgumentTypes(object):
    """ Manage the argument types/
    """

    def __init__(self, arg_props, offset=1):
        """ Given the properties find the argument types.
	"""

        self.offset = offset
        self.arg_types = set([self.extract_types(p.arg_type) for p in arg_types])

        if len(arg_types) + offset > 0x1f:
            raise ISAError("You have defined too many types. I found %d different types (they can't be more than %d)." % (len(arg_types), 0x1f-offset))

    def extract_types(self, prop):
        """Given a prperty see how many types you cna extract from it. For now
        this just returns the prop but we may need to support OR
        later.

        """

        return prop

    def __str__(self):
        """What is to be outputted to the .h as types."""

        ret = ""
        for i,t in enumerate(self.arg_types):
            ret += "#define %s %d\n" % (ArgumentTypes.macroname(t), hex(i + self.offset))

        return ret

    @staticmethod
    def macroname(arg_type):
        """Return the macro name of the type."""

        return "ARG_TYPE_%s" % arg_type.upper()

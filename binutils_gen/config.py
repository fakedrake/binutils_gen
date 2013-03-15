from argument_properties import ArgProperties, turn_immediate, capitalize_symbol, turn_ignored
from re import compile as rx


class ISAError(Exception):
    def __init__(self, str):
        super(ISAError, self).__init__(str)

# Use add a predicate in this list to set a property to an argument
# based on the regular expression of it's syntax.
BITFIELD_PROPERTIES = [
    # Define the symbol before anything else
    ArgProperties(rx("[vrfh]([tTsSrRdD])"), bitfield_symbol=1),

    # Then define arg_types
    ArgProperties(rx("[Ii]mm\d*$"), bitfield_symbol='i', arg_type="imm", modifier=turn_immediate),
    ArgProperties(rx("r.$"), arg_type="reg"),
    ArgProperties(rx("f.$"), arg_type="reg_float"),
    ArgProperties(rx("v.$"), arg_type="reg_vector"),
    ArgProperties(rx("h.$"), arg_type="reg_half"),

    # Modifiers should have all the information they need
    ArgProperties(rx("[fvh].$"), modifier=capitalize_symbol),
    ArgProperties(rx("flag$"), modifier=turn_ignored)]

DEFAULT_NEMA_ROOT = '.'

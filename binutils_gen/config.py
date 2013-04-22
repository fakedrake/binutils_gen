from re import compile as rx

from argument_types import ArgType, turn_immediate, capitalize_symbol, turn_ignored
from argument_groups import ArgGroup

# Use add a predicate in this list to set a property to an argument
# based on the regular expression of it's syntax.
ARG_TYPES = [
    # Define the symbol before anything else
    ArgType(regex=rx("[vrfh]([tTsSrRdD])"), bitfield_symbol=1),

    # Registers
    ArgType(arg_type="reg", prefix="r"),
    ArgType(arg_type="reg_float", prefix="f"),
    ArgType(arg_type="reg_vector", prefix="v"),
    ArgType(arg_type="reg_half", prefix="h"),

    # Then define arg_types
    ArgType(regex=rx("[Ii]mm\d*$"), bitfield_symbol='i', arg_type="imm", modifier=turn_immediate),
    ArgType(regex=rx("u[Ii]mm\d*$"), bitfield_symbol='i', arg_type="uimm", modifier=turn_immediate),
    ArgType(regex=rx("s[Ii]mm\d*$"), bitfield_symbol='i', arg_type="simm", modifier=turn_immediate),

    ArgType(regex=rx("invalid_argument"), arg_type="inv"), # never matched

    # Modifiers should have all the information they need
    ArgType(regex=rx("[fvh].$"), modifier=capitalize_symbol),
    ArgType(regex=rx("flag$"), modifier=turn_ignored)]

# Argument groups may be used by binutils to check if an argument is
# in a group
ARG_TYPE_GROUPS = [
    ArgGroup("immediate", lambda at: at.modifier == turn_immediate),
    ArgGroup("register", lambda at: at.prefix != ""),
    ArgGroup("invalid", lambda at: at.arg_type == "inv" or at.modifier == turn_ignored),
    ArgGroup("unsigned", lambda at: at.arg_type == "uimm" or at.arg_type == "imm")]

DEFAULT_NEMA_ROOT = '..'

# Tags
OPCODES_TAG = "opcodes"
OPCODE_NAMES_TAG = "opcode names"
TYPE_CONSTANT_TAG = "type constants"
TYPE_CHECKS_TAG = "type checks"
TYPE_GROUPS_TAG = "type groups"
ARGUMENT_GROUPS_TAG = "argument groups"
INVALID_TAG = "invalid opcode"
TYPE_PREFIXES_TAG = "type prefixes"
TYPE_PREFIXES_CHECK_TAG = "type prefixes check"

HARDCODED_TYPES = 1             # Number of hardcoded types. We are hardcoding INVALID

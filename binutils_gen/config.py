from re import compile as rx
import os

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
OPCODE_MAP_TAG = "opcode map"

HARDCODED_TYPES = 1             # Number of hardcoded types. We are hardcoding INVALID

# NemaISA.txt related
OPCODE_TRANSFORM = rx(r"rl:([a-z_]*)")

# Helper functions
def nema_root(rel_fname, root=DEFAULT_NEMA_ROOT):
    """ Nemaweaver root.
    """
    env_root = os.getenv('NEMA_ROOT')

    if env_root is not None:
        root = env_root

    return os.path.abspath(os.path.join(root, rel_fname))

def maybe_env(varname, alt_text='unset'):
    """Return the value of the var in '' or the alt_text."""
    val = os.getenv(varname)
    if val:
        return "'%s'" % val

    return alt_text

# Default paths
DEFAULT_OPC = nema_root("nemaweaver-binutils/opcodes/nemaweaver-opc.h")
DEFAULT_OPCM = nema_root("nemaweaver-binutils/opcodes/nemaweaver-opcm.h")
DEFAULT_ISA = nema_root("NemaSpec/Nema_ISA.txt")
DEFAULT_DIS = nema_root("nemaweaver-binutils/opcodes/nemaweaver-dis.c")
DEFAULT_TRANS = nema_root("nemaweaver-binutils/gas/config/tc-nemaweaver.h")
DEFAULT_GAS_HEADER = nema_root("nemaweaver-binutils/gas/config/tc-nemaweaver.h")
DEFAULT_LD_MAP = nema_root("libNema/nema_symbols.map")

# Script help message descritions
LIBSYMBOL_DESCRIPTION = """ Get a list of symbols and their offsets in memory given the
files. Also inform the GNU assembler to recognize those symbols and
enforce absolute jumps when encountered. Default file paths are
created using environment variable 'NEMA_ROOT' (currently %s), or
parent of the current directory if not set.""" % maybe_env("NEMA_ROOT")

BINUTILS_GEN_DESCRIPTION = """ Generate binutils from a NemaISA ascii table. Default paths are
calculated according to environment variable 'NEMA_ROOT' (currently
%s), or parent of current directory if not set.""" % maybe_env("NEMA_ROOT")

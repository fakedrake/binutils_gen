/* nemaweaver-opc.h -- MicroBlaze Opcodes

   Copyright 2009 Free Software Foundation, Inc.

   This file is part of the GNU opcodes library.

   This library is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3, or (at your option)
   any later version.

   It is distributed in the hope that it will be useful, but WITHOUT
   ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
   or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
   License for more details.

   You should have received a copy of the GNU General Public License
   along with this file; see the file COPYING.  If not, write to the
   Free Software Foundation, 51 Franklin Street - Fifth Floor, Boston,
   MA 02110-1301, USA.  */


#ifndef NEMAWEAVER_OPC
#define NEMAWEAVER_OPC

#include "nemaweaver-opcm.h"

/* New instn type for barrel shift imms. */
#define INST_TYPE_RD_R1_IMM5        13
#define INST_TYPE_RD_RFSL           14
#define INST_TYPE_R1_RFSL           15

/* New insn type for insn cache.  */
#define INST_TYPE_RD_R1_SPECIAL     16

/* New insn type for msrclr, msrset insns.  */
#define INST_TYPE_RD_IMM15          17

/* New insn type for tuqula rd - addik rd, r0, 42.  */
#define INST_TYPE_RD                18

/* New insn type for t*put.  */
#define INST_TYPE_RFSL              19
#define INST_TYPE_NONE              25



/* Instructions where the label address is resolved as a PC offset
   (for branch label).  */
#define INST_PC_OFFSET 1
/* Instructions where the label address is resolved as an absolute
   value (for data mem or abs address).  */
#define INST_NO_OFFSET 0

#define OPCODE_MAST_MM    0xFC0007FF


#define OPCODE_MASK_H     0xFC000000  /* High 6 bits only.  */
#define OPCODE_MASK_H1    0xFFE00000  /* High 11 bits.      */
#define OPCODE_MASK_H2    0xFC1F0000  /* High 6 and bits 20-16.  */
#define OPCODE_MASK_H12   0xFFFF0000  /* High 16.  */
#define OPCODE_MASK_H4    0xFC0007FF  /* High 6 and low 11 bits.  */
#define OPCODE_MASK_H13S  0xFFE0EFF0  /* High 11 and 15:1 bits and last nibble of last byte for spr.  */
#define OPCODE_MASK_H23S  0xFC1FC000  /* High 6, 20-16 and 15:1 bits and last nibble of last byte for spr.  */
#define OPCODE_MASK_H34   0xFC00FFFF  /* High 6 and low 16 bits.  */
#define OPCODE_MASK_H14   0xFFE007FF  /* High 11 and low 11 bits.  */
#define OPCODE_MASK_H24   0xFC1F07FF  /* High 6, bits 20-16 and low 11 bits.  */
#define OPCODE_MASK_H124  0xFFFF07FF  /* High 16, and low 11 bits.  */
#define OPCODE_MASK_H1234 0xFFFFFFFF  /* All 32 bits.  */
#define OPCODE_MASK_H3    0xFC000600  /* High 6 bits and bits 21, 22.  */
#define OPCODE_MASK_H32   0xFC00FC00  /* High 6 bits and bit 16-21.  */
#define OPCODE_MASK_H34B  0xFC0000FF  /* High 6 bits and low 8 bits.  */
#define OPCODE_MASK_H34C  0xFC0007E0  /* High 6 bits and bits 21-26.  */

/* New Mask for msrset, msrclr insns.  */
#define OPCODE_MASK_H23N  0xFC1F8000  /* High 6 and bits 11 - 16.  */

#define DELAY_SLOT    1
#define NO_DELAY_SLOT 0

#define MAX_OPCODES 280

#define ARG_IS(opcode, i, val) (OP_BREAD5((i), (opcode)->arg_type) == (val))

/* Begin generated code: type constants */

/* End generated code: type constants */


/* The maximum registers an opcode can have as args. */
#define ARG_MAX_REGS 5
#define ARG_MAX 5

/* Begin generated code: type checks */

/* End generated code: type checks */

/* Begin generated code: type groups */

/* End generated code: type groups */

/* Begin generated code: argument groups */

/* End generated code: argument groups */

/* Build an int with thes 5 bit values */
#define OP_BUILD5(a0, a1, a2, a3, a4) (((a0)&0x1f)<<0 | ((a1)&0x1f)<<5 | ((a2)&0x1f)<<10 | ((a3)&0x1f)<<15 | ((a4)&0x1f)<<20)
/* Get a field from the above */
#define OP_BREAD5(i, bitfield) (((bitfield)>>((i)*5)) & 0x1f)
/* Get an op's mask */
#define ARG_MASK(i, op)  ((1<<OP_BREAD5((i), (op)->arg_mask))-1)
#define ARG_SHIFT(i, op) (OP_BREAD5((i), (op)->arg_shift))
#define ARG_TYPE(i, op)  (OP_BREAD5((i), (op)->arg_type))
#define ARG_UIMM(op) (ARG_TYPE((op)->imm_arg, (op)) & ARG_TYPE_UIMM)

/* Get immediate position in bytes. Note that imm_size shouls be ceiled */
#define DIV_CEIL(x,n) (((x)%(n)) ? ((x)/(n)+1) : ((x)/(n)))
#define IMM_SIZE_BITS(op) (OP_BREAD5((op)->imm_arg, (op)->arg_mask))
#define IMM_SIZE(op) DIV_CEIL(IMM_SIZE_BITS(op),8)
#define IMM_BIT_POS(op) (ARG_SHIFT((op)->imm_arg, (op)) + IMM_SIZE(op))
#define IMM_POS(op) (IMM_BIT_POS(op) / 8)

struct op_code_struct
{
    char * name;

    //  short inst_type;            /* Registers and immediate values involved.  */
    unsigned long arg_mask;	/* A series of 5bit numbers of the
				 * length of each mask, this also
				 * tells us how many args exist */
    unsigned long arg_shift;	/* A series of 5bit numbers of the shift of each arg */
    unsigned long arg_type;	/* ARG_TYPE_REG or ARG_TYPE_IMM */
    short inst_offset_type;     /* Immediate vals offset from PC? (= 1 for branches).  */
    short delay_slots;          /* Info about delay slots needed after this instr. */
    short imm_arg;	        /* Which argument is the imm, -1 if none (used to be immval_mask) */
    unsigned long bit_sequence; /* All the fixed bits for the op are set and
				   all the variable bits (reg names, imm vals)
				   are set to 0.  */
    unsigned long opcode_mask;  /* Which bits define the opcode.  */
    enum nemaweaver_instr instr;
    enum nemaweaver_instr_type instr_type;
    /* More info about output format here.  */
} opcodes[MAX_OPCODES] =
{
    /* Begin generated code: opcodes */

    /* End generated code: opcodes */
    {"nop", 0, 0, 0, 0, 0, -1, 0, 0, 0, alias_and_warn},
    {"", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
};


// Register aliases
struct spl_regiser
{
    char name[20];
    unsigned value;
} special_registers[] = {
    {"ZERO",0},
    {"AT",1},
    {"2",2},
    {"3",3},
    {"4",4},
    {"5",5},
    {"6",6},
    {"7",7},
    {"8",8},
    {"9",9},
    {"10",10},
    {"11",11},
    {"12",12},
    {"13",13},
    {"14",14},
    {"15",15},
    {"16",16},
    {"17",17},
    {"18",18},
    {"19",19},
    {"20",20},
    {"21",21},
    {"22",22},
    {"23",23},
    {"24",24},
    {"25",25},
    {"26",26},
    {"27",27},
    {"GP",28},
    {"SP",29},
    {"FP",30},
    {"RA",31},
    /// NemaCore Single precision HPU Registers
    {"H0",0},
    {"H1",1},
    {"H2",2},
    {"H3",3},
    {"H4",4},
    {"H5",5},
    {"H6",6},
    {"H7",7},
    {"H8",8},
    {"H9",9},
    {"H10",10},
    {"H11",11},
    {"H12",12},
    {"H13",13},
    {"H14",14},
    {"H15",15},
    {"H16",16},
    {"H17",17},
    {"H18",18},
    {"H19",19},
    {"H20",20},
    {"H21",21},
    {"H22",22},
    {"H23",23},
    {"H24",24},
    {"H25",25},
    {"H26",26},
    {"H27",27},
    {"H28",28},
    {"H29",29},
    {"H30",30},
    {"H31",31},
    {"H32",32},
    {"H33",33},
    {"H34",34},
    {"H35",35},
    {"H36",36},
    {"H37",37},
    {"H38",38},
    {"H39",39},
    {"H40",40},
    {"H41",41},
    {"H42",42},
    {"H43",43},
    {"H44",44},
    {"H45",45},
    {"H46",46},
    {"H47",47},
    {"H48",48},
    {"H49",49},
    {"H50",50},
    {"H51",51},
    {"H52",52},
    {"H53",53},
    {"H54",54},
    {"H55",55},
    {"H56",56},
    {"H57",57},
    {"H58",58},
    {"H59",59},
    {"H60",60},
    {"H61",61},
    {"H62",62},
    {"H63",63},

    /// NemaCore Single precision FPU Registers
    {"F0",0},
    {"F1",1},
    {"F2",2},
    {"F3",3},
    {"F4",4},
    {"F5",5},
    {"F6",6},
    {"F7",7},
    {"F8",8},
    {"F9",9},
    {"F10",10},
    {"F11",11},
    {"F12",12},
    {"F13",13},
    {"F14",14},
    {"F15",15},
    {"F16",16},
    {"F17",17},
    {"F18",18},
    {"F19",19},
    {"F20",20},
    {"F21",21},
    {"F22",22},
    {"F23",23},
    {"F24",24},
    {"F25",25},
    {"F26",26},
    {"F27",27},
    {"F28",28},
    {"F29",29},
    {"F30",30},
    {"F31",31},

    /// NemaCore Vector Registers
    {"F0",0},
    {"F2",2},
    {"F4",4},
    {"F6",6},
    {"F8",8},
    {"F10",10},
    {"F12",12},
    {"F14",14},
    {"F16",16},
    {"F18",18},
    {"F20",20},
    {"F22",22},
    {"F24",24},
    {"F26",26},
    {"F28",28},
    {"F30",30},

    {"", 0}
};


/* Prefix for register names.  */
char register_prefix[]         = "r";
char F_register_prefix[]       = "f";
char V_register_prefix[]       = "vV";
char H_register_prefix[]       = "h";

char special_register_prefix[] = "spr";
char fsl_register_prefix[]     = "rfsl";
char pvr_register_prefix[]     = "rpvr";

/* #defines for valid immediate range.  */
#define MIN_IMM(op)  (0)
#define MAX_IMM(op)  ((1<<(IMM_SIZE_BITS(op)+1)) - 1)

#define MIN_IMM15 ((int) 0x0000)
#define MAX_IMM15 ((int) 0x7fff)

/* Begin generated code: invalid opcode */

/* End generated code: invalid opcode */

extern char* arg_prefix(unsigned rtype);

/* Debuging function */
#define fdd(format, arg...) printf("FD DEBUG: " format "\n", ##arg)


#define SKIP_WORD(s) do{ while ((*s<='z' && *s>='a') || (*s>='A' && *s<='Z')  || (*s>='0' && *s<='9')) \
	    ++ s; }while(0)
#define SKIP_WORD_OR_COMMA(s) do{ while ((*s<='z' && *s>='a') || (*s>='A' && *s<='Z') || (*s>='0' && *s<='9') || *s==',') \
	    if (*(s++) == ',') break; }while(0)

#endif /* NEMAWEAVER_OPC */

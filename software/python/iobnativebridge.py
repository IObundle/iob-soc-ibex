#!/usr/bin/env python3
#
#   Create IOBNATIVEBRIDGEIF in directory specified
#   The IOBNATIVEBRIDGEIF is a peripheral that only contains wires. It bridges the peripheral bus with an external interface.
#   It allows the peripheral bus signals to be accessed externally.
#

import sys
import os
import re

def create_iobnativebridgeif(directory):
    iobnativebridgeif_dir = os.path.join(directory, "IOBNATIVEBRIDGEIF")


    if os.path.isdir(iobnativebridgeif_dir):
        raise Exception("{} already exists! Delete that folder before generating this peripheral.".format(iobnativebridgeif_dir))

    # ~~~~~~~~~~~~ Create IOBNATIVEBRIDGEIF folder ~~~~~~~~~~~~
    os.mkdir(iobnativebridgeif_dir)

    # ~~~~~~~~~~~~ Create harware and software dirs ~~~~~~~~~~~~
    os.mkdir(os.path.join(iobnativebridgeif_dir,"hardware"))
    os.mkdir(os.path.join(iobnativebridgeif_dir,"software"))

    # ~~~~~~~~~~~~ Create config.mk ~~~~~~~~~~~~
    config_mk_str = """
TOP_MODULE=iob_nativebridgeif

#PATHS
LIB_DIR ?=$(REGFILEIF_DIR)/submodules/LIB
IOBNATIVEBRIDGEIF_HW_DIR:=$(IOBNATIVEBRIDGEIF_DIR)/hardware

# VERSION
VERSION ?=V0.1
$(TOP_MODULE)_version.txt:
	echo $(VERSION) > version.txt

#MAKE SW ACCESSIBLE REGISTER
MKREGS:=$(shell find $(LIB_DIR) -name mkregs.py)

#target to create (and update) swreg for nativebridgeif based on regfileif
$(IOBNATIVEBRIDGEIF_DIR)/mkregs.conf: $(REGFILEIF_DIR)/mkregs.conf
	$(IOBNATIVEBRIDGEIF_DIR)/software/python/createIObNativeIfSwreg.py $(REGFILEIF_DIR)

#cpu accessible registers
iob_nativebridgeif_swreg_def.vh iob_nativebridgeif_swreg_gen.vh: $(IOBNATIVEBRIDGEIF_DIR)/mkregs.conf
	$(REGFILEIF_DIR)/software/python/mkregsregfileif.py $< HW $(shell dirname $(MKREGS)) iob_nativebridgeif

    """
    fout = open (os.path.join(iobnativebridgeif_dir,"config.mk"), 'w')
    fout.write(config_mk_str)
    fout.close()

    # ~~~~~~~~~~~~ Create gitignore (for swreg) ~~~~~~~~~~~~
    gitignore_str = """\
hardware/include/iob_nativebridgeif_swreg.vh
    """
    fout = open (os.path.join(iobnativebridgeif_dir,".gitignore"), 'w')
    fout.write(gitignore_str)
    fout.close()

    # ~~~~~~~~~~~~ Create hardware.mk ~~~~~~~~~~~~
    harware_mk_str = """
ifeq ($(filter IOBNATIVEBRIDGEIF, $(HW_MODULES)),)

include $(IOBNATIVEBRIDGEIF_DIR)/config.mk

#add itself to HW_MODULES list
HW_MODULES+=IOBNATIVEBRIDGEIF

IOBNATIVEBRIDGEIF_INC_DIR:=$(IOBNATIVEBRIDGEIF_HW_DIR)/include
IOBNATIVEBRIDGEIF_SRC_DIR:=$(IOBNATIVEBRIDGEIF_HW_DIR)/src

#include files
VHDR+=$(wildcard $(IOBNATIVEBRIDGEIF_INC_DIR)/*.vh)
VHDR+=iob_nativebridgeif_swreg_gen.vh iob_nativebridgeif_swreg_def.vh
VHDR+=$(LIB_DIR)/hardware/include/iob_lib.vh

#hardware include dirs
INCLUDE+=$(incdir). $(incdir)$(IOBNATIVEBRIDGEIF_INC_DIR) $(incdir)$(LIB_DIR)/hardware/include

#sources
VSRC+=$(IOBNATIVEBRIDGEIF_SRC_DIR)/iob_nativebridgeif.v

endif
    """
    fout = open (os.path.join(iobnativebridgeif_dir,"hardware","hardware.mk"), 'w')
    fout.write(harware_mk_str)
    fout.close()

    # ~~~~~~~~~~~~ Create include, iob_nativebridgeif.vh, inst.vh and pio.vh ~~~~~~~~~~~~
    os.mkdir(os.path.join(iobnativebridgeif_dir,"hardware/include"))
    # inst.vh
    fin = open (os.path.join(os.path.dirname(__file__), '../../hardware/include/inst.vh'), 'r')
    instv_content=fin.readlines()
    fin.close()
    for i in range(len(instv_content)):
        instv_content[i] = re.sub('regfileif','nativebridgeif', instv_content[i])
    fout = open (os.path.join(iobnativebridgeif_dir,"hardware/include","inst.vh"), 'w')
    fout.writelines(instv_content)
    fout.close()
    # pio.vh
    fin = open (os.path.join(os.path.dirname(__file__), '../../hardware/include/pio.vh'), 'r')
    pio_content=fin.readlines()
    fin.close()
    for i in range(len(pio_content)):
        if 'input' in pio_content[i]:
            pio_content[i] = re.sub('REGFILEIF','IOBNATIVEBRIDGEIF', 
                             re.sub('regfileif','nativebridgeif', 
                             re.sub('input','output', pio_content[i])))
        else:
            pio_content[i] = re.sub('REGFILEIF','IOBNATIVEBRIDGEIF', 
                             re.sub('regfileif','nativebridgeif', 
                             re.sub('output','input', pio_content[i])))
    fout = open (os.path.join(iobnativebridgeif_dir,"hardware/include","pio.vh"), 'w')
    fout.writelines(pio_content)
    fout.close()
    # createIObNativeIfSwreg.py
    os.mkdir(os.path.join(iobnativebridgeif_dir,"software/python"))
    swreg_python_creator = """\
#!/usr/bin/env python3
#Script created by iobnativebridge.py
# Call this script with REGFILEIF_DIR to create the iob_nativebridge_swreg.vh
import os
import sys
import re

fin = open (os.path.join(sys.argv[1], 'mkregs.conf'), 'r')
swreg_content=fin.readlines()
fin.close()
for i in range(len(swreg_content)):
    swreg_content[i] = re.sub('REGFILEIF','IOBNATIVEBRIDGEIF', swreg_content[i])
fout = open (os.path.join(os.path.dirname(__file__),"../../","mkregs.conf"), 'w')
fout.writelines(swreg_content)
fout.close()
    """
    fout = open (os.path.join(iobnativebridgeif_dir,"software/python","createIObNativeIfSwreg.py"), 'w')
    fout.writelines(swreg_python_creator)
    fout.close()
    os.chmod(os.path.join(iobnativebridgeif_dir,"software/python","createIObNativeIfSwreg.py"), 0o755)

    # ~~~~~~~~~~~~ Create verilog source ~~~~~~~~~~~~
    os.mkdir(os.path.join(iobnativebridgeif_dir,"hardware/src"))
    verilog_source_str = """
`timescale 1ns/1ps
`include "iob_lib.vh"
`include "iob_nativebridgeif_swreg_def.vh"

module iob_nativebridgeif
  # (
     parameter DATA_W = `DATA_W,
     parameter ADDR_W = `iob_nativebridgeif_swreg_ADDR_W
     )
   (

    // CPU interface
`include "iob_s_if.vh"

    // External interface
    `IOB_OUTPUT(valid_ext,   1),
    `IOB_OUTPUT(address_ext, ADDR_W),
    `IOB_OUTPUT(wdata_ext,   DATA_W),
    `IOB_OUTPUT(wstrb_ext,   DATA_W/8),
    `IOB_INPUT(rdata_ext,  DATA_W),
    `IOB_INPUT(ready_ext,  1),


`include "gen_if.vh"
    );

    // Connect interfaces
    assign valid_ext = valid;
    assign address_ext = address;
    assign wdata_ext = wdata;
    assign wstrb_ext = wstrb;
    assign rdata = rdata_ext;
    assign ready = ready_ext;

endmodule
    """
    fout = open (os.path.join(iobnativebridgeif_dir,"hardware/src","iob_nativebridgeif.v"), 'w')
    fout.write(verilog_source_str)
    fout.close()

    # ~~~~~~~~~~~~ Create software.mk ~~~~~~~~~~~~
    software_str = """
include $(IOBNATIVEBRIDGEIF_DIR)/config.mk

IOBNATIVEBRIDGEIF_SW_DIR:=$(IOBNATIVEBRIDGEIF_DIR)/software

#include
INCLUDE+=

#headers
HDR+=iob_nativebridgeif_swreg.h

#sources
SRC+=

iob_nativebridgeif_swreg.h iob_nativebridgeif_inverted_swreg.h: $(IOBNATIVEBRIDGEIF_DIR)/mkregs.conf
	$(REGFILEIF_DIR)/software/python/mkregsregfileif.py $< SW $(shell dirname $(MKREGS)) iob_nativebridgeif
    """
    fout = open (os.path.join(iobnativebridgeif_dir,"software","software.mk"), 'w')
    fout.write(software_str)
    fout.close()

    # ~~~~~~~~~~~~ Create embedded.mk ~~~~~~~~~~~~
    os.mkdir(os.path.join(iobnativebridgeif_dir,"software/embedded"))
    embedded_str = """
ifeq ($(filter IOBNATIVEBRIDGEIF, $(SW_MODULES)),)

SW_MODULES+=IOBNATIVEBRIDGEIF

include $(IOBNATIVEBRIDGEIF_DIR)/software/software.mk

# add embeded sources
SRC+=iob_nativebridgeif_swreg_emb.c

iob_nativebridgeif_swreg_emb.c: iob_nativebridgeif_swreg.h
	

endif
    """
    fout = open (os.path.join(iobnativebridgeif_dir,"software/embedded","embedded.mk"), 'w')
    fout.write(embedded_str)
    fout.close()

    # ~~~~~~~~~~~~ Create pc-emul.mk ~~~~~~~~~~~~
    os.mkdir(os.path.join(iobnativebridgeif_dir,"software/pc-emul"))
    pc_emul_str = """
#nativebridge common parameters
include $(IOBNATIVEBRIDGEIF_DIR)/software/software.mk

#pc sources
SRC+=$(IOBNATIVEBRIDGEIF_SW_DIR)/pc-emul/iob_nativebridgeif_swreg_emul.c
    """
    fout = open (os.path.join(iobnativebridgeif_dir,"software/pc-emul","pc-emul.mk"), 'w')
    fout.write(pc_emul_str)
    fout.close()
    # iob-nativebridgeif.c for pc-emul
    fin = open (os.path.join(os.path.dirname(__file__), '../pc-emul/iob_regfileif_swreg_pc_emul.c'), 'r')
    src_content=fin.readlines()
    fin.close()
    for i in range(len(src_content)):
        src_content[i] = re.sub('regfile','iobnativebridge', 
                         re.sub('REGFILE','IOBNATIVEBRIDGE', src_content[i]))
    fout = open (os.path.join(iobnativebridgeif_dir,"software/pc-emul","iob_nativebridgeif_swreg_emul.c"), 'w')
    fout.writelines(src_content)
    fout.close()

# Main function
if __name__ == "__main__" :
    if len(sys.argv) != 2:
        print("Usage: {} <path>".format(sys.argv[0]))
        print(" <path>: Create IOBNATIVEBRIDGEIF in given path.")
        quit()
    else:
        create_iobnativebridgeif(sys.argv[1])

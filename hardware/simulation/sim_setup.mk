#
# This file segment is included in LIB_DIR/Makefile
#
# SIMULATION HARDWARE
#

# HEADERS

#axi portmap for axi ram instance
AXI_GEN ?=$(LIB_DIR)/scripts/if_gen.py
SRC+=$(BUILD_SIM_DIR)/src/s_axi_portmap.vh
$(BUILD_SIM_DIR)/src/s_axi_portmap.vh:
	$(AXI_GEN) axi_portmap 's_' 's_' 'm_' && mv s_axi_portmap.vh $@


# SOURCES

#axi memory
include $(LIB_DIR)/hardware/axi_ram/hw_setup.mk

SRC+=$(BUILD_SIM_DIR)/src/system_tb.v $(BUILD_SIM_DIR)/src/system_top.v

$(BUILD_SIM_DIR)/src/system_tb.v:

$(BUILD_SIM_DIR)/src/system_top.v:


#
# SCRIPTS
#
SRC+=$(BUILD_SW_PYTHON_DIR)/makehex.py $(BUILD_SW_PYTHON_DIR)/hex_split.py $(BUILD_SW_PYTHON_DIR)/hw_defines.py
$(BUILD_SW_PYTHON_DIR)/%.py: $(LIB_DIR)/scripts/%.py
	mkdir -p `dirname $@`
	cp $< $@

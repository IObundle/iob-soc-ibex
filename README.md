<!--
SPDX-FileCopyrightText: 2025 IObundle

SPDX-License-Identifier: MIT
-->

# IOb-SoC-Ibex:

IOb-SoC-Ibex is a System-on-Chip (SoC) built upon [IOb-SoC](https://github.com/IObundle/iob-soc). It is a modified version of IOb-SoC that uses [Ibex](https://github.com/lowRISC/ibex) as the CPU.

Like [IOb-SoC](https://github.com/IObundle/iob-soc), IOb-Soc-Ibex is described in Python using the [Py2HWSW](https://github.com/IObundle/py2hwsw/blob/main/py2hwsw/lib/default.nix) framework. The SoC is entirely described in a few lines of Python. The Py2HWSW framework describes SoCs, in this case using a main [Ibex](https://github.com/lowRISC/ibex) CPU, adding C software and a list of peripherals. After a setup procedure, Py2HWSW creates a build directory with all the sources and makefiles to build and run various tools on the SoC, such as simulation, synthesis, and FPGA prototyping; the SoC is described in Verilog.

The Py2HWSW framework also has a comprehensive library of prebuilt modules and peripherals, including their bare-metal drivers. IOb-SoC-Ibex uses the iob-uart and iob-timer from this library. The external memory interface uses an AXI4 master bus. It may be used to access an on-chip RAM or a 3rd party memory controller IP (typically a DDR controller).

  
## Dependencies

IOb-SoC-Ibex needs the [Py2HWSW](https://github.com/IObundle/py2hwsw/) framework, which runs on a Nix Shell. First, download and install
[nix-shell](https://nixos.org/download.html#nix-install-linux).

Py2HWSW will self-install when `nix-shell` is run on a directory that contains the [py2hwsw default.nix](https://github.com/IObundle/py2hwsw/blob/main/py2hwsw/lib/default.nix) file. All dependencies will also be installed.

In this directory, [default.nix](https://github.com/IObundle/iob-soc-ibex/blob/main/default.nix) will automatically call the [py2hwsw default.nix](https://github.com/IObundle/py2hwsw/blob/main/py2hwsw/lib/default.nix) file. So, you can just use a Nix command with `nix-shell` in this directory, or run a Makefile target like `make setup`, and everything will be installed.

Alternatively, it is possible, but more complex, to install Py2HWSW and its dependencies manually. The explanation of the manual installation process is beyond the scope of this README.
This is not advised for any IOBundle system, but specially not advised for this specific system, since this repository is setup so that it uses one Nix environment to run [Py2HWSW](https://github.com/IObundle/py2hwsw/), and a different one to generate [Ibex](https://github.com/lowRISC/ibex). For the latter, the Nix Flakes environment, with all the CPU's dependencies, available in [Ibex-Demo-System](https://github.com/lowRISC/ibex-demo-system) is used.

More information about this can be found at [IOb-Ibex](https://github.com/IObundle/iob-ibex) or in the sections bellow.


## Operating Systems

IOb-SoC-Ibex can run on most mainstream Linux distributions. The reference distribution is Ubuntu 24.04.1 LTS.


## SoC Configuration

The SoC configuration is in the `iob_soc.py` file at the repository root. To create your own SoC description, follow the instructions in the Py2HWSW user guide.

In here, since we wanted the SoC to use a specific core, we had to state that in the python file, by using:

```Bash
cpu = "iob_ibex",
```
This will indicate to the framework that it should be looking for a `iob_ibex.py` file.

[IOb-Ibex](https://github.com/IObundle/iob-ibex) is a submodule of this repository and it serves as a wrapper of [Ibex](https://github.com/lowRISC/ibex). There are multiple reasons on why an intermediate wrapper was needed, such as the need for an AXI4 interface and many others. Consult the [IOb-Ibex README](https://github.com/IObundle/iob-ibex/blob/main/README.md) for further details.

If that `cpu = "iob_ibex"` parameter was deleted, the Py2HWSW framework would use the default CPU, [IOb-VexRiscV](https://github.com/IObundle/iob-vexriscv), a wrapper for [VexRiscV](https://github.com/SpinalHDL/VexRiscv).

## Setup the SoC by Creating the Build Directory

At the repository root, there is a [Makefile](https://github.com/IObundle/iob-soc-ibex/blob/main/Makefile) with some ready-to-use commands, assuming you have [nix-shell](https://nixos.org/download.html#nix-install-linux) installed. If you have installed Py2HWSW without nix-shell, edit the make file to remove the `nix-shell --run "(...)"` command wrappers.
To create the build directory, simply type:

```Bash
make setup
```

The build directory is created in the folder ../iob_soc_Vx.y, where Vx.y is the IOb-SoC's current version.

The build directory only has source code files and Makefiles. If you do not want to use the Py2HWSW framework, you may, from now on, only use the build directory, provided you have installed all the tools that makefiles will call outside the nix-shell environment.

## Setup Ibex by Generating and Copying RTL files

To use IOb-Soc-Ibex with the [Ibex](https://github.com/lowRISC/ibex) RTL files, these files need to be copied to the build directory along with the rest of the system's files. Since the [Ibex](https://github.com/lowRISC/ibex) repository relies on a custom fork of [FuseSoc](https://github.com/lowRISC/fusesoc) to generate and manage dependencies and RTL files, we created a wrapper called [IOb-Ibex](https://github.com/IObundle/iob-ibex). This wrapper streamlines the process by interacting with Ibex, generating the necessary files, and copying them into the build directory automatically.


The top [Makefile](https://github.com/IObundle/iob-soc-ibex/blob/main/Makefile) of this repository calls upon the [Makefile of IOb-Ibex](https://github.com/IObundle/iob-ibex/blob/main/Makefile) using the `make ibex-setup` target. More information regarding this interactions should be found there, but, in short, a different Nix environment is used. The necessity of using a separate environment is described in the [README of IOb-Ibex](https://github.com/IObundle/iob-ibex/blob/main/README.md).

If you were to inspect the [Makefile](https://github.com/IObundle/iob-soc-ibex/blob/main/Makefile) currently here, you can see that all targets that use `nix-shell` are split:

    sim-run:
        nix-shell --run "make clean setup"
        make ibex-setup
        nix-shell --run "make -C ../$(CORE)_V$(VERSION)/ sim-run SIMULATOR=$(SIMULATOR)"

First, we use the default [Nix-Shell Environment](https://github.com/IObundle/iob-soc-ibex/blob/main/default.nix) (together with [Py2HWSW](https://github.com/IObundle/py2hwsw/)) to create the Build Directory and generate all the Verilog files of the SoC's system (peripherals, interconnects, testbenches, etc).

Then we comunicate with the [Makefile of IOb-Ibex](https://github.com/IObundle/iob-ibex/blob/main/Makefile), that will use the [Nix Flakes Environment](https://github.com/IObundle/iob-ibex/blob/main/flake.nix) to generate the Ibex's RTL files and dependencies (like primitives), and will then copy everything to the Build Directory.

At last, we return to the default [Nix-Shell Environment](https://github.com/IObundle/iob-soc-ibex/blob/main/default.nix) to run the system inside the Build Directory.

## Important Simulation Notes

Whenever the system is setup, with:
```Bash
make setup
```

The local [sim_build.mk](https://github.com/IObundle/iob-soc-ibex/blob/main/hardware/simulation/sim_build.mk) makefile is included in an external [Makefile](https://github.com/IObundle/py2hwsw/blob/main/py2hwsw/hardware/simulation/Makefile) provided by [Py2HWSW](https://github.com/IObundle/py2hwsw/). In here we could not use the framework like that.

[Ibex](https://github.com/lowRISC/ibex) requires for certain files to be loaded first (such as `*_pkg.sv` files). Since the `include sim_build.mk` statement is only inserted after the sources are loaded, we copied the whole [Makefile](https://github.com/IObundle/iob-soc-ibex/blob/main/hardware/simulation/Makefile) to `hardware/simulation` and defined the ordering of the sources there.

It is also relevant to notice that Ibex is mainly described in System Verilog. Not all simulators supported by default in [Py2HWSW](https://github.com/IObundle/py2hwsw/), accept System Verilog. `xcelium` was the simulator used while developing, which imposed a memory size limit (the system can simulate with bigger memories, they'll just not be visible in `gtkwave`, for example). To limit the memory size, we used the following parameter in `iob_soc.py`:
```Bash
"mem_addr_w": 15,  # the default 18 are not visible in xcelium's VCD files
```

As with the Makefile, [Py2HWSW](https://github.com/IObundle/py2hwsw/) also supplies the system with a testbench, generated upon setup. Some asserions in Ibex were conflicting with the system, so a modified [iob_soc_tb.v](https://github.com/IObundle/iob-soc-ibex/blob/main/hardware/simulation/src/iob_soc_tb.v) is provided with `$assertoff();`. The presence of this file here, will impede [Py2HWSW](https://github.com/IObundle/py2hwsw/) to use the default.


## How to Simulate the System

To simulate IOb-SoC-Ibex's RTL using a Verilog simulator, run:

```Bash
make sim-run [SIMULATOR=icarus!verilator|xcelium|vcs|questa] [USE_INTMEM=0|1] [USE_EXTMEM=0|1] [INIT_MEM=0|1]
```

This target compiles the software and hardware, and simulates in the `../iob_soc_Vx.y/hardware/simulation` directory. The `../iob_soc_Vx.y/hardware/simulation/sim_build.mk` makefile segment allows users to change the simulation settings.
The `INIT_MEM` variable specifies whether the firmware is initially loaded in the memory, skipping the boot process, and the `USE_EXTMEM` variable indicates whether an external memory such as DRAM is used.

To run a simulation test comprising a few configurations and two simulators, type:
```Bash
make sim-test
```

The settings for each simulator are described in the [`../iob_soc_Vx.y/hardware/simulation/<simulator>.mk`](https://github.com/IObundle/py2hwsw/tree/main/py2hwsw/hardware/simulation) file. For example, file `icarus.mk` describes the settings for the Icarus Verilog simulator.

The simulator will timeout after GRAB_TIMEOUT seconds, which is 300 seconds by default. Its value can be specified in the `../iob_soc_Vx.y/hardware/simulation/sim_build.mk` Makefile segment, for example, as
```Bash
GRAB_TIMEOUT ?= 3600
```

## Emulate the system on PC

You can *emulate* IOb-SoC-Ibex's on a PC to develop and debug your embedded software. A model to emulate the UART uses a Python console server that comes with Py2HWSW. The same server is used to communicate with FPGA targets.
If you develop peripherals, you can build embedded software models for PC emulation. To emulate IOb-SoC-Ibex's embedded software on a PC, type:

```Bash
make pc-emul-run
```
The Makefile compiles and runs the software in the `../iob_soc_Vx.y/software/` directory. The Makefile includes the `sw_build.mk` segment supplied initially in the same directory. Please feel free to change this file for your specific project. To run an emulation test comparing the result to the expected result, run
```Bash
make pc-emul-test
```

## Run on FPGA board

The FPGA design tools must be installed locally to build and run IOb-SoC-Ibex on an FPGA board. The FPGA board must also be attached to the local host. Currently, only AMD (Xilinx) and Altera boards are supported.

The board settings are in the  [`../iob_soc_Vx.y/hardware/fpga/<tool>/<board_dir>`](https://github.com/IObundle/py2hwsw/tree/main/py2hwsw/hardware/fpga) directory.
For example, the [`../iob_soc_Vx.y/hardware/fpga/vivado/basys3`](https://github.com/IObundle/py2hwsw/tree/main/py2hwsw/hardware/fpga/vivado/basys3) directory contents describe the board BASYS3, which has an FPGA device that can be programmed by the Xilinx/AMD Vivado design tool.

To build an FPGA design of an IOb-SoC-Ibex system and run it on the board located in the `board_dir` directory, type
```Bash
make fpga-run [BOARD=<board_dir>] [USE_INTMEM=0|1] [USE_EXTMEM=0|1] [INIT_MEM=0|1]
```

To run an FPGA test comparing the result to the expected result, run
```Bash
make fpga-test
```
The FPGA test contents can be edited in IOb-SoC-Ibex's top Makefile. 

To configure the serial port connected to the FPGA board, set the corresponding environment variable for that board.
The environment variables for each board are available in their [`board.mk`](https://github.com/IObundle/py2hwsw/blob/main/py2hwsw/hardware/fpga/vivado/basys3/board.mk) file.

For example, to set the serial port for the BASYS3 board, run
```Bash
export BAS3_SERIAL_PORT=/dev/ttyUSB0
```

## Compile the documentation

To compile documents, the LaTeX software must be installed. Three document types are generated: the Product Brief (pb), the User Guide (ug), and a presentation. To build a given document type DOC, run
```Bash
make doc-build [DOC=pb|ug|presentation]
```

To generate the three documents as a test, run 
```Bash
make doc-test
```


## Total test

To run all simulation, FPGA board, and documentation tests, type:

```Bash
make test-all
```

## Running more Makefile Targets

The examples above are the Makefile targets at IOb-SoC-Ibex's root directory that call the targets in the top Makefile in the build directory. Please explore the available targets in the build directory's top Makefile to add more targets to the root directory Makefile.

## Cleaning the build directory
To clean the build directory, run
```Bash
make clean
```

## Use another Py2HWSW version

By default, when running the `nix-shell` tool, it will build an environment that contains the Py2HWSW version specified in first lines of the [default.nix file](https://github.com/IObundle/iob-soc/blob/main/default.nix#L8).
You can update the `py2hwsw_commit` and `py2hwsw_sha256` lines of that file to use another version of Py2HWSW from the IObundle's github repository.


If you cloned the Py2HWSW repository to a local directory, you can use that directory as a source for the Py2HWSW Nix package.
To use a local directory as a source for Py2HWSW, set the following environment variable with the path to the Py2HWSW root directory:
```Bash
export PY2HWSW_ROOT=/path/to/py2hwsw_root_dir
```


# Acknowledgements

First, we acknowledge all the volunteer contributors for all their valuable pull requests, issues, and discussions. 

The work has been partially performed in the scope of the A-IQ Ready project, which receives funding within Chips Joint Undertaking (Chips JU) - the Public-Private Partnership for research, development, and innovation under Horizon Europe – and National Authorities under grant agreement No. 101096658.

The A-IQ Ready project is supported by the Chips Joint Undertaking (Chips JU) - the Public-Private Partnership for research, development, and innovation under Horizon Europe – and National Authorities under Grant Agreement No. 101096658.

<table>
    <tr>
        <td align="center" width="50%"><img src="assets/A-IQ_Ready_logo_blue_transp.png" alt="AI-Q Ready logo" style="width:50%"></td>
        <td align="center"><img src="assets/Chips-JU_logo.jpeg" alt="Chips JU logo" style="width:50%"></td>
    </tr>
</table>

This project provides the basic infrastructure to other projects funded through the NGI Assure Fund, a fund established by NLnet
with financial support from the European Commission's Next Generation Internet program under the aegis of DG Communications Networks, Content, and Technology.

<table>
    <tr>
        <td align="center" width="50%"><img src="https://nlnet.nl/logo/banner.svg" alt="NLnet foundation logo" style="width:50%"></td>
        <td align="center"><img src="https://nlnet.nl/image/logos/NGIAssure_tag.svg" alt="NGI Assure logo" style="width:50%"></td>
    </tr>
</table>

# cocotb testbench
# Ed Carstens, 5/14/2025

import random
from rns import rns
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, ReadOnly
from cocotb.result import TestFailure, ReturnValue

async def drive_x(dut, n, expvals, latency=30):
    dut.log.info(f"Write {n} random values to RNS input, x..")
    base = [16,9,5,7,11,13,17]
    for i in range(n):
        y = int(random.getrandbits(23))
        #y = int(random.getrandbits(6))
        x = rns(y, base).xmods
        expvals.append(y)
        await RisingEdge(dut.clk)
        dut.x16.value = eval('0b' + x[0].onehot())
        dut.x9.value = eval('0b' + x[1].onehot())
        dut.x5.value = eval('0b' + x[2].onehot())
        dut.x7.value = eval('0b' + x[3].onehot())
        dut.x11.value = eval('0b' + x[4].onehot())
        dut.x13.value = eval('0b' + x[5].onehot())
        dut.x17.value = eval('0b' + x[6].onehot())
        #bits = x8 | (x9 & 0x1FF) << 8 | (x5 & 0x1F) << 17 | \
        # (x7 & 0x7F) << 22 | (x13 & 0x1FFF) << 29 | \
        # (x17 & 0x1FFFF) << 42 | (x11 & 0x7FF) << 59
        #dut.x.value = bits

    await RisingEdge(dut.clk)
    dut.x16.value = 0
    dut.x9.value = 0
    dut.x5.value = 0
    dut.x7.value = 0
    dut.x11.value = 0
    dut.x13.value = 0
    dut.x17.value = 0
    
    for i in range(latency):
        await RisingEdge(dut.clk)

async def monitor_y(dut, n, actvals, latency=30):
    for i in range(latency):
        await RisingEdge(dut.clk)
    for i in range(n):
        await RisingEdge(dut.clk)
        actvals.append(dut.y.value.integer)

@cocotb.test()
async def test_rns2bin(dut):
    """
    Try doing a simple test of rns2bin
    """

    # Setup struct interface
    #rns0 = rns_struct()
    #dut.x.value = rns0

    # Set up clock
    cocotb.start_soon(Clock(dut.clk, 5000).start())

    dut._log.info("Do powerup (reset)..")
    #dut.rst.value = 1
    #dut.x.value = 0
    # clean the pipeline
    #for i in range(4):
    await RisingEdge(dut.clk)
    
    n = 20
    actvals = []
    mon_task = cocotb.start_soon(monitor_y(dut, n, actvals, 20))
    expvals = []
    await drive_x(dut, n, expvals)
    dut._log.info(f"expvals={expvals}")
    dut._log.info(f"actvals={actvals}")
    assert expvals == actvals, "Check all expected values vs actual values"

def test_runner():
    import os
    from cocotb.runner import get_runner
    runner = get_runner(os.getenv("SIM"))
    runner.build(
        verilog_sources=["design.sv"],
        hdl_toplevel="top",
        always=True,
        )
    runner.test(hdl_toplevel="top", test_module="my_testbench,")

if __name__ == "__main__":
    test_runner()

        

# Play with cocotb
# Ed Carstens, 4/28/2025

import random
from rns import rns
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, ReadOnly
from cocotb.result import TestFailure, ReturnValue

#@cocotb.coroutine
async def drive_x(dut, n, expvals):
    """
    This coroutine drives the input, x[17:0]
    """
    dut.log.info(f"Write {n} random values to x[17:0]..")
    base = [8,9,5,7,11,13]
    for i in range(n):
        x = int(random.getrandbits(18))
        dut.x.value = x
        expected_y = [zm.x for zm in rns(x, base).xmods]
        expvals.append(expected_y)
        await RisingEdge(dut.clk)  # sync to posedge clk
    # clear pipeline, let last one finish
    for i in range(4):
        x = 0
        await RisingEdge(dut.clk)

def oh2int(xoh):
    _xoh = int(xoh)
    rv = 0
    while _xoh > 1:
        _xoh = _xoh >> 1
        rv += 1
    return rv

#@cocotb.coroutine
async def monitor_y(dut, n, actvals):
    """
    This coroutine monitors the RNS output, y, storing actual values in actvals
    """
    # wait for pipeline latency
    for i in range(4):
        await RisingEdge(dut.clk)
    # sample output values
    for i in range(n):
        await RisingEdge(dut.clk)
        act8 = oh2int(dut.y.x8.value)
        act9 = oh2int(dut.y.x9.value)
        act5 = oh2int(dut.y.x5.value)
        act7 = oh2int(dut.y.x7.value)
        act11 = oh2int(dut.y.x11.value)
        act13 = oh2int(dut.y.x13.value)
        actvals.append([act8,act9,act5,act7,act11,act13])
    
@cocotb.test()
async def test_bin2rns(dut):
    """
    Try doing a simple test of bin2rns_p
    """
    # Set up clock
    cocotb.start_soon(Clock(dut.clk, 5000).start())

    dut._log.info("Do powerup (reset)..")
    #dut.rst.value = 1
    dut.x.value = 0
    # clean the pipeline
    for i in range(4):
        await RisingEdge(dut.clk)
    
    n = 4
    actvals = []
    mon_task = cocotb.start_soon(monitor_y(dut, n, actvals))
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
        hdl_toplevel="bin2rns_p",
        always=True,
        )
    runner.test(hdl_toplevel="bin2rns_p", test_module="my_testbench,")

if __name__ == "__main__":
    test_runner()

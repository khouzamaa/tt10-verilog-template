# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

# Test case 1: Normal addition
    dut.ui_in.value = 20
    dut.uio_in.value = 30
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 50, f"Expected 50, got {dut.uo_out.value}"

    # Test case 2: Zero addition
    dut.ui_in.value = 0
    dut.uio_in.value = 45
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 45, f"Expected 45, got {dut.uo_out.value}"

    # Test case 3: Maximum values (255 + 255)
    dut.ui_in.value = 255
    dut.uio_in.value = 255
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 254, f"Expected 254, got {dut.uo_out.value}"  # Handling overflow

    # Test case 4: Carry generation
    dut.ui_in.value = 240
    dut.uio_in.value = 16
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0, f"Expected 0 (carry ignored), got {dut.uo_out.value}"

    # Test case 5: Random values
    dut.ui_in.value = 90
    dut.uio_in.value = 195
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 29, f"Expected 29, got {dut.uo_out.value}"

    # Test case 6: Edge case (sum exceeds 8-bit range)
    dut.ui_in.value = 200
    dut.uio_in.value = 100
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 44, f"Expected 44 due to overflow, got {dut.uo_out.value}"

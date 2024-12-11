from test import create_testbench
import os

def half_adder_model(a, b):
    s = a ^ b
    cout = a & b
    return {"s": f"1'b{s}", "cout": f"1'b{cout}"}

def full_adder_model(a, b, cin):
    s = (a ^ b) ^ cin
    cout = (a & b) | ((a ^ b) & cin)
    return {"s": f"1'b{s}", "cout": f"1'b{cout}"}

def basic_tests(tb_dir):
    tb_half_adder = create_testbench(os.path.join(os.path.dirname(tb_dir), "half_adder.v"))
    tb_half_adder.set_golden_model(half_adder_model)
    tb_half_adder.set_inputs(a="1'b0", b="1'b0")
    tb_half_adder.assert_outputs()
    tb_half_adder.set_inputs(a="1'b0", b="1'b1")
    tb_half_adder.assert_outputs()
    tb_half_adder.set_inputs(a="1'b1", b="1'b0")
    tb_half_adder.assert_outputs()
    tb_half_adder.set_inputs(a="1'b1", b="1'b1")
    tb_half_adder.assert_outputs()
    tb_half_adder.output_verilog(os.path.join(tb_dir, "half_adder_tb.v"))

    tb_full_adder = create_testbench(os.path.join(os.path.dirname(tb_dir), "full_adder.v"))
    tb_full_adder.set_golden_model(full_adder_model)
    tb_full_adder.set_inputs(a="1'b0", b="1'b0", cin="1'b0")
    tb_full_adder.assert_outputs()
    tb_full_adder.set_inputs(a="1'b0", b="1'b0", cin="1'b1")
    tb_full_adder.assert_outputs()
    tb_full_adder.set_inputs(a="1'b0", b="1'b1", cin="1'b0")
    tb_full_adder.assert_outputs()
    tb_full_adder.set_inputs(a="1'b0", b="1'b1", cin="1'b1")
    tb_full_adder.assert_outputs()
    tb_full_adder.set_inputs(a="1'b1", b="1'b0", cin="1'b0")
    tb_full_adder.assert_outputs()
    tb_full_adder.set_inputs(a="1'b1", b="1'b0", cin="1'b1")
    tb_full_adder.assert_outputs()
    tb_full_adder.set_inputs(a="1'b1", b="1'b1", cin="1'b0")
    tb_full_adder.assert_outputs()
    tb_full_adder.set_inputs(a="1'b1", b="1'b1", cin="1'b1")
    tb_full_adder.assert_outputs()
    tb_full_adder.output_verilog(os.path.join(tb_dir, "full_adder_tb.v"))

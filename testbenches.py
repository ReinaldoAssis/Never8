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

def reg8bit_model(datain, enable, clk):
    if clk == '1' and enable == '1':
        return {"dataout": datain}
    else:
        return {"dataout": "8'b00000000"} # Default to 0 if not enabled or not clock edge

def basic_tests(tb_dir):

    def path(name):
        return os.path.join(os.path.dirname(tb_dir), name)
    
    def outpath(name):
        return os.path.join(tb_dir, name)
                           
    tb_half_adder = create_testbench(path("half_adder.v"))
    tb_half_adder.set_golden_model(half_adder_model)
    tb_half_adder.set_inputs(a="1'b0", b="1'b0")
    tb_half_adder.assert_outputs()
    tb_half_adder.set_inputs(a="1'b0", b="1'b1")
    tb_half_adder.assert_outputs()
    tb_half_adder.set_inputs(a="1'b1", b="1'b0")
    tb_half_adder.assert_outputs()
    tb_half_adder.set_inputs(a="1'b1", b="1'b1")
    tb_half_adder.assert_outputs()
    tb_half_adder.output_verilog(outpath("half_adder_tb.v"))

    tb_full_adder = create_testbench(path("full_adder.v"))
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

    tb_8bit_adder = create_testbench(path("eight_bit_adder.v"))
    tb_8bit_adder.auto_wait = False
    tb_8bit_adder.set_inputs(a="8'b00000000",b="8'b00000000",cin="1'b0")
    tb_8bit_adder.wait(1)
    tb_8bit_adder.assert_outputs(s="8'b00000000",cout="1'b0")

    tb_8bit_adder.wait(1)

    tb_8bit_adder.set_inputs(a="8'b00000001",b="8'b00000000",cin="1'b1")
    tb_8bit_adder.wait(1)
    tb_8bit_adder.assert_outputs(s="8'b00000010",cout="1'b0")

    tb_8bit_adder.wait(1)

    tb_8bit_adder.set_inputs(a="8'b11111111",b="8'b00000001",cin="1'b0")
    tb_8bit_adder.wait(1)
    tb_8bit_adder.assert_outputs(s="8'b00000000",cout="1'b1")


    tb_8bit_adder.output_verilog(outpath("eight_bit_adder_tb.v"))

    tb_reg8bit = create_testbench(path("reg8bit.v"))
    tb_reg8bit.auto_wait = False
    tb_reg8bit.set_golden_model(reg8bit_model)

    tb_reg8bit.set_inputs(datain="8'b10101010", enable="1'b1", clk="1'b0")
    tb_reg8bit.wait(5)
    tb_reg8bit.drive_signal("clk", "1'b1")
    tb_reg8bit.wait(5)

    tb_reg8bit.assert_outputs(dataout="8'b10101010")

    tb_reg8bit.set_inputs(datain="8'b01010101", enable="1'b1", clk="1'b0")
    tb_reg8bit.wait(5)
    tb_reg8bit.drive_signal("clk", "1'b1")
    tb_reg8bit.wait(5)

    tb_reg8bit.assert_outputs(dataout="8'b01010101")


    tb_reg8bit.test_name("DISABLED BUT CLOCKED")

    tb_reg8bit.set_inputs(datain="8'b00000000", enable="1'b1")
    tb_reg8bit.drive_signal("clk", "1'b1")
    tb_reg8bit.wait(100 )
    tb_reg8bit.drive_signal("clk", "1'b0")
    tb_reg8bit.wait(100 )
    tb_reg8bit.drive_signal("clk", "1'b1")

    tb_reg8bit.set_inputs(datain="8'b00000000", enable="1'b0", clk="1'b0")
    tb_reg8bit.wait(100 )
    tb_reg8bit.drive_signal("clk", "1'b1")
    tb_reg8bit.wait(100)

    tb_reg8bit.assert_outputs(dataout="8'b00000000")

    tb_reg8bit.output_verilog(outpath("reg8bit_tb.v"))

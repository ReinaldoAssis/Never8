`timescale 1ns / 1ps

module alu8bit_tb;

    reg [2:0] opcode;
    reg [4:0] a;
    reg [7:0] b;
    wire  zflag;
    wire  c;
    wire [7:0] data_out;

    alu8bit uut (
        .opcode(opcode),
        .a(a),
        .b(b),
        .zflag(zflag),
        .c(c),
        .data_out(data_out)
    );

    initial begin
        // Test vector 1
        opcode = 3'b000; a = 5'b00001; b = 8'b00000001;

        #100;

        if (data_out !== 8'b00000010 || zflag !== 1'b0 || c !== 1'b0) begin
            $display("Test failed: SOMA failed for opcode=%b, a=%b, b=%b. Expected zflag=%b, c=%b, data_out=%b, got zflag=%b, c=%b, data_out=%b", opcode, a, b, 8'b00000010, 1'b0, 1'b0, zflag, c, data_out);
        end else begin
            $display("Test passed: SOMA passed for opcode=%b, a=%b, b=%b. zflag=%b, c=%b, data_out=%b", opcode, a, b, zflag, c, data_out);
        end

        $finish;
    end

endmodule

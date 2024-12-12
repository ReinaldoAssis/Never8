`timescale 1ns / 1ps

module regbank_tb;

    reg [4:0] sel;
    reg [7:0] data_in;
    reg  clk;
    reg  write_reg;
    wire [7:0] data_out;

    regbank uut (
        .sel(sel),
        .data_in(data_in),
        .clk(clk),
        .write_reg(write_reg),
        .data_out(data_out)
    );

    initial begin
        // Test vector 1
        sel = 5'b00000; data_in = 8'b00000101; clk = 1'b0; write_reg = 1'b1;

        #10;

        clk = 1'b1;

        #10;

        clk = 1'b0;

        #10;

        clk = 1'b1;

        #10;

        if (data_out !== 8'b00000000) begin
            $display("Test failed: ZERO REGISTER failed for sel=%b, data_in=%b, clk=%b, write_reg=%b. Expected data_out=%b, got data_out=%b", sel, data_in, clk, write_reg, 8'b00000000, data_out);
        end else begin
            $display("Test passed: ZERO REGISTER passed for sel=%b, data_in=%b, clk=%b, write_reg=%b. data_out=%b", sel, data_in, clk, write_reg, data_out);
        end

        // Test vector 10
        sel = 5'b00001; data_in = 8'b00000101; clk = 1'b0; write_reg = 1'b1;

        #10;

        clk = 1'b1;

        #10;

        clk = 1'b0;

        #10;

        clk = 1'b1;

        #10;

        if (data_out !== 8'b00000101) begin
            $display("Test failed: WRITE REGISTER failed for sel=%b, data_in=%b, clk=%b, write_reg=%b. Expected data_out=%b, got data_out=%b", sel, data_in, clk, write_reg, 8'b00000101, data_out);
        end else begin
            $display("Test passed: WRITE REGISTER passed for sel=%b, data_in=%b, clk=%b, write_reg=%b. data_out=%b", sel, data_in, clk, write_reg, data_out);
        end

        $finish;
    end

endmodule

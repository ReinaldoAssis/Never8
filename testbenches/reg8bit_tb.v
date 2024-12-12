`timescale 1ns / 1ps

module reg8bit_tb;

    reg  enable;
    reg  clk;
    reg [7:0] datain;
    wire [7:0] dataout;

    reg8bit uut (
        .enable(enable),
        .clk(clk),
        .datain(datain),
        .dataout(dataout)
    );

    initial begin
        // Test vector 1
        datain = 8'b10101010; enable = 1'b1; clk = 1'b0;

        #5;

        clk = 1'b1;

        #5;

        if (dataout !== 8'b10101010) begin
            $display("Test failed: Unnamed Test failed for enable=%b, clk=%b, datain=%b. Expected dataout=%b, got dataout=%b", enable, clk, datain, 8'b10101010, dataout);
        end else begin
            $display("Test passed: Unnamed Test passed for enable=%b, clk=%b, datain=%b. dataout=%b", enable, clk, datain, dataout);
        end

        // Test vector 6
        datain = 8'b01010101; enable = 1'b1; clk = 1'b0;

        #5;

        clk = 1'b1;

        #5;

        if (dataout !== 8'b01010101) begin
            $display("Test failed: Unnamed Test failed for enable=%b, clk=%b, datain=%b. Expected dataout=%b, got dataout=%b", enable, clk, datain, 8'b01010101, dataout);
        end else begin
            $display("Test passed: Unnamed Test passed for enable=%b, clk=%b, datain=%b. dataout=%b", enable, clk, datain, dataout);
        end

        // Test vector 11
        datain = 8'b00000000; enable = 1'b1;

        clk = 1'b1;

        #100;

        clk = 1'b0;

        #100;

        clk = 1'b1;

        // Test vector 17
        datain = 8'b00000000; enable = 1'b0; clk = 1'b0;

        #100;

        clk = 1'b1;

        #100;

        if (dataout !== 8'b00000000) begin
            $display("Test failed: DISABLED BUT CLOCKED failed for enable=%b, clk=%b, datain=%b. Expected dataout=%b, got dataout=%b", enable, clk, datain, 8'b00000000, dataout);
        end else begin
            $display("Test passed: DISABLED BUT CLOCKED passed for enable=%b, clk=%b, datain=%b. dataout=%b", enable, clk, datain, dataout);
        end

        $finish;
    end

endmodule

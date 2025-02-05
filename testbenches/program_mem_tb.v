`timescale 1ns / 1ps

module program_mem_tb;

    reg [7:0] address;
    reg  clk;
    wire [7:0] data_out;

    program_mem uut (
        .address(address),
        .clk(clk),
        .data_out(data_out)
    );

    initial begin
        // Test vector 1
        address = 8'b00000000; clk = 1'b0;

        #10;

        clk = 1'b1;

        #10;

        if (data_out !== 8'b00000001) begin
            $display("Test failed: Unnamed Test failed for address=%b, clk=%b. Expected data_out=%b, got data_out=%b", address, clk, 8'b00000001, data_out);
        end else begin
            $display("Test passed: Unnamed Test passed for address=%b, clk=%b. data_out=%b", address, clk, data_out);
        end

        $finish;
    end

endmodule

`timescale 1ns / 1ps

module maverik_tb;

    reg  clk;
    wire [7:0] reg_out;
    wire [7:0] next_pc;
    wire [7:0] next_pc_jmp;
    wire [7:0] mem_out;

    maverik uut (
        .clk(clk),
        .reg_out(reg_out),
        .next_pc(next_pc),
        .next_pc_jmp(next_pc_jmp),
        .mem_out(mem_out)
    );

    initial begin
        // Test vector 1
        clk = 1'b0;

        #100;

        clk = 1'b1;

        #100;

        clk = 1'b0;

        #100;

        if (reg_out !== 8'b00000001 || next_pc !== 8'b00000010 || next_pc_jmp !== 8'b00000010 || mem_out !== 8'b00000010) begin
            $display("Test failed: ADD failed for clk=%b. Expected reg_out=%b, next_pc=%b, next_pc_jmp=%b, mem_out=%b, got reg_out=%b, next_pc=%b, next_pc_jmp=%b, mem_out=%b", clk, 8'b00000001, 8'b00000010, 8'b00000010, 8'b00000010, reg_out, next_pc, next_pc_jmp, mem_out);
        end else begin
            $display("Test passed: ADD passed for clk=%b. reg_out=%b, next_pc=%b, next_pc_jmp=%b, mem_out=%b", clk, reg_out, next_pc, next_pc_jmp, mem_out);
        end

        $finish;
    end

endmodule

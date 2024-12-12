module alu8bit (
    input [2:0] opcode,
    input [4:0] a,
    input [7:0] b,
    output reg zflag,
    output reg c,
    output reg [7:0] data_out
);
    wire [7:0] sum1;
    wire sum_cout;

    eight_bit_adder adder1(
        .a({3'b000, a}),
        .b(b),
        .cin(1'b0),
        .s(sum1),
        .cout(sum_cout)
    );

    always @(*) begin
        case(opcode)
            3'b000: begin  // Addition
                data_out = sum1;
                c = sum_cout;
                zflag = (data_out == 8'b0);
            end
            default: begin
                data_out = 8'b0;
                c = 1'b0;
                zflag = 1'b1;
            end
        endcase
    end
endmodule
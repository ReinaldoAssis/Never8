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

    wire [7:0] sub1;
    wire [7:0] sub_cout;

    wire [7:0] not_a = {3'b111,~a};

    eight_bit_adder adder1(
        .a({3'b000, a}),
        .b(b),
        .cin(1'b0),
        .s(sum1),
        .cout(sum_cout)
    );

    eight_bit_adder subtract(
        .a(not_a),
        .b(b),
        .cin(1'b1),
        .s(sub1),
        .cout(sub_cout)
    );


    always @(*) begin
        case(opcode[0])
            1'b0: begin  // Addition
                data_out = sum1;
                c = sum_cout;
                zflag = (data_out == 8'b0);
            end
            1'b1: begin  // subtraction
                data_out = sub1;
                c = sub_cout;
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
module eight_bit_adder(
    input [7:0] a,
    input [7:0] b,
    input cin,
    output [7:0] s,
    output cout
);

    wire [7:0] couts;

    full_adder fa1 (
        .a(a[0]),
        .b(b[0]),
        .cin(cin),
        .s(s[0]),
        .cout(couts[0])
    );

    full_adder fa2 (
        .a(a[1]),
        .b(b[1]),
        .cin(couts[0]),
        .s(s[1]),
        .cout(couts[1])
    );

    full_adder fa3 (
        .a(a[2]),
        .b(b[2]),
        .cin(couts[1]),
        .s(s[2]),
        .cout(couts[2])
    );

    full_adder fa4 (
        .a(a[3]),
        .b(b[3]),
        .cin(couts[2]),
        .s(s[3]),
        .cout(couts[3])
    );

    full_adder fa5 (
        .a(a[4]),
        .b(b[4]),
        .cin(couts[3]),
        .s(s[4]),
        .cout(couts[4])
    );

    full_adder fa6 (
        .a(a[5]),
        .b(b[5]),
        .cin(couts[4]),
        .s(s[5]),
        .cout(couts[5])
    );

    full_adder fa7 (
        .a(a[6]),
        .b(b[6]),
        .cin(couts[5]),
        .s(s[6]),
        .cout(couts[6])
    );

    full_adder fa8 (
        .a(a[7]),
        .b(b[7]),
        .cin(couts[6]),
        .s(s[7]),
        .cout(cout)
    );

endmodule

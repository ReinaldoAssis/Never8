module full_adder(
    input a,
    input b,
    input cin,
    output s,
    output cout
);

    wire s1;
    wire cout1;
    wire cout_ha2; //Added to store cout from ha2

    half_adder ha1 (
        .a(a),
        .b(b),
        .s(s1),
        .cout(cout1)
    );

    half_adder ha2 (
        .a(s1),
        .b(cin),
        .s(s),
        .cout(cout_ha2) //Changed to store cout in cout_ha2
    );

    assign cout = cout1 | cout_ha2; //Corrected cout calculation

endmodule

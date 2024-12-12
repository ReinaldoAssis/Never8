`timescale 1ns / 1ps

module eight_bit_adder_tb;

    reg [7:0] a;
    reg [7:0] b;
    reg  cin;
    wire [7:0] s;
    wire  cout;

    eight_bit_adder uut (
        .a(a),
        .b(b),
        .cin(cin),
        .s(s),
        .cout(cout)
    );

    initial begin
        // Test vector 1
        a = 8'b00000000; b = 8'b00000000; cin = 1'b0;

        #1;

        if (s !== 8'b00000000 || cout !== 1'b0) begin
            $display("Test failed: Unnamed Test failed for a=%b, b=%b, cin=%b. Expected s=%b, cout=%b, got s=%b, cout=%b", a, b, cin, 8'b00000000, 1'b0, s, cout);
        end else begin
            $display("Test passed: Unnamed Test passed for a=%b, b=%b, cin=%b. s=%b, cout=%b", a, b, cin, s, cout);
        end

        #1;

        // Test vector 5
        a = 8'b00000001; b = 8'b00000000; cin = 1'b1;

        #1;

        if (s !== 8'b00000010 || cout !== 1'b0) begin
            $display("Test failed: Unnamed Test failed for a=%b, b=%b, cin=%b. Expected s=%b, cout=%b, got s=%b, cout=%b", a, b, cin, 8'b00000010, 1'b0, s, cout);
        end else begin
            $display("Test passed: Unnamed Test passed for a=%b, b=%b, cin=%b. s=%b, cout=%b", a, b, cin, s, cout);
        end

        #1;

        // Test vector 9
        a = 8'b11111111; b = 8'b00000001; cin = 1'b0;

        #1;

        if (s !== 8'b00000000 || cout !== 1'b1) begin
            $display("Test failed: Unnamed Test failed for a=%b, b=%b, cin=%b. Expected s=%b, cout=%b, got s=%b, cout=%b", a, b, cin, 8'b00000000, 1'b1, s, cout);
        end else begin
            $display("Test passed: Unnamed Test passed for a=%b, b=%b, cin=%b. s=%b, cout=%b", a, b, cin, s, cout);
        end

        $finish;
    end

endmodule

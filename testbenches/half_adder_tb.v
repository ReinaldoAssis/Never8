`timescale 1ns / 1ps

module half_adder_tb;

    reg  a;
    reg  b;
    wire  s;
    wire  cout;

    half_adder uut (
        .a(a),
        .b(b),
        .s(s),
        .cout(cout)
    );

    initial begin
        // Test vector 1
        a = 1'b0; b = 1'b0;
        #10;

        if (s !== 1'b0 || cout !== 1'b0) begin
            $display("Test failed: Unnamed Test failed for a=%b, b=%b. Expected s=%b, cout=%b, got s=%b, cout=%b", a, b, 1'b0, 1'b0, s, cout);
        end else begin
            $display("Test passed: Unnamed Test passed for a=%b, b=%b. s=%b, cout=%b", a, b, s, cout);
        end

        // Test vector 3
        a = 1'b0; b = 1'b1;
        #10;

        if (s !== 1'b1 || cout !== 1'b0) begin
            $display("Test failed: Unnamed Test failed for a=%b, b=%b. Expected s=%b, cout=%b, got s=%b, cout=%b", a, b, 1'b1, 1'b0, s, cout);
        end else begin
            $display("Test passed: Unnamed Test passed for a=%b, b=%b. s=%b, cout=%b", a, b, s, cout);
        end

        // Test vector 5
        a = 1'b1; b = 1'b0;
        #10;

        if (s !== 1'b1 || cout !== 1'b0) begin
            $display("Test failed: Unnamed Test failed for a=%b, b=%b. Expected s=%b, cout=%b, got s=%b, cout=%b", a, b, 1'b1, 1'b0, s, cout);
        end else begin
            $display("Test passed: Unnamed Test passed for a=%b, b=%b. s=%b, cout=%b", a, b, s, cout);
        end

        // Test vector 7
        a = 1'b1; b = 1'b1;
        #10;

        if (s !== 1'b0 || cout !== 1'b1) begin
            $display("Test failed: Unnamed Test failed for a=%b, b=%b. Expected s=%b, cout=%b, got s=%b, cout=%b", a, b, 1'b0, 1'b1, s, cout);
        end else begin
            $display("Test passed: Unnamed Test passed for a=%b, b=%b. s=%b, cout=%b", a, b, s, cout);
        end

        $finish;
    end

endmodule

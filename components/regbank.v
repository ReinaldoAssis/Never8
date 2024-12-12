module regbank (
    input [4:0] sel,
    input [7:0] data_in,
    input clk,
    input write_reg,
    output reg [7:0] data_out
);

    // we can have 32 register, but some are reserved
    reg [7:0] register_file [0:31];

    always @(posedge clk) begin

        if (write_reg) begin
            register_file[sel] <= data_in;
        end        

        if (sel == 0)
            data_out <=  8'b00000000;
        else
            data_out <= register_file[sel];

    end

endmodule
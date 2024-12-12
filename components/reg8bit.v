module reg8bit (
    input enable,
    input clk,
    input [7:0] datain,
    output reg [7:0] dataout
);

    always @(posedge clk) begin
        if (enable) begin
            dataout <= datain;
        end
    end

endmodule

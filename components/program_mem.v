module program_mem (
    input [7:0] address,     // 8-bit address line (allows 256 bytes of program memory)
    input clk,               // Clock input
    output reg [7:0] data_out // 8-bit instruction output
);

    // Declare the memory array
    reg [7:0] memory [0:255];

    // Initialize memory contents (you can modify this)
    initial begin
        // Example: Load some initial program instructions
        // You'll replace these with your actual program instructions
        memory[0] = 8'b00000001;  // add 1
        memory[1] = 8'b00000010;  // add 2
        memory[2] = 8'b00000011;  // add 3
        
        // You can also use $readmemh or $readmemb to load from a file
        // $readmemh("program.hex", memory);
    end

    // Synchronous read (registered output for better timing)
    always @(posedge clk) begin
        data_out <= memory[address];
    end

endmodule
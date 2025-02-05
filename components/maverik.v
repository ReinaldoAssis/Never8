module maverik(
    input clk,
    output wire [7:0] reg_out,
    output wire [7:0] next_pc,
    output wire [7:0] next_pc_jmp,
    output wire [7:0] mem_out
);
    reg [7:0] pc;  
    // wire [7:0] mem_out;
    reg [7:0] acc; // accumulator
    wire zflag;
    wire carry;
    // wire cout_unused; // Para capturar cout não utilizado

    // Inicialização inicial
    initial begin
        pc = 8'b00000000;
        acc = 8'b00000000;
    end

    program_mem memory (
        .address(pc),
        .clk(clk),
        .data_out(mem_out)
    );

    alu8bit alu (
        .opcode(mem_out[7:5]),
        .a(mem_out[4:0]),
        .b(acc),
        .zflag(zflag),
        .c(carry),
        .data_out(reg_out)
    );

    eight_bit_adder jmp_pc_adder (
        .a(pc),
        .b({3'b000, mem_out[4:0]}), // zero extend
        .cin(1'b0),
        .cout(), 
        .s(next_pc_jmp)
    );

    eight_bit_adder next_pc_adder (
        .a(pc),
        .b(8'b00000001),
        .cin(1'b0),
        .cout(), 
        .s(next_pc)
    );

    // Lógica de atualização sequencial
    always @(posedge clk) begin
        case (mem_out[7:5])
            3'b011: begin // jump
                pc <= next_pc_jmp;
            end
            default: begin
                pc <= next_pc;
            end
        endcase
    end
endmodule
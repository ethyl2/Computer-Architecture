"""CPU functionality."""
import os
import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
ADD = 0b10100000
RET = 0b00010001
CALL = 0b01010000


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        # sets SP (stack pointer) to the value F4 # maybe move to a helper method
        self.reg[-1] = 0b11110100  # 0xf4
        self.ram = [0] * 256
        self.pc = 0
        # self.ir = 0b00000000 # maybe just have this as local var in run()
        self.fl = 0b00000000
        self.ops = {}
        '''
        self.ops[0b10000010] = LDI
        self.ops[0b01000111] = PRN
        self.ops[0b00000001] = HLT
        self.ops[0b10100010] = MUL
        '''
        self.ops[LDI] = self.handle_LDI
        self.ops[PRN] = self.handle_PRN
        self.ops[HLT] = self.handle_HLT
        self.ops[MUL] = self.handle_MUL
        self.ops[PUSH] = self.handle_PUSH
        self.ops[POP] = self.handle_POP
        self.ops[ADD] = self.handle_ADD
        self.ops[RET] = self.handle_RET
        self.ops[CALL] = self.handle_CALL

    def load(self):
        """Load a program into memory."""
        program = []

        # If a file is specified as the argument, load that file
        if len(sys.argv) > 1:
            file_to_load = sys.argv[1]

            with open(os.path.join(sys.path[0], file_to_load), 'r') as f:
                instructions = f.read()

            separated = instructions.split()

            for item in separated:
                if item[0] == '0' or item[0] == '1':
                    program.append(int(item, 2))

        else:
            # If not argument, use hard-coded program:

            program = [
                # From print8.ls8
                0b10000010,  # LDI R0,8
                0b00000000,
                0b00001000,
                0b01000111,  # PRN R0
                0b00000000,
                0b00000001,  # HLT
            ]
            '''
            # Use the following if you want to print an error message and exit instead:
            print("Error: Filename of program to run is needed")
            sys.exit(1)
            '''

        address = 0

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def ram_read(self, mar):
        # mar <- the address that is being read
        # return mdr <- the data that was read
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        # mdr <- the data to write
        # mar <- the address that is being written to
        self.ram[mar] = mdr
        # no return, I guess?

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            # self.reg[reg_a] += self.reg[reg_b]
            total = self.reg[reg_a] + self.reg[reg_b]
            # To keep register within range 0-255
            self.reg[reg_a] = total & 0xFF
        # elif op == "SUB": etc
        elif op == 'MUL':
            product = self.reg[reg_a] * self.reg[reg_b]
            # To keep register within range 0-255
            self.reg[reg_a] = product & 0xFF
            # self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")
    '''
    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    '''

    def handle_LDI(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
        self.pc += 3

    def handle_PRN(self, operand_a, operand_b):
        print(self.reg[operand_a])
        self.pc += 2

    def handle_MUL(self, operand_a, operand_b):
        self.alu('MUL', operand_a, operand_b)
        self.pc += 3

    def handle_ADD(self, operand_a, operand_b):
        self.alu('ADD', operand_a, operand_b)
        self.pc += 3

    def handle_HLT(self, operand_a, operand_b):
        sys.exit(0)

    def handle_PUSH(self, operand_a, operand_b):
        # given register (mar) <- operand_a
        # Decrement the SP
        self.reg[-1] -= 1
        # Copy the value in the given register to the address pointed to by SP
        # self.ram[self.reg[-1]] = self.reg[operand_a]
        self.ram_write(self.reg[operand_a], self.reg[-1])
        self.pc += 2

    def handle_POP(self, operand_a, operand_b):
        # given register (mar) <- operand_a
        # Copy the value from the address pointed to by SP to the given register.
        # self.reg[operand_a] = self.ram[self.reg[-1]]
        self.reg[operand_a] = self.ram_read(self.reg[-1])
        # Increment SP
        self.reg[-1] += 1
        self.pc += 2

    def handle_RET(self, operand_a, operand_b):
        # Pop the value from the top of the stack and store it in the PC.
        self.pc = self.ram_read(self.reg[-1])

    def handle_CALL(self, operand_a, operand_b):
        # given register <- operand_a
        # Push the address of the instruction directly after CALL onto the stack.
        self.reg[-1] += 1
        # self.ram[self.reg[-1]] = pc + 2
        self.ram_write(self.pc + 2, self.reg[-1])

        # Set the PC to the address stored in the given register.
        self.pc = self.reg[operand_a]

    def run(self):
        """Run the CPU."""
        # running = True

        # while running:
        while True:
            # Read the memory address stored in register PC and store result in IR (Instruction Register)
            ir = self.ram_read(self.pc)
            ir_op = self.ops[ir]
            # Read the bytes at PC+1 and PC+2 in case the instruction needs them
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # self.trace()

            # Perform the actions needed for the instruction
            ir_op(operand_a, operand_b)
            '''
            if ir_op == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif ir_op == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            elif ir_op == MUL:
                self.alu('MUL', operand_a, operand_b)
                self.pc += 3
            elif ir_op == HLT:
                # running = False
                sys.exit(0)
            '''

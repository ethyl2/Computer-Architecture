"""CPU functionality."""
import os
import sys

LDI = 'LDI'
PRN = 'PRN'
HLT = 'HLT'
MUL = 'MUL'


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        # sets SP to F4 # maybe move to a helper method
        self.reg[-1] = 0b11110100
        self.ram = [0] * 256
        self.pc = 0
        # self.ir = 0b00000000 # maybe just have this as local var in run()
        self.fl = 0b00000000
        self.ops = {}  # what is the best way to do this??
        self.ops[0b10000010] = LDI
        self.ops[0b01000111] = PRN
        self.ops[0b00000001] = HLT
        self.ops[0b10100010] = MUL

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

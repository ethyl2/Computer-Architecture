"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0b00000000] * 8
        # sets SP to F4 # maybe move to a helper method
        self.reg[-1] = 0b11110100
        self.ram = [0b00000000] * 256
        self.pc = 0b00000000
        # self.ir = 0b00000000 # maybe just have this as local var in run()
        self.fl = 0b00000000

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

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
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

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

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            # Read the memory address stored in register PC and store result in IR (Instruction Register)
            ir = self.ram[self.pc]

            # Read the bytes at PC+1 and PC+2 in case the instruction needs them
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            self.trace()

            # Perform the actions needed for the instruction
            if ir == 0b10000010:  # LDI
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif ir == 0b01000111:  # PRN
                print(self.reg[operand_a])
                self.pc += 2
            elif ir == 0b00000001:  # HLT
                running = False

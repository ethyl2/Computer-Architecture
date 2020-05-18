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
ST = 0b10000100


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
        self.ops[ST] = self.handle_ST

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

    def alu(self, op, register_a, register_b):
        """ALU operations."""

        if op == "ADD":
            # self.reg[register_a] += self.reg[register_b]
            total = self.reg[register_a] + self.reg[register_b]
            # To keep register within range 0-255
            self.reg[register_a] = total & 0xFF
        # elif op == "SUB": etc
        elif op == 'MUL':
            product = self.reg[register_a] * self.reg[register_b]
            # To keep register within range 0-255
            self.reg[register_a] = product & 0xFF
            # self.reg[register_a] *= self.reg[register_b]
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

    def handle_LDI(self, register, immediate):
        # Set the value of the specified register to be the given value (immediate)
        self.reg[register] = immediate
        self.pc += 3

    def handle_PRN(self, register):
        # Print to the console the decimal integer value that is stored in the given register.
        print(self.reg[register])
        self.pc += 2

    def handle_MUL(self, register_a, register_b):
        # In ALU, multiply the values in two registers together and store the result in register_a.
        self.alu('MUL', register_a, register_b)
        self.pc += 3

    def handle_ADD(self, register_a, register_b):
        # In ALU, add the values in two registers and store the result in register_a.
        self.alu('ADD', register_a, register_b)
        self.pc += 3

    def handle_HLT(self):
        # Halt the CPU (and exit the emulator).
        sys.exit(0)

    def handle_PUSH(self, register):
        # Push the value in the given register on the stack.

        # Decrement the SP (stack pointer)
        self.reg[-1] -= 1

        # Copy the value in the given register to the address pointed to by SP
        # self.ram[self.reg[-1]] = self.reg[register]
        self.ram_write(self.reg[register], self.reg[-1])
        self.pc += 2

    def handle_POP(self, register):
        # Pop the value at the top of the stack into the given register.

        # Copy the value from the address pointed to by SP to the given register.
        # self.reg[register] = self.ram[self.reg[-1]]
        self.reg[register] = self.ram_read(self.reg[-1])

        # Increment SP (stack pointer)
        self.reg[-1] += 1
        self.pc += 2

    def handle_RET(self):
        # Return from subroutine.
        # Pop the value from the top of the stack and store it in the PC.
        self.pc = self.ram_read(self.reg[-1])

    def handle_CALL(self, register):
        # Call a subroutine (function) at the address stored in the register.

        # Push the address of the instruction directly after CALL onto the stack.
        self.reg[-1] += 1
        # self.ram[self.reg[-1]] = pc + 2
        self.ram_write(self.pc + 2, self.reg[-1])

        # Set the PC to the address stored in the given register.
        self.pc = self.reg[register]

    def handle_ST(self, operand_a, operand_b):
        # Store value in register_b in the address stored in register_a.

        # self.ram[self.reg[register_a]] = self.reg[register_b]
        self.ram_write(self, self.reg[register_b], self.reg[register_a])

    def run(self):
        """Run the CPU."""

        while True:
            # Read the memory address stored in register PC and store result in IR (Instruction Register)
            ir = self.ram_read(self.pc)
            ir_op = self.ops[ir]

            # Check to see which operands are needed for the instruction.
            # print('{0:08b}'.format(ir))
            num_operands = int('{0:08b}'.format(ir)[:2], 2)
            # print("Num operands: " + str(num_operands))

            # Read the bytes at PC+1 and PC+2 if the instruction needs them.
            # Perform the actions needed for the instruction.

            if num_operands == 2:
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                ir_op(operand_a, operand_b)
            elif num_operands == 1:
                operand_a = self.ram_read(self.pc + 1)
                ir_op(operand_a)
            else:
                ir_op()

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

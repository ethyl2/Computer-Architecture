"""CPU functionality."""
import os
import sys
import time

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
JMP = 0b01010100
PRA = 0b01001000
IRET = 0b00010011


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        # sets SP (stack pointer) to the value F4 # maybe move to a helper method
        self.reg[-1] = 0b11110100  # 0xf4
        self.ram = [0] * 256
        self.pc = 0
        self.fl = 0b00000000
        self.ops = {}

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
        self.ops[JMP] = self.handle_JMP
        self.ops[PRA] = self.handle_PRA
        self.ops[IRET] = self.handle_IRET

        self.start_time = time.time()

    def load(self):
        """Load a program into memory."""
        program = []

        # If a file is specified as the argument, load that file
        if len(sys.argv) > 1:
            file_to_load = sys.argv[1]
            address = 0

            with open(os.path.join(sys.path[0], file_to_load), 'r') as f:
                for line in f:
                    string_val = line.split("#")[0].strip()
                    if string_val == '':
                        continue
                    bin_val = int(string_val, 2)
                    self.ram[address] = bin_val
                    address += 1

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
        # Accept the address to read and return the value stored there

        # mar <- the address that is being read
        # return mdr <- the data that was read
        if mar < len(self.ram):
            # print("current mar: " + str(mar))
            return self.ram[mar]
        else:
            print("MAR is too high: " + str(mar))
            sys.exit(1)

    def ram_write(self, mdr, mar):
        # Accept a value to write, and the address to write it to

        # mdr <- the data to write
        # mar <- the address that is being written to
        self.ram[mar] = mdr

    def alu(self, op, register_a, register_b):
        """ALU operations."""

        if op == "ADD":
            # self.reg[register_a] += self.reg[register_b]
            total = self.reg[register_a] + self.reg[register_b]
            # To keep register within range 0-255
            self.reg[register_a] = total & 0xFF
        # elif op == "SUB": etc
        elif op == 'MUL':
            # self.reg[register_a] *= self.reg[register_b]
            product = self.reg[register_a] * self.reg[register_b]
            # To keep register within range 0-255
            self.reg[register_a] = product & 0xFF

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
        '''
        # This is a version of trace that works with python2
        print(str(self.pc) + " | " + str(self.ram_read(self.pc)) + " " +
              str(self.ram_read(self.pc+1)) + " " + str(self.ram_read(self.pc+2)))

        registers = []
        for i in range(8):
            registers.append(self.reg[i])
        print(registers)
        '''

    def handle_LDI(self, register, immediate):
        # Set the value of the specified register to be the given value (immediate)
        self.reg[register] = immediate

    def handle_PRN(self, register):
        # Print to the console the decimal integer value that is stored in the given register.
        print(self.reg[register])

    def handle_PRA(self, register):
        # Print to the console the ASCII character corresponding to the value in the given register.
        print(chr(self.reg[register]))

    def handle_MUL(self, register_a, register_b):
        # In ALU, multiply the values in two registers together and store the result in register_a.
        self.alu('MUL', register_a, register_b)

    def handle_ADD(self, register_a, register_b):
        # In ALU, add the values in two registers and store the result in register_a.
        self.alu('ADD', register_a, register_b)

    def handle_HLT(self):
        # Halt the CPU (and exit the emulator).
        sys.exit(0)

    def handle_PUSH(self, register):
        # Push the value in the given register on the stack.

        # Decrement the SP (stack pointer)
        self.reg[-1] -= 1

        # Copy the value in the given register to the address pointed to by SP
        # self.ram[self.reg[-1]] = self.reg[register]
        '''
        print("Value of SP " + str(self.reg[-1]))
        print("Register: " + str(register))
        print("Value of register: " + str(self.reg[register]))
        '''
        self.ram_write(self.reg[register], self.reg[-1])

    def handle_POP(self, register):
        # Pop the value at the top of the stack into the given register.

        # Copy the value from the address pointed to by SP to the given register.
        # self.reg[register] = self.ram[self.reg[-1]]
        self.reg[register] = self.ram_read(self.reg[-1])

        # Increment SP (stack pointer)
        self.reg[-1] += 1

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

    def handle_ST(self, register_a, register_b):
        # Store value in register_b in the address stored in register_a.

        # self.ram[self.reg[register_a]] = self.reg[register_b]
        self.ram_write(self.reg[register_b], self.reg[register_a])

    def handle_JMP(self, register):
        # Jump to the address stored in the given register

        # Set the PC to the address stored in the given register.
        self.pc = self.reg[register]

    def handle_IRET(self):
        # Return from an interupt handler.
        # print("Now in handle_IRET")

        # Pop off R6-R0 from the stack in that order.
        for i in range(6, -1, -1):
            self.handle_POP(i)

        # Pop off the FL register from the stack.
        self.fl = self.ram_read(self.reg[-1])
        # print("self.fl is now " + str(self.fl))
        self.reg[-1] += 1

        # Pop off the return address from the stack and store it in PC
        self.pc = self.ram_read(self.reg[-1])
        self.reg[-1] += 1
        # print("back to address " + str(self.pc))

        # Re-enable interrupts
        self.reg[5] = 1
        self.start_time = time.time()

    def run(self):
        """Run the CPU."""

        while True:
            # self.trace()

            # Check to see if one second has elapsed
            current_time = time.time()
            # print("Time difference: " + str(current_time - self.start_time))
            if current_time - self.start_time > 1:
                # print("Time to fire the timer interrupt")

                # Set bit #0 in IS (AKA R6, self.reg[6], Interrupt Status)
                # Later, to handle multiple interrupts, modify this:
                self.reg[6] = 1

                # Check to see if interrupts are enabled by looking at value of IM (AKA R5, self.reg[5], Interrupt Mask)
                interrupts_enabled = self.reg[5] > 0

                # If interrupts are enabled, bitwise-AND the IM with IS.
                if interrupts_enabled:
                    # print("Interrupts_enabled check passed")
                    masked_interrupts = self.reg[5] & self.reg[6]

                    # Step through each bit of masked_interrupts and see which interrupts are set.
                    for i in range(8):
                        # Right shift interrupts down by i, then mask with 1 to see if that bit was set
                        interrupt_happened = (
                            (masked_interrupts >> i) & 1) == 1

                        if interrupt_happened:
                            # print("Interrupt_happened")
                            # Disable further interrupts
                            self.reg[5] = 0

                            # Clear the bit in the IS register
                            self.reg[6] = 0

                            # Push the PC register on the stack.
                            # print("Putting the PC on the stack: " + str(self.pc))
                            self.reg[-1] -= 1
                            self.ram_write(self.pc, self.reg[-1])

                            # Push the FL register on the stack.
                            self.reg[-1] -= 1
                            self.ram_write(self.fl, self.reg[-1])

                            # Push RO-R6 on the stack
                            for i in range(7):
                                self.handle_PUSH(i)  # self.reg[i]
                            # Look up the address of the appropriate handler from the interrupt vector table.
                            # And set the PC to the handler address
                            # self.pc = self.ram[248] # F8, the first slot of the interrupt vector table
                            self.pc = self.ram_read(248)
                            # print(
                            #     "Time to do the interrupt handling. Self.pc is now " + str(self.pc))
                            break
                        else:
                            print("Interrupt didn't happen?")

                            # else:
                            # print("Interrupts_enabled check failed")

                    # Read the memory address stored in register PC (Program Counter) and store result in IR (Instruction Register)
                    # self.trace()
            ir = self.ram_read(self.pc)

            if ir in self.ops:
                ir_op = self.ops[ir]
            else:
                # Exit if the instruction is not a valid option
                print("Unknown instruction " + str(ir) + " at " + str(self.pc))
                sys.exit(1)

            # Check to see which operands are needed for the instruction.

            # Old way:
            # num_operands = int('{0:08b}'.format(ir)[:2], 2)
            # New way uses bitwise-AND and shifting to get the relevant bits.
            num_operands = (ir & 11000000) >> 6
            # print("Num operands: " + str(num_operands))

            # Check to see if the instruction handler sets the PC directly.
            sets_pc = int('{0:08b}'.format(ir)[3])

            # Read the bytes at PC+1 and PC+2 if the instruction needs them.
            # Perform the actions needed for the instruction.

            if num_operands == 2:
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                ir_op(operand_a, operand_b)
                if not sets_pc:
                    self.pc += 3

            elif num_operands == 1:
                operand_a = self.ram_read(self.pc + 1)
                ir_op(operand_a)
                if not sets_pc:
                    self.pc += 2

            else:
                ir_op()
                if not sets_pc:
                    self.pc += 1

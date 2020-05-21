"""CPU functionality."""
import os
import sys
import time

LDI = 0b10000010
LD = 0b10000011
PRN = 0b01000111
HLT = 0b00000001
PUSH = 0b01000101
POP = 0b01000110
RET = 0b00010001
CALL = 0b01010000
ST = 0b10000100
JMP = 0b01010100
JEQ = 0b01010101
JGE = 0b01011010
JLT = 0b01011000
JLE = 0b01011001
JGT = 0b01010111
JNE = 0b01010110
PRA = 0b01001000
IRET = 0b00010011

ADD = 0b10100000
SUB = 0b10100001
MUL = 0b10100010
DIV = 0b10100011
MOD = 0b10100100

DEC = 0b01100110
INC = 0b01100101

AND = 0b10101000
OR = 0b10101010
XOR = 0b10101011
SHR = 0b10101101
SHL = 0b10101100
NOT = 0b01101001

CMP = 0b10100111


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        # sets SP (stack pointer) to the value F4
        self.sp = -1  # AKA 7
        self.reg[self.sp] = 0b11110100  # 0xf4

        self.ram = [0] * 256
        self.pc = 0
        self.fl = 0b00000000

        self.ops = {}

        self.ops[LDI] = self.handle_LDI
        self.ops[LD] = self.handle_LD
        self.ops[PRN] = self.handle_PRN
        self.ops[HLT] = self.handle_HLT
        self.ops[PUSH] = self.handle_PUSH
        self.ops[POP] = self.handle_POP
        self.ops[RET] = self.handle_RET
        self.ops[CALL] = self.handle_CALL
        self.ops[ST] = self.handle_ST
        self.ops[JMP] = self.handle_JMP
        self.ops[JEQ] = self.handle_JEQ
        self.ops[JGE] = self.handle_JGE
        self.ops[JLT] = self.handle_JLT
        self.ops[JLE] = self.handle_JLE
        self.ops[JGT] = self.handle_JGT
        self.ops[JNE] = self.handle_JNE
        self.ops[PRA] = self.handle_PRA
        self.ops[IRET] = self.handle_IRET

        self.ops[ADD] = self.alu
        self.ops[MUL] = self.alu
        self.ops[SUB] = self.alu
        self.ops[DIV] = self.alu
        self.ops[MOD] = self.alu
        self.ops[DEC] = self.alu
        self.ops[INC] = self.alu
        self.ops[AND] = self.alu
        self.ops[OR] = self.alu
        self.ops[XOR] = self.alu
        self.ops[SHR] = self.alu
        self.ops[SHL] = self.alu
        self.ops[NOT] = self.alu
        self.ops[CMP] = self.alu

        self.alu_ops = {}
        self.alu_ops[0b0010] = 'MUL'
        self.alu_ops[0b0000] = 'ADD'
        self.alu_ops[0b0001] = 'SUB'
        self.alu_ops[0b0011] = 'DIV'
        self.alu_ops[0b0100] = 'MOD'
        self.alu_ops[0b0110] = 'DEC'
        self.alu_ops[0b1000] = 'AND'
        self.alu_ops[0b1010] = 'OR'
        self.alu_ops[0b1011] = 'XOR'
        self.alu_ops[0b1101] = 'SHR'
        self.alu_ops[0b1100] = 'SHL'
        self.alu_ops[0b1001] = 'NOT'
        self.alu_ops[0b0101] = 'INC'
        self.alu_ops[0b0111] = 'CMP'

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

    def alu(self, op, register_a, register_b=None):
        """ALU operations."""

        # op = self.alu_ops[self.ram_read(self.pc) & 0b00001111]

        if op == "ADD":
            # Add the values in two registers and store the result in register_a.
            # self.reg[register_a] += self.reg[register_b]
            total = self.reg[register_a] + self.reg[register_b]
            # To keep register value within range 0-255
            self.reg[register_a] = total & 0xFF

        elif op == 'SUB':
            # Subtract the value in the second register from the first, storing the result in register_a.
            difference = self.reg[register_a] - self.reg[register_b]
            # To keep register value within range 0-255
            self.reg[register_a] = difference & 0xFF

        elif op == 'MUL':
            # Multiply the values in two registers together and store the result in register_a.
            # self.reg[register_a] *= self.reg[register_b]
            product = self.reg[register_a] * self.reg[register_b]
            # To keep register value within range 0-255
            self.reg[register_a] = product & 0xFF

        elif op == 'DIV':
            # Divide the value in the first register by the value in the second, storing the result in register_a.
            if self.reg[register_b] == 0:
                print("Division by 0 is not allowed.")
                sys.exit(1)
            quotient = self.reg[register_a] // self.reg[register_b]
            self.reg[register_a] = quotient & 0xFF

        elif op == 'MOD':
            # Divide the value in the first register by the value in the second, storing the remainder of the result in registerA.
            if self.reg[register_b] == 0:
                print("Division by 0 is not allowed.")
                sys.exit(1)
            remainder = self.reg[register_a] % self.reg[register_b]
            self.reg[register_a] = remainder & 0xFF

        elif op == 'AND':
            # Bitwise-AND the values in register_a and register_b, then store the result in register_a.
            result = self.reg[register_a] & self.reg[register_b]
            # print('{0:08b}'.format(self.reg[register_a]))
            # print('{0:08b}'.format(self.reg[register_b]))
            self.reg[register_a] = result
            # print('{0:08b}'.format(self.reg[register_a]))

        elif op == 'OR':
            # Perform a bitwise-OR between the values in register_a and register_b, storing the result in register_a.
            result = self.reg[register_a] | self.reg[register_b]
            # print('{0:08b}'.format(self.reg[register_a]))
            # print('{0:08b}'.format(self.reg[register_b]))
            self.reg[register_a] = result
            # print('{0:08b}'.format(self.reg[register_a]))

        elif op == 'XOR':
            # Perform a bitwise-XOR between the values in register_a and register_b, storing the result in register_a.
            result = self.reg[register_a] ^ self.reg[register_b]
            # print('{0:08b}'.format(self.reg[register_a]))
            # print('{0:08b}'.format(self.reg[register_b]))
            self.reg[register_a] = result
            # print('{0:08b}'.format(self.reg[register_a]))

        elif op == 'SHR':
            # Shift the value in register_a right by the number of bits specified in register_b, filling the high bits with 0.
            # print('{0:08b}'.format(self.reg[register_a]))
            self.reg[register_a] = self.reg[register_a] >> self.reg[register_b]
            # print('{0:08b}'.format(self.reg[register_a]))

        elif op == 'SHL':
            # Shift the value in register_a left by the number of bits specified in register_b, filling the low bits with 0.
            # print('{0:08b}'.format(self.reg[register_a]))
            result = self.reg[register_a] << self.reg[register_b]
            self.reg[register_a] = result & 0xFF
            # print('{0:08b}'.format(self.reg[register_a]))

        elif op == 'NOT':
            # Perform a bitwise-NOT on the value in a register, storing the result in the register.
            # print('{0:08b}'.format(self.reg[register_a]))
            # One way:
            # self.reg[register_a] = (1 << 8) - 1 - self.reg[register_a]
            # Another way:
            # self.reg[register_a] = ~self.reg[register_a] & ((1 << 8) - 1)
            # print('{0:08b}'.format(self.reg[register_a]))
            # Another way:
            self.reg[register_a] = int(bin(~self.reg[register_a] & 0xff), 2)
            # print('{0:08b}'.format(self.reg[register_a]))

        elif op == 'DEC':
            # Decrement (subtract 1 from) the value in the given register
            self.reg[register_a] -= 1

        elif op == 'INC':
            # Increment (add 1 to) the value in the given register
            self.reg[register_a] += 1

        elif op == 'CMP':
            # FL bits: 00000LGE
            # Compare the values in two registers.
            # If they are equal, set the Equal E flag to 1, otherwise set it to 0.
            if self.reg[register_a] == self.reg[register_b]:
                self.fl = 0b00000001
            # If register_a is less than register_b, set the Less-than L flag to 1, otherwise set it to 0.
            elif self.reg[register_a] < self.reg[register_b]:
                self.fl = 0b00000100
            # If register_a is greater than registerB, set the Greater-than G flag to 1, otherwise set it to 0.
            elif self.reg[register_a] > self.reg[register_b]:
                self.fl = 0b00000010
            print('self.fl:' + '{0:08b}'.format(self.fl))

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

    def handle_LD(self, register_a, register_b):
        # Loads register_a with the value at the memory address stored in register_b.
        memory_address = self.reg[register_b]
        # value = self.ram[memory_address]
        value = self.ram_read(memory_address)
        self.reg[register_a] = value

    def handle_PRN(self, register):
        # Print to the console the decimal integer value that is stored in the given register.
        print(self.reg[register])

    def handle_PRA(self, register):
        # Print to the console the ASCII character corresponding to the value in the given register.
        # end="" should keep from going to a new line
        print(chr(self.reg[register]), end="")

    def handle_HLT(self):
        # Halt the CPU (and exit the emulator).
        sys.exit(0)

    def handle_PUSH(self, register):
        # Push the value in the given register on the stack.

        # Decrement the SP (stack pointer)
        self.reg[self.sp] -= 1

        # Copy the value in the given register to the address pointed to by SP
        # self.ram[self.reg[-1]] = self.reg[register]
        '''
        print("Value of SP " + str(self.reg[-1]))
        print("Register: " + str(register))
        print("Value of register: " + str(self.reg[register]))
        '''
        self.ram_write(self.reg[register], self.reg[self.sp])

    def handle_POP(self, register):
        # Pop the value at the top of the stack into the given register.

        # Copy the value from the address pointed to by SP to the given register.
        # self.reg[register] = self.ram[self.reg[-1]]
        self.reg[register] = self.ram_read(self.reg[self.sp])

        # Increment SP (stack pointer)
        self.reg[self.sp] += 1

    def handle_RET(self):
        # Return from subroutine.
        # Pop the value from the top of the stack and store it in the PC.
        self.pc = self.ram_read(self.reg[self.sp])
        # Increment the SP
        self.reg[self.sp] += 1

    def handle_CALL(self, register):
        # Call a subroutine (function) at the address stored in the register.

        # Push the address of the instruction directly after CALL onto the stack.
        # Increment the SP
        self.reg[self.sp] -= 1
        # self.ram[self.reg[-1]] = pc + 2
        self.ram_write(self.pc + 2, self.reg[self.sp])

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

    def handle_JEQ(self, register):
        # If equal flag is set (true), jump to the address stored in the given register.
        if self.fl & 0b00000001:
            self.pc = self.reg[register]
        else:
            self.pc += 2

    def handle_JLT(self, register):
        # If less-than flag is set (true), jump to the address stored in the given register.
        if self.fl >> 2:
            # print("Less-than flag is true")
            # print("Jump to " + str(self.reg[register]))
            self.pc = self.reg[register]
        else:
            self.pc += 2

    def handle_JLE(self, register):
        # If less-than flag or equal flag is set (true), jump to the address stored in the given register.
        if self.fl >> 2 or self.fl & 0b00000001:
            # print("Less-than or equal flag is true")
            # print("Jump to " + str(self.reg[register]))
            self.pc = self.reg[register]
            '''
            # If you want to break up the 2 conditions, modify the one above and add below
            elif self.fl & 0b00000001:
                # print("Equal flag is true")
                # print("Jump to " + str(self.reg[register]))
                self.pc = self.reg[register]
            '''
        else:
            print("Less-than and equal flags are false")
            self.pc += 2

    def handle_JGT(self, register):
        # If greater-than flag is set (true), jump to the address stored in the given register.
        if self.fl >> 1 == 1:
            # print("Greater-than flag is true")
            # print("Jump to " + str(self.reg[register]))
            self.pc = self.reg[register]
        else:
            self.pc += 2

    def handle_JGE(self, register):
        # If the greater-than or the equal flag is set (true), jump to the address stored in the given register.
        if self.fl >> 1 == 1 or self.fl & 0b00000001:
            # print("Greater-than or equal flag is true")
            # print("Jump to " + str(self.reg[register]))
            self.pc = self.reg[register]
        else:
            self.pc += 2

    def handle_JNE(self, register):
        # If E flag is clear (false, 0), jump to the address stored in the given register.
        if self.fl & 0b00000001:
            # print("Equal flag is true")
            self.pc += 2
        else:
            # print("Equal flag is clear")
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
        self.reg[self.sp] += 1

        # Pop off the return address from the stack and store it in PC
        self.pc = self.ram_read(self.reg[-1])
        self.reg[self.sp] += 1
        # print("back to address " + str(self.pc))

        # Re-enable interrupts # need to modify this to handle mult interrupts
        self.reg[5] = 1
        self.start_time = time.time()

    def run(self):  # , stdscr is 2nd arg for keyboard polling
        """Run the CPU."""
        # stdscr.nodelay(1)

        while True:
            '''
            c = stdscr.getch()

            if c == ord('q'):
                sys.exit(0)
            if c != -1:
                stdscr.clear()
                stdscr.refresh()
                stdscr.move(0, 0)
                print(c)
                print("Time to fire keyboard interrupts")
                # Set second bit in IS (AKA R6, self.reg[6], Interrupt Status)
                initial_is = self.reg[6]
                result = initial_is | 0b00000010
                self.reg[6] = result
            '''
            # Check to see if one second has elapsed
            current_time = time.time()
            # print("Time difference: " + str(current_time - self.start_time))
            if current_time - self.start_time > 1:
                # print("Time to fire the timer interrupt")

                # Set bit #0 in IS (AKA R6, self.reg[6], Interrupt Status)
                initial_is = self.reg[6]
                result = initial_is | 0b00000001
                self.reg[6] = result
                # print("set IS: " + str(self.reg[6]))
                # self.reg[6] = 1

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

                    if interrupt_happened:  # and i == 0:
                        # Timer interrupt
                        # print("Interrupt_happened")
                        # Disable further interrupts
                        self.reg[5] = 0

                        # Clear the bit in the IS register
                        initial_is = self.reg[6]
                        result = initial_is ^ 0b00000001
                        self.reg[6] = result
                        # self.reg[6] = 0

                        # Push the PC register on the stack.
                        # print("Putting the PC on the stack: " + str(self.pc))
                        self.reg[self.sp] -= 1
                        self.ram_write(self.pc, self.reg[self.sp])

                        # Push the FL register on the stack.
                        self.reg[self.sp] -= 1
                        self.ram_write(self.fl, self.reg[self.sp])

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

                    elif interrupt_happened and i == 1:
                        # Keyboard interrupt
                        # print("Interrupt_happened")
                        # Disable further interrupts
                        self.reg[5] = 0

                        # Clear the 2nd bit in the IS register
                        initial_is = self.reg[6]
                        result = initial_is ^ 0b00000010
                        self.reg[6] = result

                        # Push the PC register on the stack.
                        # print("Putting the PC on the stack: " + str(self.pc))
                        self.reg[self.sp] -= 1
                        self.ram_write(self.pc, self.reg[self.sp])

                        # Push the FL register on the stack.
                        self.reg[self.sp] -= 1
                        self.ram_write(self.fl, self.reg[self.sp])

                        # Push RO-R6 on the stack
                        for i in range(7):
                            self.handle_PUSH(i)  # self.reg[i]
                        # Look up the address of the appropriate handler from the interrupt vector table.
                        # And set the PC to the handler address
                        # self.pc = self.ram[249] # F9, the second slot of the interrupt vector table
                        self.pc = self.ram_read(249)
                        # print(
                        #     "Time to do the interrupt handling. Self.pc is now " + str(self.pc))
                        break
                    '''
                    else:
                        # print("Interrupt didn't happen?")
                        not_important = True

                        # else:
                        # print("Interrupts_enabled check failed")
                    '''

            # Read the memory address stored in register PC (Program Counter) and store result in IR (Instruction Register)
            ir = self.ram_read(self.pc)

            if ir in self.ops:
                ir_op = self.ops[ir]
            else:
                # Exit if the instruction is not a valid option
                print("Unknown instruction " +
                      str(ir) + " at " + str(self.pc))
                sys.exit(1)

            # Check to see which operands are needed for the instruction.

            # Use bitwise-AND and shifting to get the relevant bits.
            num_operands = (ir & 0b11000000) >> 6
            # print("Num operands: " + str(num_operands))

            # Check to see if the instruction handler sets the PC directly.
            # Use bitwise-AND and shifting to get the relevant bits.
            sets_pc = (ir & 0b00010000) >> 4

            # Check to see if the instruction is handled by the ALU
            handled_by_ALU = (ir & 0b00100000) >> 5

            if handled_by_ALU:
                op = self.alu_ops[self.ram_read(self.pc) & 0b00001111]

            # Read the bytes at PC+1 and PC+2 if the instruction needs them.
            # Perform the actions needed for the instruction.

            if num_operands == 2:
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                if handled_by_ALU:
                    ir_op(op, operand_a, operand_b)
                else:
                    ir_op(operand_a, operand_b)
                if not sets_pc:
                    self.pc += 3

            elif num_operands == 1:
                operand_a = self.ram_read(self.pc + 1)
                if handled_by_ALU:
                    ir_op(op, operand_a)
                else:
                    ir_op(operand_a)
                if not sets_pc:
                    self.pc += 2

            else:
                ir_op()
                if not sets_pc:
                    self.pc += 1

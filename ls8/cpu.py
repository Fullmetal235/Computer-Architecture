"""CPU functionality."""

import sys
import copy

LDI = 130
PRN = 71
HLT = 1
MUL = 162
PUSH = 69
POP = 70


class CPU:
	"""Main CPU class."""

	def __init__(self):
		"""
		Construct a new CPU.
		"""
		self.ram = [0] * 256
		self.register = [0] * 8
		self.pc = 0

	# accepts address to read, returns value at that index
	def ram_read(self, MAR):
		# return value in ram at index of program step
		return self.ram[MAR]

	# accepts a value (MDR) and an address (MAR) to write it to
	def ram_write(self, MAR, MDR):
		self.ram[MAR] = MDR

	# takes file input
	def load(self):
		"""Load a program into memory."""
		address = 0

		with open(sys.argv[1]) as file:
			for instruction in file:
				cleaned_instruction = instruction.split(" ")[0]
				if cleaned_instruction != "#":
					self.ram[address] = int(cleaned_instruction, 2) # keeping it in binary
					address += 1

	def alu(self, op, reg_a, reg_b):
		"""ALU operations."""

		if op == "ADD":
			self.register[reg_a] += self.register[reg_b]
		elif op == "MUL":
			self.register[reg_a] *= self.register[reg_b]
		else:
			raise Exception("Unsupported ALU operation")

	def trace(self):
		"""
		Handy function to print out the CPU state. You might want to call this
		from run() if you need help debugging.
		"""

		print(f"TRACE: %02X | %02X %02X %02X |" % (
				self.pc,
				#self.fl,
				#self.ie,
				self.ram_read(self.pc),
				self.ram_read(self.pc + 1),
				self.ram_read(self.pc + 2)
			), end='')

		for i in range(8):
			print(" %02X" % self.register[i], end='')

			print()

	def run(self):
		"""Run the CPU."""
		# defining instruction
		# instruction equals current index of program counter "pc"
		# print(instruction)
		halted = False
		# starting address index for stacks according to spec
		SP = -14
		while not halted:
			instruction = self.ram[self.pc]
			operand_a = self.ram_read(self.pc + 1)
			operand_b = self.ram_read(self.pc + 2)

			# print(instruction)
			if instruction == HLT:
				halted = True

			# 3 steps to an LDI
			# Step 1: reading instruction
			elif instruction == LDI:
				# Step 2: location		# Step 3: value
				self.register[operand_a] = operand_b
				self.pc += 3

			elif instruction == PRN:
				value = self.register[operand_a]

				print(f'Print: {value}')
				self.pc += 2

			elif instruction == PUSH:
				# stack pointer points at f4 if stack empty, grows downward (the "top" of the stack is bottom-most value)
				# Step 1: decrement SP
				SP -= 1
				# Step 2: push register at given index to top of stack
				self.ram[SP] = self.register[operand_a]

				self.pc += 2

			elif instruction == POP:
				# stack pointer points at f4 if stack empty, grows downward (the "top" of the stack is bottom-most value)
				# Step 1: copy current value into the register of the given index
				copy = self.ram[SP]
				self.register[operand_a] = copy
				# Step 2: increment SP (towards top of RAM)
				SP += 1
				self.pc += 2

			elif instruction == MUL:
				self.alu("MUL", operand_a, operand_b)
				self.pc += 3
			else:
				print(f'Unknown instructions at index {self.pc}')
				sys.exit(1)
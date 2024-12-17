from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Computer:
    registers: list[int]
    pointer: int = 0

    def run(self, program: list[int]) -> list[int]:
        output = []
        while self.pointer < len(program):
            instruction = program[self.pointer]
            literal = program[self.pointer + 1]
            combo = literal if literal < 4 else self.registers[literal - 4]

            self.pointer += 2

            if instruction == 0:
                self.registers[0] = self.registers[0] >> combo

            elif instruction == 1:
                self.registers[1] = self.registers[1] ^ literal

            elif instruction == 2:
                self.registers[1] = combo & 7

            elif instruction == 3:
                if self.registers[0] != 0:
                    self.pointer = literal

            elif instruction == 4:
                self.registers[1] = self.registers[1] ^ self.registers[2]

            elif instruction == 5:
                output.append(combo & 7)

            elif instruction == 6:
                self.registers[1] = self.registers[0] >> combo

            elif instruction == 7:
                self.registers[2] = self.registers[0] >> combo

        return output


def decompiled(a: int) -> list[int]:
    b = c = 0
    output = []

    # fmt: off
    while a != 0:             # 3, 0
        b = a & 7             # 2, 4
        b = b ^ 2             # 1, 2
        c = a >> b            # 7, 5
        b = b ^ 3             # 1, 3
        b = b ^ c             # 4, 3
        output.append(b & 7)  # 5, 5
        a = a >> 3            # 0, 3
    # fmt: on

    return output


def reverse(target: list[int]) -> int:
    stack = [(0, 0)]
    while stack:
        value, matches = stack.pop()
        if matches == len(target):
            return value

        for i in reversed(range(8)):
            new_value = value * 8 + i
            new_matches = matches + 1
            output = decompiled(new_value)
            if output[-new_matches:] == target[-new_matches:]:
                stack.append((new_value, new_matches))

    message = "No solution found"
    raise AssertionError(message)


def solve() -> None:
    computer = Computer(registers=[64584136, 0, 0])
    program = [2, 4, 1, 2, 7, 5, 1, 3, 4, 3, 5, 5, 0, 3, 3, 0]
    output = computer.run(program)
    part_one = ",".join(map(str, output))
    print(f"Part one: {part_one}")

    part_two = reverse(program)
    print(f"Part two: {part_two}")

""" https://adventofcode.com/2023/day/3
--- Day 3: Gear Ratios ---
You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water
source, but this is as far as he can bring you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone!
The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If
you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers
and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is
a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and
58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all the part numbers in the engine
schematic?


--- Part Two ---
The engineer finds the missing part and installs it in the engine! As the engine springs to life, you jump in the
closest gondola, finally ready to ascend to the water source.

You don't seem to be going very fast, though. Maybe something is still wrong? Fortunately, the gondola has a phone
labeled "help", so you pick it up and the engineer answers.

Before you can explain the situation, she suggests that you look out the window. There stands the engineer, holding a
phone in one hand and waving with the other. You're going so slowly that you haven't even left the station. You
exit the gondola.

The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is
adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out
which gear needs to be replaced.

Consider the same engine schematic again:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear
ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear
because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.

What is the sum of all the gear ratios in your engine schematic?
"""
import re

test_schematic = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""


def _initiate_schematic(schematic: str) -> tuple[str, int]:
    schematic_rows = len(schematic.strip().split("\n"))
    schematic_cols = len(schematic.strip().split("\n")[0])
    if schematic_rows != schematic_cols:
        raise ValueError("Schematic must be square.")

    return schematic.strip().replace("\n", ""), schematic_rows


def _get_symbols(schematic: str, schematic_size: int, matching_pattern: str):
    # get all the symbols and their x,y coordinates
    symbols_x_y = []
    for symbol in [
        (match.group(), match.start())
        for match in re.finditer(pattern=matching_pattern, string=schematic)
    ]:
        symbols_x_y.append(
            (int(symbol[1] % schematic_size), int(symbol[1] / schematic_size))
        )

    return symbols_x_y


def _get_part_numbers(schematic: str, schematic_size: int):
    # get all the part numbers and their x,y coordinates
    pn_x_y = []
    pn_matches = re.finditer(pattern=r"\d+", string=schematic)
    for pn in [(match.group(), match.start()) for match in pn_matches]:
        y = int(pn[1] / schematic_size)
        pn_x_y.append(
            (
                pn[0],
                [(int(pn[1] % schematic_size) + i, y) for i in range(len(str(pn[0])))],
            )
        )

    return pn_x_y


def get_valid_part_numbers(schematic: str) -> list[int]:
    schematic, schematic_size = _initiate_schematic(schematic)
    symbols_x_y = _get_symbols(schematic, schematic_size, r"[^\w\d\s.]")
    pn_x_y = _get_part_numbers(schematic, schematic_size)

    # check which pn's are adjacent to a symbol
    valid_pns = []
    for pn, pn_coords in pn_x_y:
        go_to_next_pn = False
        for coord in pn_coords:
            for symbol in symbols_x_y:
                if abs(coord[0] - symbol[0]) <= 1 and abs(coord[1] - symbol[1]) <= 1:
                    valid_pns.append(int(pn))
                    go_to_next_pn = True
                if go_to_next_pn:
                    break
            if go_to_next_pn:
                break

    return valid_pns


def get_gear_ratios(schematic: str):
    schematic, schematic_size = _initiate_schematic(schematic)
    symbols_x_y = _get_symbols(schematic, schematic_size, r"[*]")
    pn_x_y = _get_part_numbers(schematic, schematic_size)

    # check which part-number's makeup a gear
    valid_pns = {}
    for pn, pn_coords in pn_x_y:
        go_to_next_pn = False
        for coord in pn_coords:
            for i, symbol in enumerate(symbols_x_y):
                if abs(coord[0] - symbol[0]) <= 1 and abs(coord[1] - symbol[1]) <= 1:
                    if i not in valid_pns:
                        valid_pns[i] = [int(pn)]
                    else:
                        valid_pns[i].append(int(pn))

                    go_to_next_pn = True
                if go_to_next_pn:
                    break
            if go_to_next_pn:
                break

    # remove invalid gears
    gear_ratios = []
    for i, gear in valid_pns.items():
        if len(gear) == 2:
            gear_ratios.append(gear[0] * gear[1])

    return gear_ratios


if __name__ == "__main__":
    # part 1
    assert sum(get_valid_part_numbers(test_schematic)) == 4361

    with open("puzzle_input") as puzzle_input:
        part_1_final_answer = sum(get_valid_part_numbers(puzzle_input.read()))

    wrong_answers = [305688]  # 305688 is too low
    assert part_1_final_answer not in wrong_answers

    print(f"Sum of all part numbers: {part_1_final_answer}")

    # part 2
    assert sum(get_gear_ratios(test_schematic)) == 467835

    with open("puzzle_input") as puzzle_input:
        part_2_final_answer = sum(get_gear_ratios(puzzle_input.read()))

    print(f"Sum of all gear ratios: {part_2_final_answer}")

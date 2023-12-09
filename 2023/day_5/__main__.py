from dataclasses import dataclass
from pathlib import Path


@dataclass
class Input:
    seeds: list[int]
    mappings: dict[str, list[tuple[int, int, int]]]

    @classmethod
    def from_raw_input(cls, raw_input: str):
        lines = raw_input.strip().split("\n")
        for line in lines:
            if line == "":
                lines.remove(line)

        seeds = [int(seed) for seed in lines.pop(0).split(":")[1].strip().split(" ")]
        mappings = {}
        current_mapping = "unknown"
        for line in lines:
            if line[0].isalpha():
                current_mapping = line.replace(":", "").replace(" ", "-")
                mappings[current_mapping] = []
            else:
                mappings[current_mapping].append(
                    tuple(int(number) for number in line.split(" "))
                )

        if "unknown" in mappings:
            raise ValueError("Unknown mappings found")

        return cls(
            seeds=seeds,
            mappings=mappings,
        )

    @classmethod
    def from_test_input(cls):
        return cls.from_raw_input(Path("test_input").read_text())

    @classmethod
    def from_puzzle_input(cls):
        return cls.from_raw_input(Path("puzzle_input").read_text())


def get_location_given_seed(seed: int, mappings: dict):
    # Normally it would be good to be explicit, but since the order of the list happens to bne the order of
    # deciphering we can use that to our advantage and just loop through each mapping stage to the end.

    temp_value = seed
    for list_of_mappings in mappings.values():
        for mapping in list_of_mappings:
            if mapping[1] <= temp_value < mapping[1] + mapping[2]:
                temp_value = temp_value + mapping[0] - mapping[1]
                break
    return temp_value


def generate_seeds_given_seed_ranges(seeds: list[int]):
    for i in range(0, len(seeds), 2):
        for j in range(seeds[i], seeds[i] + seeds[i + 1]):
            yield j


if __name__ == "__main__":
    # Part 1
    test_input = Input.from_test_input()
    assert (
        min(
            [
                get_location_given_seed(seed, test_input.mappings)
                for seed in test_input.seeds
            ]
        )
        == 35
    )

    puzzle_input = Input.from_puzzle_input()

    part_1_min_seed_location = min(
        [
            get_location_given_seed(seed, puzzle_input.mappings)
            for seed in puzzle_input.seeds
        ]
    )
    print(f"Part 1: seed location is {part_1_min_seed_location}")

    # Part 2
    part_2_min_seed_location = None
    for seed in generate_seeds_given_seed_ranges(puzzle_input.seeds):
        if part_2_min_seed_location is None:
            part_2_min_seed_location = get_location_given_seed(
                seed, puzzle_input.mappings
            )
        elif (
            new_location := get_location_given_seed(seed, puzzle_input.mappings)
        ) < part_2_min_seed_location:
            part_2_min_seed_location = new_location

    print(f"Part 2: seed location is {part_2_min_seed_location}")

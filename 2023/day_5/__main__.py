test_input = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""


def get_inputs(raw_input: str):
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

    return seeds, mappings


def get_seed_location(seed: int, mappings: dict):
    # Normally it would be good to be explicit, but since the order of the list happens to bne the order of
    # deciphering we can use that to our advantage and just loop through each mapping stage to the end.

    temp_value = seed
    for mapped_set in mappings.values():
        for mapping in mapped_set:
            if mapping[1] <= temp_value < mapping[1] + mapping[2]:
                temp_value = temp_value + mapping[0] - mapping[1]
                break
    return temp_value


if __name__ == "__main__":
    # Part 1
    test_seeds, test_mappings = get_inputs(test_input)

    assert get_seed_location(79, test_mappings) == 82
    assert get_seed_location(14, test_mappings) == 43
    assert get_seed_location(55, test_mappings) == 86
    assert get_seed_location(13, test_mappings) == 35

    with open("puzzle_input") as puzzle_input:
        seeds, mappings = get_inputs(puzzle_input.read())

    seed_location = min([get_seed_location(seed, mappings) for seed in seeds])

    print(f"Part 1: seed location is {seed_location}")


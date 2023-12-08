""" https://adventofcode.com/2023/day/1
--- Day 1: Trebuchet?! ---
Something is wrong with global snow production, and you've been selected to take a look. The Elves have even given
you a map; on it, they've used stars to mark the top fifty locations that are likely to be having problems.

You've been doing this long enough to know that to restore snow operations, you need to check all fifty stars by
December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the
second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

You try to ask why they can't just use a weather machine ("not powerful enough") and where they're even
sending you ("the sky") and why your map looks mostly blank ("you sure ask a lot of questions") and hang on
did you just say the sky ("of course, where do you think snow comes from") when you realize that the Elves are
already loading you into a trebuchet ("please hold still, we need to strap you in").

As they're making the final adjustments, they discover that their calibration document (your puzzle input) has
been amended by a very young Elf who was apparently just excited to show off her art skills. Consequently, the
Elves are having trouble reading the values on the document.

The newly-improved calibration document consists of lines of text; each line originally contained a specific
calibration value that the Elves now need to recover. On each line, the calibration value can be found by
combining the first digit and the last digit (in that order) to form a single two-digit number.

For example:

1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

Consider your entire calibration document. What is the sum of all the calibration values?

--- Part Two ---
Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and last digit on each line. For example:

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.

What is the sum of all the calibration values?
"""
word_to_digit_mapping = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def get_first_digit_in_string(text: str):
    for char in text:
        if char.isdigit():
            return char


def get_first_word_digit(text: str):
    first_found_digit_words = {
        key: text.find(key)
        for key, value in word_to_digit_mapping.items()
        if key in text
    }
    if len(first_found_digit_words) > 0:
        first_word_digit = min(first_found_digit_words, key=first_found_digit_words.get)
        text = text.replace(
            first_word_digit, str(word_to_digit_mapping[first_word_digit])
        )

    return get_first_digit_in_string(text)


def get_last_word_digit(text: str):
    last_found_digit_words = {
        key: text.rfind(key)
        for key, value in word_to_digit_mapping.items()
        if key in text
    }
    if len(last_found_digit_words) > 0:
        last_word_digit = max(last_found_digit_words, key=last_found_digit_words.get)
        text = text.replace(
            last_word_digit, str(word_to_digit_mapping[last_word_digit])
        )

    return get_first_digit_in_string(text[::-1])


def get_line_calibration_value(text: str):
    digit_1 = get_first_word_digit(text)
    digit_2 = get_last_word_digit(text)

    return int(digit_1 + digit_2)


if __name__ == "__main__":
    assert get_line_calibration_value("1abc2") == 12
    assert get_line_calibration_value("pqr3stu8vwx") == 38
    assert get_line_calibration_value("a1b2c3d4e5f") == 15
    assert get_line_calibration_value("treb7uchet") == 77
    assert get_line_calibration_value("two1nine") == 29
    assert get_line_calibration_value("eightwothree") == 83
    assert get_line_calibration_value("abcone2threexyz") == 13
    assert get_line_calibration_value("xtwone3four") == 24
    assert get_line_calibration_value("4nineeightseven2") == 42
    assert get_line_calibration_value("zoneight234") == 14
    assert get_line_calibration_value("7pqrstsixteen") == 76
    assert get_line_calibration_value("three3qs7sevenpkjone18twonek") == 31
    assert get_line_calibration_value("lkvtwone1zpkjnbjtjrqppqsksdz") == 21
    assert get_line_calibration_value("twone") == 21  # this one got me at first...

    with open("puzzle_input") as file:
        final_answer = sum(
            get_line_calibration_value(line) for line in file.readlines()
        )

    wrong_answers = [53559, 53561]
    assert final_answer not in wrong_answers

    print(f"Final answer: {final_answer}")

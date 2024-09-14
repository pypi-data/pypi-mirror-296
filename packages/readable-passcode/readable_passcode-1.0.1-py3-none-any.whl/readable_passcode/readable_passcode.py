import random
import string
import os
import argparse

# Get the current directory to locate the word file
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
WORD_FILE_PATH = os.path.join(CURRENT_DIR, "words.txt")


def load_words(file_path=WORD_FILE_PATH):
    """
    Generator to lazily load words from a text file.

    :param file_path: Path to the text file containing words.
    :yield: A word from the file.
    """
    with open(file_path, "r") as file:
        for line in file:
            yield line.strip()


def count_words_in_file(file_path=WORD_FILE_PATH):
    """
    Count the number of lines (words) in the text file.

    :param file_path: Path to the text file.
    :return: Total number of lines (words) in the file.
    """
    with open(file_path, "r") as file:
        return sum(1 for line in file)


def get_random_words_directly(file_path=WORD_FILE_PATH, word=3):
    """
    Retrieve random words directly from a file
    without loading the whole file into memory.

    :param file_path: Path to the text file.
    :param word: Number of random words to select.
    :return: A list of random words.
    """
    total_words = count_words_in_file(file_path)
    random_words = []

    with open(file_path, "r") as file:
        for _ in range(word):
            random_line_number = random.randint(0, total_words - 1)
            for i, line in enumerate(file):
                if i == random_line_number:
                    random_words.append(line.strip())
                    break
            file.seek(0)  # Reset file pointer for the next iteration

    return random_words


def passcode_generator(word=3, number=0, special_char=False):
    """
    Generates a human-readable passcode by combining words
    with optional custom-length number and special character.

    :param word: Number of words to include in the passcode.
    :param number: The length of the random number to append.
    :param special_char: Whether to append a random special character
    :return: A human-readable passcode.
    """
    passcode_words = get_random_words_directly(word=word)
    passcode = "-".join(passcode_words)
    if number:
        str_number = "".join(
            random.choice(string.digits) for _ in range(number)
        )
        passcode += f"-{str_number}"
    if special_char:
        passcode += random.choice(string.punctuation)

    return passcode


# CLI handler function
def cli():
    parser = argparse.ArgumentParser(
        description="Generate a human-readable passcode."
    )

    parser.add_argument(
        "--word",
        type=int,
        default=3,
        help="Number of words in the passcode (default: 3)",
    )
    parser.add_argument(
        "--number",
        type=int,
        help="Length of the number",
    )
    parser.add_argument(
        "--special-char",
        action="store_true",
        help="Include a special character",
    )

    args = parser.parse_args()

    # Generate passcode based on CLI arguments
    passcode = passcode_generator(
        word=args.word,
        number=args.number,
        special_char=args.special_char,
    )

    print(passcode)


if __name__ == "__main__":
    cli()

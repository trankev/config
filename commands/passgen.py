import argparse

import pathlib
import secrets
import typing

DICTIONARY_FOLDER = pathlib.Path("/usr/share/dict")
DICTIONARIES = [
    DICTIONARY_FOLDER / "french",
    # DICTIONARY_FOLDER / "catalan",
    DICTIONARY_FOLDER / "ngerman",
    DICTIONARY_FOLDER / "british-english",
    # DICTIONARY_FOLDER / "italian",
    DICTIONARY_FOLDER / "spanish",
    # DICTIONARY_FOLDER / "finnish",
]
PADDING_CHARACTERS = "0123456789!@#$%&_+-=[]{}|\\/?<>"


def iter_words() -> typing.Iterator[str]:
    for filepath in DICTIONARIES:
        with filepath.open() as fd:
            yield from (line.strip() for line in fd)


def filter_characters(words: typing.Iterator[str], chars: str) -> typing.Iterator[str]:
    for word in words:
        for char in chars:
            if char in word:
                break
        else:
            yield word


def filter_length(words: typing.Iterator[str], *, at_least: int = 0, at_most: int = 0) -> typing.Iterator[str]:
    for word in words:
        if at_least and len(word) < at_least:
            continue
        if at_most and len(word) > at_most:
            continue
        yield word


def choices(sequence: typing.Sequence[str], *, k: int = 1) -> typing.Set[str]:
    result = set()
    while len(result) < k:
        result.add(secrets.choice(sequence))
    return result


def pad_symbols(word: str, symbols: str) -> str:
    symbol = secrets.choice(symbols)
    position = secrets.randbelow(len(word))
    return "".join((word[:position], symbol, word[position:]))


def run(args: argparse.Namespace) -> None:
    words = filter_characters(iter_words(), "'")
    words = filter_length(words, at_least=args.min_length, at_most=args.max_length)
    words = list(set(words))
    chosen = choices(words, k=args.word_count)
    password = "".join(chosen)
    padding_count = secrets.randbelow(args.max_padding - args.min_padding) + args.min_padding
    for _ in range(padding_count):
        password = pad_symbols(password, args.characters)
    print(password)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--word-count", type=int, default=4)
    parser.add_argument("-m", "--min-length", type=int, default=4)
    parser.add_argument("-M", "--max-length", type=int, default=10)
    parser.add_argument("-p", "--min-padding", type=int, default=3)
    parser.add_argument("-P", "--max-padding", type=int, default=6)
    parser.add_argument("-c", "--characters", default=PADDING_CHARACTERS)
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()

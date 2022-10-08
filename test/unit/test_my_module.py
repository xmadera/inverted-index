import pprint

import inverted_index


def test_main():
    pprint.pprint(
        inverted_index.inverted_index_of(
            [
                ("001", "https://www.gutenberg.org/cache/epub/69042/pg69042.txt"),
                ("002", "https://www.gutenberg.org/cache/epub/69035/pg69035.txt"),
                ("003", "https://www.gutenberg.org/cache/epub/69040/pg69040.txt"),
            ]
        )
    )

import inverted_index


def test_main():
    inverted_index.inverted_index_of(
        [
            "https://www.gutenberg.org/cache/epub/69042/pg69042.txt",
            "https://www.gutenberg.org/cache/epub/69035/pg69035.txt",
            "https://www.gutenberg.org/cache/epub/69040/pg69040.txt",
        ]
    )

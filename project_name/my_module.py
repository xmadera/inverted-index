import re
import urllib.request
import string


def inverted_index_of(document_list):
    data_into_list = []
    # Open txt from url
    document = urllib.request.urlopen(document_list)

    for line in document.readlines():
        formatted_line = re.split(r'\W+', line.decode('utf-8').lower())
        # Translate each word to remove punctuations --> !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
        punctuations = str.maketrans('', '', string.punctuation)
        formatted_without_punctuations = [w.translate(punctuations) for w in formatted_line]
        data_into_list.extend(filter(None, formatted_without_punctuations))

    # printing the data
    print(data_into_list)


if __name__ == '__main__':
    inverted_index_of("https://www.gutenberg.org/cache/epub/69042/pg69042.txt")

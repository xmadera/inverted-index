import re
import string
import urllib.request
import nltk
from googletrans import Translator


def inverted_index_of(document_list):
    translator = Translator()

    document_object = {}

    for doc_id, doc_url in document_list:
        data_into_list = []

        """ Open txt from url """
        document = urllib.request.urlopen(doc_url)

        for line in document.readlines():
            # remove numbers
            line_without_numbers = re.sub(r'\d+', '', line.decode('utf-8').lower())

            formatted_line = re.split(r'\W+', line_without_numbers)

            # Translate each word to remove punctuations --> !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
            punctuations = str.maketrans('', '', string.punctuation)

            formatted_without_punctuations = [w.translate(punctuations) for w in formatted_line]

            formatted_without_empty = list(filter(None, formatted_without_punctuations))

            for word in formatted_without_empty:
                translated = translator.detect(word)
                # print(translated)

            data_into_list.extend(formatted_without_empty)

        data_into_list = list(dict.fromkeys(data_into_list))

        """ Tagged list --> To remove conjunctions, prepositions, etc.."""
        data_into_list_tagged = nltk.pos_tag(data_into_list)
        for tagged_word in data_into_list_tagged:
            # TODO: Add next tag keys
            if tagged_word[1] == "CC" or tagged_word[1] == "TO" or not tagged_word[0]:
                data_into_list.remove(tagged_word[0])

        """ Save non inverted index dictionary"""
        document_object[doc_id] = data_into_list
        # print(data_into_list)

    """ Convert to inverted index dictionary"""
    inv_idx_dict = dict()
    for key in document_object:
        # Go through the list that is saved in the document_object:
        for item in document_object[key]:
            # Check if in the inverted dict (inv_idx_dict) the key exists
            if item not in inv_idx_dict:
                # If not create a new list
                inv_idx_dict[item] = [key]
            else:
                inv_idx_dict[item].append(key)

    # pprint.pprint(inv_idx_dict)
    return inv_idx_dict

# TODO: Remove prepositions, conjunctions etc.. from documents
# https://stackoverflow.com/questions/24406201/how-do-i-remove-verbs-prepositions-conjunctions-etc-from-my-text
# https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html

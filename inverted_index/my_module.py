import json
import re
import string
import urllib.request

from cld3 import _cld3 as cld3
import nltk
from dict2xml import dict2xml


def inverted_index_of(document_list):
    document_dictionary = {}

    for doc_url in document_list:
        # Init variables for every document
        data_into_list = []
        document_id = 0
        document_metadata = {"ID": 0, "Title": "", "Author": "", "Release Date": "", "Produced by": ""}

        """ Open txt from url """
        document = urllib.request.urlopen(doc_url)

        for line in document.readlines():
            """Get book ID from document"""
            if document_id == 0:
                match_document_id = re.findall(r'eBook #(\d+)', line.decode('utf-8'))
                if match_document_id:
                    document_id = int(match_document_id[0])
                    document_metadata["ID"] = int(match_document_id[0])

            """ Reading metadata """
            # Metadata such as [Title, Author, Release Date, Language, Produced by]
            if document_metadata["Title"] == "":
                match_title = re.findall('^Title: (.+)', line.decode('utf-8'))
                if match_title:
                    document_metadata["Title"] = match_title[0].rstrip()
            if document_metadata["Author"] == "":
                match_title = re.findall('^Author: (.+)', line.decode('utf-8'))
                if match_title:
                    document_metadata["Author"] = match_title[0].rstrip()
            if document_metadata["Release Date"] == "":
                match_title = re.findall('^Release Date: (.+)', line.decode('utf-8'))
                if match_title:
                    document_metadata["Release Date"] = match_title[0].rstrip()
            if document_metadata["Produced by"] == "":
                match_title = re.findall('^Produced by: (.+)', line.decode('utf-8'))
                if match_title:
                    document_metadata["Produced by"] = match_title[0].rstrip()

            """ Cleaning & formatting document text """
            # remove numbers
            line_without_numbers = re.sub(r'\d+', '', line.decode('utf-8').lower())

            formatted_line = re.split(r'\W+', line_without_numbers)

            # Translate each word to remove punctuations --> !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
            punctuations = str.maketrans('', '', string.punctuation)

            formatted_without_punctuations = [w.translate(punctuations) for w in formatted_line]

            formatted_without_empty = list(filter(None, formatted_without_punctuations))

            data_into_list.extend(formatted_without_empty)

        data_into_list = list(dict.fromkeys(data_into_list))

        """ Tagged list --> To remove conjunctions, prepositions, etc.. """
        data_into_list_tagged = nltk.pos_tag(data_into_list)
        for tagged_word in data_into_list_tagged:
            if tagged_word[1] == "CC" or tagged_word[1] == "TO" or tagged_word[1] == "IN" or tagged_word[
                1] == "DT" or not tagged_word[0]:
                data_into_list.remove(tagged_word[0])

        """ Remove non-english words --> (extension) choose language """
        language_list = []
        for word in data_into_list:
            language_detection = cld3.get_language(word)
            language_list.append(language_detection)

        """ Save non inverted index dictionary"""
        document_dictionary[document_id] = data_into_list

        with open(str(document_id) + '.txt', 'w') as f:
            f.write('METADATA\n\n')
            for key, value in document_metadata.items():
                f.write('%s: %s\n' % (key, value))
        f.close()

    """ Convert to inverted index dictionary"""
    inv_idx_document_dict = dict()
    for key in document_dictionary:
        # Go through the list that is saved in the document_dictionary:
        for item in document_dictionary[key]:
            # Check if in the inverted dict (inv_idx_document_dict) the key exists
            if item not in inv_idx_document_dict:
                # If not create a new list
                inv_idx_document_dict[item] = [key]
            else:
                inv_idx_document_dict[item].append(key)

    # Serializing into xml
    xml = dict2xml(inv_idx_document_dict)
    # print(xml)

    # Serializing into json
    json_object = json.dumps(inv_idx_document_dict, indent=4)
    # print(json_object)

    return inv_idx_document_dict

# Remove prepositions, conjunctions etc.. from documents
# https://stackoverflow.com/questions/24406201/how-do-i-remove-verbs-prepositions-conjunctions-etc-from-my-text
# https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html

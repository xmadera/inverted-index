import re
import string
import urllib.request
# import pprint
import nltk
from langdetect import detect


def inverted_index_of(document_list):
    document_object = {}

    for doc_url in document_list:
        # Init variables for every document
        data_into_list = []
        document_id = 0
        document_metadata = {
            "ID": 0,
            "Title": "",
            "Author": "",
            "Release Date": "",
            "Produced by": ""
        }

        """ Open txt from url """
        document = urllib.request.urlopen(doc_url)

        for line in document.readlines():

            """ Get book ID from document """
            if document_id == 0:
                match_document_id = re.findall('eBook #(\d+)', line.decode('utf-8'))
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
            # TODO: Add next tag keys
            if tagged_word[1] == "CC" or tagged_word[1] == "TO" or not tagged_word[0]:
                data_into_list.remove(tagged_word[0])

        """ Remove non-english words --> (extension) choose language """
        for word in data_into_list:
            lang = detect(word)
            if lang != "en":
                data_into_list.remove(word)

        """ Save non inverted index dictionary"""
        document_object[document_id] = data_into_list

        # pprint.pprint(document_metadata)
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

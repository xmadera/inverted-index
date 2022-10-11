import json
import re
import ssl
import string
from urllib.request import urlopen

import nltk
from cld3 import _cld3 as cld3
from dict2xml import dict2xml

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def inverted_index_of(document_list):
    document_dictionary = {}
    document_dictionary_metadata = {}
    word_dictionary_language = {}
    word_dictionary_chapters = {}

    for doc_url in document_list:
        # Init variables for every document
        data_into_list = []
        document_id = 0
        document_metadata = {"id": "", "title": "", "author": "", "release_date": "", "produced_by": ""}
        current_chapter = ""

        """ Open txt from url """
        document = urlopen(doc_url, context=ctx)

        for line in document.readlines():
            decoded_line = line.decode('utf-8')

            document_id = handle_metadata(decoded_line, document_id, document_metadata)

            handle_text_line(current_chapter, data_into_list, decoded_line)

        data_into_list = list(dict.fromkeys(data_into_list))

        for word in data_into_list:
            if word not in word_dictionary_chapters:
                word_dictionary_chapters[word] = [current_chapter]
            else:
                word_dictionary_chapters[word].append(current_chapter)

        tag_word_list(data_into_list)

        get_word_language(data_into_list, word_dictionary_language)

        """ Save non inverted index dictionary """
        document_dictionary[document_id] = data_into_list

        """ Save Document metadata into dictionary """
        document_dictionary_metadata[document_id] = document_metadata

    inv_idx_document_dict = convert_word_dictionary_to_inverted_index(document_dictionary)

    """ Add language object to inverted dictionary """
    for key in inv_idx_document_dict:
        inv_idx_document_dict[key].append({"language": word_dictionary_language[key].language})

    handle_documents_serialization(document_dictionary_metadata)

    handle_words_serialization(inv_idx_document_dict)


def handle_words_serialization(inv_idx_document_dict):
    # Serialize into xml
    xml_inc_idx_document = dict2xml(inv_idx_document_dict, indent="    ", wrap="words")
    # Save json into file
    with open('words/words.xml', 'w') as f:
        f.write(xml_inc_idx_document)
    f.close()
    # Serialize into json
    json_inc_idx_document = json.dumps(inv_idx_document_dict, indent="    ")
    # Save json into file
    with open('words/words.json', 'w') as f:
        f.write(json_inc_idx_document)
    f.close()


def handle_documents_serialization(document_dictionary_metadata):
    # Serialize into xml
    xml_document_metadata = '<?xml version="1.0" encoding="UTF-8"?>\n' + dict2xml(
        document_dictionary_metadata, indent="    ", wrap="metadata"
    )
    # Save xml into file
    with open('documents/metadata.xml', 'w') as f:
        f.write(xml_document_metadata)
    f.close()
    # Serialize into json
    json_document_metadata = json.dumps(document_dictionary_metadata, indent="    ")
    # Save json into file
    with open('documents/metadata.json', 'w') as f:
        f.write(json_document_metadata)
    f.close()


def convert_word_dictionary_to_inverted_index(document_dictionary):
    """Convert to inverted index dictionary"""
    inv_idx_document_dict = dict()
    for key in document_dictionary:
        # Go through the list that is saved in the document_dictionary:
        for item in document_dictionary[key]:
            # Check if in the inverted dict (inv_idx_document_dict) the key exists
            if item not in inv_idx_document_dict:
                # If not create a new list
                inv_idx_document_dict[item] = [{"document_id": [key]}]
            else:
                inv_idx_document_dict[item][0]["document_id"].append(key)

    return inv_idx_document_dict


def get_word_language(data_into_list, word_dictionary_language):
    """Save word language detection into dictionary"""
    for word in data_into_list:
        language_detection = cld3.get_language(word)
        word_dictionary_language[word] = language_detection


def tag_word_list(data_into_list):
    """Tagged list --> To remove conjunctions, prepositions, etc.."""
    data_into_list_tagged = nltk.pos_tag(data_into_list)
    for tagged_word in data_into_list_tagged:
        if (
            tagged_word[1] == "CC"
            or tagged_word[1] == "TO"
            or tagged_word[1] == "IN"
            or tagged_word[1] == "DT"
            or not tagged_word[0]
        ):
            data_into_list.remove(tagged_word[0])


def handle_text_line(current_chapter, data_into_list, decoded_line):
    """Cleaning & formatting document text"""
    # remove numbers
    line_without_numbers = re.sub(r'\d+', '', decoded_line.lower())
    formatted_line = re.split(r'\W+', line_without_numbers)

    # Translate each word to remove punctuations --> !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    punctuations = str.maketrans('', '', string.punctuation)
    formatted_without_punctuations = [w.translate(punctuations) for w in formatted_line]
    formatted_without_empty = list(filter(None, formatted_without_punctuations))

    data_into_list.extend(formatted_without_empty)

    # TODO chapter
    # if (len(formatted_without_empty) == 1):
    #     if (is_roman_number(formatted_without_empty[0].upper())):
    #         current_chapter = formatted_without_empty[0]


def handle_metadata(decoded_line, document_id, document_metadata):
    """Get book ID from document"""
    if document_id == 0:
        match_document_id = re.findall(r'eBook #(\d+)', decoded_line)
        if match_document_id:
            document_id = match_document_id[0]
            document_metadata["id"] = int(match_document_id[0])

    """ Reading metadata """
    # Metadata such as [Title, Author, Release Date, Language, Produced by]
    if document_metadata["title"] == "":
        match_title = re.findall('^Title: (.+)', decoded_line)
        if match_title:
            document_metadata["title"] = match_title[0].rstrip()
    if document_metadata["author"] == "":
        match_title = re.findall('^Author: (.+)', decoded_line)
        if match_title:
            document_metadata["author"] = match_title[0].rstrip()
    if document_metadata["release_date"] == "":
        match_title = re.findall('^Release Date: (.+)', decoded_line)
        if match_title:
            document_metadata["release_date"] = match_title[0].rstrip()
    if document_metadata["produced_by"] == "":
        match_title = re.findall('^Produced by: (.+)', decoded_line)
        if match_title:
            document_metadata["produced_by"] = match_title[0].rstrip()

    return document_id


def is_roman_number(num):
    pattern = re.compile(
        r"""   
                                ^M{0,3}
                                (CM|CD|D?C{0,3})?
                                (XC|XL|L?X{0,3})?
                                (IX|IV|V?I{0,3})?$
            """,
        re.VERBOSE,
    )

    if re.match(pattern, num):
        return True

    return False


# Remove prepositions, conjunctions etc.. from documents
# https://stackoverflow.com/questions/24406201/how-do-i-remove-verbs-prepositions-conjunctions-etc-from-my-text
# https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html

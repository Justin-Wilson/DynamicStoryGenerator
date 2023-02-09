import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

# Load the default English corpus in nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')

def proper_nouns(text):
    # Tokenize the text
    words = word_tokenize(text)

    # Part of speech tagging for the words
    tagged_words = pos_tag(words)

    # Store proper nouns and their indexes in a dictionary
    proper_nouns = {}
    for index, (word, pos) in enumerate(tagged_words):
        if pos == 'NNP':
            proper_nouns[index] = word

    return proper_nouns

def pronouns(text):
    words = word_tokenize(text)
    tagged_words = nltk.pos_tag(words)
    pronouns = {}
    for index, tagged_word in enumerate(tagged_words):
        word, tag = tagged_word
        if tag == "PRP":
            pronouns[index] = word.lower()
    return pronouns

def replace_values(document, new_proper_noun, new_pronouns):
    # Load the .docx file
    from docx import Document
    document = Document(document)

    # Combine all text from the .docx file
    text = ""
    for para in document.paragraphs:
        text += para.text.rstrip()

    # Get Dictionaries
    proper_nouns_dict = proper_nouns(text)
    print("Proper Nouns Dict:", proper_nouns_dict)
    pronouns_dict = pronouns(text)
    print("Pronouns Dict:", pronouns_dict)

    # Print the original text
    print("Original Text: \n", text)

    pronoun_map = {
        "he": "she",
        "his": "her's",
        "him": "her",
        "she": "he",
        "her's": "his",
        "her": "him",
        "they": "they"
    }

    # Replace the proper nouns with the new values
    words = word_tokenize(text)
    for index in proper_nouns_dict:
        words[index] = new_proper_noun
    for index in pronouns_dict:
        words[index] = pronoun_map[pronouns_dict[index]]

    # Print the new text
    new_text = " ".join(words)
    new_text = new_text.replace(" . ", ". ")
    print("New Text: \n", new_text)


# Call the function
replace_values("story_text.docx", "John", "he/his/him")

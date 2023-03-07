import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
from nltk.tree import Tree
import re

# Load the default English corpus in nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')

def replace_names(text, replacement):
    # Tokenize the text and tag each token with its part of speech
    tokens = word_tokenize(text)
    tagged = pos_tag(tokens)
    
    # Use NLTK's named entity chunker to identify entities in the text
    chunked = ne_chunk(tagged)
    
    # Find all the named entities that are labeled as a person
    names = []
    for subtree in chunked.subtrees(filter=lambda t: t.label() == 'PERSON'):
        name = ' '.join(word for word, pos in subtree.leaves())
        names.append(name)
    
    # Replace each instance of each name with the specified replacement string
    for name in names:
        text = re.sub(r'\b{}\b'.format(re.escape(name)), replacement, text)

    #print("Number of names found: ", len(names))
    
    return text

def replace_pronouns(text, pronoun_string):
    pronoun_list = pronoun_string.split('/')
    pronoun_map = {
        "he": pronoun_list[0],
        "him": pronoun_list[1],
        "his": pronoun_list[2],
        "himself": pronoun_list[1] + 'self',
        "she": pronoun_list[0],
        "her": pronoun_list[2],
        "hers": pronoun_list[2],
        "herself": pronoun_list[1] + 'self',
        # This is alot harder to do, I dont know if the client wants it. 
        # But this is a 1 to many mapping depending on the rest of the sentence

        # "they": "they",
        # "them": pronoun_list[1],
        # "their": pronoun_list[2],
        # "theirs": pronoun_list[2] + 's',
        # "themselves": pronoun_list[1] + 'selves'
    }

    regex = re.compile(r'\b(?:he|him|his|himself|she|her|hers|herself)\b', re.IGNORECASE)
    matches = regex.findall(text)

    if len(matches) > 0:
        #print("Pronouns found:", ', '.join(matches))
        new_text = regex.sub(lambda match: pronoun_map[match.group(0).lower()], text)
        return new_text
    else:
        return text

def gender_terms(text):
    # define the gender tags
    gender_tags = ['NN', 'NNS', 'NNP', 'NNPS']
    # tokenize the text into words
    words = word_tokenize(text)
    # perform part-of-speech tagging on the words
    pos_tags = nltk.pos_tag(words)
    # extract all the gender identifying terms from the text
    gender_terms = {}
    for index, tagged_word in enumerate(pos_tags):
        word, tag = tagged_word
        if tag in gender_tags and word.lower() in ['boy', 'girl', 'man', 'woman']:
            gender_terms[index] = word.lower()

    #print("Number of gender terms found: ", len(gender_terms))
    
    return gender_terms

def capitalize_sentences(text):
    # Split the text into sentences
    sentences = sent_tokenize(text)
    # Capitalize the first letter of each sentence
    capitalized_sentences = [sentence.capitalize() for sentence in sentences]
    # Join the sentences back into a single string
    capitalized_text = " ".join(capitalized_sentences)
    return capitalized_text

def recapitalize_name(word, text):
    # split the text into words
    words = text.split()
    
    # loop through the words and capitalize the instances of the given word
    for i in range(len(words)):
        if words[i].lower() == word.lower():
            words[i] = words[i].capitalize()
    
    # join the words back into a string
    capitalized_text = " ".join(words)
    
    return capitalized_text


def possessives(text):
    words = word_tokenize(text)
    tagged_words = nltk.pos_tag(words)
    possessives = {}
    for index, tagged_word in enumerate(tagged_words):
        word, tag = tagged_word
        if tag == "PRP$":
            possessives[index] = word.lower()
    return possessives

possessive_map = {
    "his": "her",
    "her": "his",
    "they": "they",
    "she": "he",
    "their": "their"
}


def replace_values(document, new_name, new_pronouns, new_gender_term):
    # Load the .docx file
    from docx import Document
    document = Document(document)

    # Combine all text from the .docx file
    text = ""
    for para in document.paragraphs:
        text += para.text.rstrip()

    # Get Dictionaries
    gender_terms_dict = gender_terms(text)
    possessives_dict = possessives(text)
    print("Possessive Dict:", possessives_dict)

    # Print the original text
    print("Original Text: \n", text)

    # Replace the proper nouns with the new values
    words = word_tokenize(text)
    for index in gender_terms_dict:
        words[index] = new_gender_term
    for index in possessives_dict:
        words[index] = possessive_map[possessives_dict[index]]

    # Print the new text
    ## Convert list of words back to text
    new_text = " ".join(words)
    new_text = new_text.replace(" . ", ". ").replace(" , ", ", ").replace(" ' ","' ")

     #Replace Names
    new_text = replace_names(new_text, new_name)
    #print("Before pronoun switch: \n", new_text)
    #print("Before pronoun replace: \n", new_text)
    new_text = replace_pronouns(new_text, new_pronouns)
    #print("After pronoun replacemet: \n", new_text)
    #print("Combined back to text: \n", new_text, "\n")
    new_text = new_text.replace(" . ", ". ").replace(" , ", ", ").replace(" ' ","' ")

    # Capitalize letters after periods
    capitalized_text = capitalize_sentences(new_text)
    capitalized_text = recapitalize_name(new_name, new_text)
    print("New text: \n", capitalized_text, "\n")



# Call the function hard coded for now.
replace_values("story_text_test1.docx", "Tim", "he/him/his", "boy")
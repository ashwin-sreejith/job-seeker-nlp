import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk import RegexpTokenizer
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.probability import *
from itertools import chain


# save file paths
stopwords_file_path = "process/stopwords_en.txt"


def tokenize(raw_data):
    """Tokenizes the given string and returns it in lower case"""
    pattern = r"[a-zA-Z]+(?:[-'][a-zA-Z]+)?"
    data_str_lower = raw_data.lower()
    sentences = sent_tokenize(data_str_lower)
    tokenizer = RegexpTokenizer(pattern)
    token_lists = [tokenizer.tokenize(sen) for sen in sentences]
    tokenised_data = list(chain.from_iterable(token_lists))
    tokenised_data = [token for token in tokenised_data if token != 'nbsp']
    return tokenised_data


def tokenizer(field):
    """Creates a list of tokens corresponding to each description"""
    token_list = [tokenize(ad) for ad in field]
    return token_list


def rem_word_less_than_two(token_list):
    """Removes words with length less than 2 amd returns the list"""
    token_list = [word for word in token_list if len(word) >= 2]
    return token_list


def load_stopwords(path):
    """Loads the stopwords file using specified path and returns set of stop words"""
    with open(path, 'r') as file:
        stopwords_list = file.read().splitlines()
    return set(stopwords_list)


def rem_stop_words(token_list, stopword_set):
    """Removes the stopwords and returns the list"""
    token_list = [word for word in token_list if word not in stopword_set]
    return token_list


def lemmatise(lemmatizer, token_list):
    """Lemmatises and returns the list"""
    token_list = [lemmatizer.lemmatize(word) for word in token_list]
    return token_list


def preprocess(text_descriptions):
    # token_list = tokenizer(text_descriptions)
    token_list = tokenize(text_descriptions)
    token_list = rem_word_less_than_two(token_list)
    stopword_set = load_stopwords(stopwords_file_path)
    token_list = rem_stop_words(token_list, stopword_set)
    lemmatizer = WordNetLemmatizer()
    token_list = lemmatise(lemmatizer, token_list)
    return token_list

# ### References

# - [1]Gallagher, L 20230, 'ex1_movie_preprocess.ipynb', Lab Material, COSC2820, RMIT University, Melbourne.
# - [2]Gallagher, L 20230, 'w08_ex1_solution.ipynb', Lab Material, COSC2820, RMIT University, Melbourne.
# - [3]Gallagher, L 20230, 'w09_act1_term_embedding.ipynb', Lab Material, COSC2820, RMIT University, Melbourne.
# - [4]Gallagher, L 20230, 'w09_act2_embedding_classification.ipynb', Lab Material, COSC2820, RMIT University, Melbourne.

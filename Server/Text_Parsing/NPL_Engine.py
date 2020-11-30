import nltk
import gensim
import string
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from gensim.corpora.dictionary import Dictionary
from gensim.models import Word2Vec, KeyedVectors
from collections import Counter

# Downloads for nltk:
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

# Word2vec related:
MODEL = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True, limit=100000)
CLUSTER = [x[0] for x in MODEL.most_similar_cosmul("volunteer", topn=120)]

# Topic identification related:
STOPWORDS = set(stopwords.words('english'))
EXCLUDE = set(string.punctuation)
LEMMA = WordNetLemmatizer()


def clean(document):
    """
        clean: This function cleans a string (multiple words) and returns it, preserving the order.
    """
    stopwords_removal = " ".join([i for i in document.lower().split() if i not in STOPWORDS])
    punctuation_removal = ''.join(ch for ch in stopwords_removal if ch not in EXCLUDE)
    normalized = " ".join(LEMMA.lemmatize(word) for word in punctuation_removal.split())
    return normalized


def make_lda_model(document, num_topics, passes):
    """
        make_lda_model: This function will make an LDA (latent dirichlet allocation) model from the provided
        document, number of topics and the number of passes on said document.

        document: list of lists of strings (multiple words). needs to be clean.
    """
    dictionary = gensim.corpora.Dictionary(document)
    document_term_matrix = [dictionary.doc2bow(doc) for doc in document]
    lda_object = gensim.models.ldamodel.LdaModel
    lda_model = lda_object(document_term_matrix, num_topics=num_topics, passes=passes, id2word=dictionary)
    return lda_model


def make_bag_of_words(document):
    """
        make_bag_of_words: This function will clean the provided document and return a BOW.
    """
    tokens = word_tokenize(clean(document))
    bag_of_words = Counter(tokens)
    return bag_of_words


def calculate_bow_relation_to_cluster(bag_of_words):
    pass


def main():
    """
        Used for testing only.
    """
    test = ["Avengers: Infinity War was a 2018 American superhero film based on the Marvel Comics superhero team the " 
            "Avengers. It is the 19th film in the Marvel Cinematic Universe (MCU). The running time of the movie was "
            "149 minutes and the box office collection was around 2 billion dollars. (Source: Wikipedia) "]
    bow = make_bag_of_words(test[0])
    print("After cleaning: " + str(bow.most_common(5)))
    pass


if __name__ == '__main__':
    main()

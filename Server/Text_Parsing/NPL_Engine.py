import gensim
import string
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from gensim.corpora.dictionary import Dictionary
from gensim.models import Word2Vec, KeyedVectors
from collections import Counter

# Downloads for nltk:
"""
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
"""


# Thresholds:
EMERGENCY_THRESHOLD = 11
HAVER_THRESHOLD = 8.5

# Word2vec related:
MODEL = KeyedVectors.load_word2vec_format('Text_Parsing/GoogleNews-vectors-negative300.bin',
                                          binary=True, limit=100000)
POST_CLUSTER = [x[0] for x in MODEL.most_similar(positive=["volunteer", "help", "contribution", "love"],
                                                 negative=["hate", "stupid", "annoying", "racism"],
                                                 topn=125)]
HEALTH_CLUSTER = [x[0] for x in MODEL.most_similar(positive=["help", "medicine", "hurt", "injured", "doctor", "pain",
                                                             "feeling", "sick", "headache", "ache", "drugs"], topn=100)]

# Topic identification related:
STOPWORDS = set(stopwords.words('english'))
EXCLUDE = set(string.punctuation)
LEMMA = WordNetLemmatizer()


def clean(document):
    """
        clean: This function cleans a string (multiple words) and returns it, preserving the order.
        This is an internal function, it is not necessary for BOW operations in this document.
    """
    stopwords_removal = " ".join([i for i in document.lower().split() if i not in STOPWORDS])
    punctuation_removal = ''.join(ch for ch in stopwords_removal if ch not in EXCLUDE)
    numeric_removal = " ".join([i for i in punctuation_removal.split() if i.isalpha()])
    normalized = " ".join(LEMMA.lemmatize(word) for word in numeric_removal.split())
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
    """
        calculate_bow_relation_to_cluster: This function will calculate the resemblance of the BOW to the word cluster
        and returns a "resemblance score".
    """
    total_score = 0
    valid_word_count = 0
    for word_from_bag, occurrences in bag_of_words.items():
        if word_from_bag in MODEL:
            for word_from_cluster in POST_CLUSTER:
                current_iteration_score = MODEL.similarity(word_from_bag, word_from_cluster) * occurrences
                total_score = total_score + current_iteration_score
                # print("testing {} with {} = {}".format(word_from_bag, word_from_cluster, current_iteration_score))
            valid_word_count = valid_word_count + 1
    if valid_word_count != 0:
        total_score = total_score / valid_word_count
    else:
        total_score = 0
    print(total_score)
    return total_score


def determine_emergency_query(query):
    total_score = 0
    iteration_counter = 0
    query = clean(query)
    for word in query.strip().split():
        if word in MODEL:
            for word_from_cluster in HEALTH_CLUSTER:
                current_iteration_score = MODEL.similarity(word, word_from_cluster)
                total_score += current_iteration_score
                # print("testing {} with {} = {}".format(word, word_from_cluster, current_iteration_score))
            iteration_counter += 1
    if iteration_counter != 0:
        total_score = total_score / iteration_counter
    else:
        total_score = 0
    print(total_score)
    return total_score


def main_bow():
    """
        Used for testing only.
    """
    test = ["Avengers: Infinity War was a 2018 American superhero film based on the Marvel Comics superhero team the "
            "Avengers. It is the 19th film in the Marvel Cinematic Universe (MCU). The running time of the movie was "
            "149 minutes and the box office collection was around 2 billion dollars. (Source: Wikipedia) ",
            "Volunteering allows you to connect to your community and make it a better place. ... And volunteering is "
            "a two-way street: It can benefit you and your family as much as the cause you choose to help. Dedicating "
            "your time as a volunteer helps you make new friends, expand your network, and boost your social skills.",
            "One advanced diverted domestic sex repeated bringing you old. Possible procured her trifling laughter "
            "thoughts property she met way. Companions shy had solicitude favourable own.",
            "I would really like to volunteer at a foster care house",
            "I really hate annoying first graders that always ask stupid questions all the time for no reason",
            "Hi dear volunteers, I have access to a large database designed to gather reporters who are looking for "
            "items and I would be happy to help - are there volunteers and entrepreneurs here who are interested in "
            "exposure and would like to tell their story or their venture / volunteering platform between stories and "
            "reporters from many fields?"]
    bow = make_bag_of_words(test[0])
    bow2 = make_bag_of_words(test[1])
    bow3 = make_bag_of_words(test[2])
    bow4 = make_bag_of_words(test[3])
    bow5 = make_bag_of_words(test[4])
    bow6 = make_bag_of_words(test[5])

    calculate_bow_relation_to_cluster(bow)
    calculate_bow_relation_to_cluster(bow2)
    calculate_bow_relation_to_cluster(bow3)
    calculate_bow_relation_to_cluster(bow4)
    calculate_bow_relation_to_cluster(bow5)
    calculate_bow_relation_to_cluster(bow6)
    pass


def main_query():
    print("test: ", determine_emergency_query("headache"))

    queries = [
        "I need a doctor",
        "I need a doctor I don't feel well",
        "I need to buy medicine",
        "My head hurts",
        "I have a headache",
        "I am having trouble breathing",
        "supermarket",
        "I love unicorns",
        "I want a stick up my ass",
        "u gay",
        "son of a bitch"
    ]
    for query in queries:
        print(determine_emergency_query(query))


if __name__ == '__main__':
    main_bow()

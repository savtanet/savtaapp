# ***** NOT IN USE ******

from nltk.tokenize import sent_tokenize, word_tokenize
import gensim.downloader as wv

# loading google's model of word2vec.
module = wv.load('word2vec-google-news-300')


def calculate_paragraph(text, allowed_words=[], banned_words=[]):
    """
    Description: This function will use word2vec to understand if a given text is related to the topic.
                 The user should give a list for 'allowed_words' and list of 'banned_words',
                 so the function could calculate the resemblance of the given text to the given topic.
    Input: text - String - the text you want to analyze.
           allowed_words - List<String> - words related to the topic.
           banned_words - List<String> - words that are the opposite of the topic.
    Output: score - Tuple<Int> - resemblance score, banned score.
    """
    # getting all the allowed words from the text file.
    if not allowed_words:
        with open('Text_Parsing/Allowed_Words.txt', 'r') as f:
            while True:
                word = f.readline().lower().replace(' ', '').replace('\n', '')
                if word == '':
                    break
                else:
                    allowed_words.append(word)

    # getting all the banned words from the text file.
    if not banned_words:
        with open('Text_Parsing/Banned_Words.txt', 'r') as f:
            while True:
                word = f.readline().lower().replace(' ', '').replace('\n', '')
                if word == '':
                    break
                else:
                    banned_words.append(word)

    # getting all the important information from the given text.
    clean_data = []
    tokenized_text = sent_tokenize(text)
    for sentence in tokenized_text:
        for word in sentence.split(' '):
            clean_data.append(word.replace('.', '').replace(' ', '').lower())

    i_allowed = 0
    i_banned = 0
    allowed_words_average = 0.0
    banned_words_average = 0.0

    # calculating the averages of the paragraph.
    for word in clean_data:
        if allowed_words is not None:
            for allowed_word in allowed_words:
                try:
                    allowed_words_average += module.similarity(word, allowed_word)
                    i_allowed += 1
                except KeyError:
                    break
        if banned_words is not None:
            for banned_word in banned_words:
                try:
                    banned_words_average += module.similarity(word, banned_word)
                    i_banned += 1
                except KeyError:
                    break

    try:
        allowed_words_average = allowed_words_average / float(i_allowed)
    except ZeroDivisionError:
        pass
    try:
        banned_words_average = banned_words_average / float(i_banned)
    except ZeroDivisionError:
        pass

    return allowed_words_average, banned_words_average


def test_similarity_manually():
    try:
        while True:
            word1 = input('Enter first word: ')
            word2 = input('Enter second word: ')

            print(module.similarity(word1, word2))

    except KeyboardInterrupt:
        return


def calculate_similarity(w1, w2):
    return module.similarity(w1, w2)


def calculate_diff(allowed_vs_banned):
    if allowed_vs_banned[0] < allowed_vs_banned[1]:
        return False
    else:
        diff = ((allowed_vs_banned[0] - allowed_vs_banned[1]) / allowed_vs_banned[1]) * 100.0
        if diff > 35:
            return True
        else:
            return False


if __name__ == '__main__':
    test_similarity_manually()

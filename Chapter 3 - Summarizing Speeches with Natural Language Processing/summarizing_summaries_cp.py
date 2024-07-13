"""
Program that uses summary program from dream_summary.py and summarizes articles that are already considered summaries.
Will do this on the Wikipedia page for gensim. Then transfer bed_summary.py program to summarize a Apple service
agreement [although I will not read it to see if it's right, maybe someone will].
"""
from collections import Counter
import re
import requests
import bs4
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
# Make sure to install gensim version < 4.0 summarize was removed in all later versions
from gensim.summarization import summarize


# Create a method that loads in the webpage and returns the speech
def get_speech(url_text):
    url = url_text
    page = requests.get(url)
    page.raise_for_status()
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    # Get text of speech for each paragraph
    p_elems = [element.text for element in soup.find_all('p')]

    # Combine paragraphs into speech text
    speech = ' '.join(p_elems)
    return speech

# Define bed_summ)_, scraping web and preparing speech string
def bed_summ(url_text, title):
    # Get the speech from the URL
    speech = get_speech(url_text)

    # Step 2 - Summarizing the speech
    print('\nSummary of %s speech:' % title)
    # Set length of summary to 255 words
    summary = summarize(speech, word_count=255)
    sentences = sent_tokenize(summary)
    # Remove all duplicate sentences
    sents = set(sentences)
    # Since sets are unordered, this program rarely outputs the same results twice but overall summarizes the speech
    print(' '.join(sents))


# Define dream_summ() function to scrape webpage and assign speech to a var as a string
def dream_summ(text_url):
    # Get the speech from the URL
    speech = get_speech(text_url)

    # Complete the dream_summ() function
    # Replace all extra white spaces with just 1 white space [\s+] = runs of whitespace
    speech = re.sub('\s+', ' ', speech)
    # Remove anything that is not a letter
    speech_edit = re.sub('[^a-zA-Z]', ' ', speech)
    # Call the method to remove extra whitespaces since punctuation just got replaced by spaces
    speech_edit = re.sub('\s+', ' ', speech_edit)

    while True:
        # Get user input for max words per sentences and max number of sentences for summary
        max_words = input('Enter max words per sentence for summary: ')
        num_sents = input('Enter number of sentences for summary: ')
        # If correct input format was entered then exit while loop else continue
        if max_words.isdigit() and num_sents.isdigit():
            break
        else:
            print('\nInput must be in whole numbers.\n')

    # Clean text by removing stop words
    speech_edit_no_stop = remove_stop_words(speech_edit)
    # Calculate frequency of words in text
    word_freq = get_word_freq(speech_edit_no_stop)
    # Score sentences based on the word frequency calculation
    sent_scores = score_sentences(speech, word_freq, max_words)

    # Use the Counter method to rank the sentences returned
    counts = Counter(sent_scores)
    summary = counts.most_common(int(num_sents))
    print('\nSUMMARY:')
    for i in summary:
        # Sentence is at index 0 and rank is at index 1
        print(i[0])


# Removing stop words
def remove_stop_words(speech_edit):
    """Remove stop words from string and return string"""
    # Get list of stopwords
    stop_words = set(stopwords.words('english'))
    speech_edit_no_stop = ''
    for word in nltk.word_tokenize(speech_edit):
        if word.lower() not in stop_words:
            # Add word to speech if it is not a stop word
            speech_edit_no_stop += word + ' '
    return speech_edit_no_stop


# Calculating the frequency of occurrence of words
def get_word_freq(speech_edit_no_stop):
    """Return a dictionary of word frequency in a string"""
    # Call lower while calling word_tokenize() so that the original version of speech can remain for summary
    word_freq = nltk.FreqDist(nltk.word_tokenize(speech_edit_no_stop.lower()))
    return word_freq


# Scoring sentences
def score_sentences(speech, word_freq, max_words):
    """Return dictionary of sentence scores based on word frequency"""
    sent_scores = dict()
    # Tokenize speech into sentences
    sentences = nltk.sent_tokenize(speech)
    for sent in sentences:
        # Keep track of the score for each sentence, start by setting it to 0
        sent_scores[sent] = 0
        # Tokenize sentences into words
        words = nltk.word_tokenize(sent.lower())
        sent_word_count = len(words)
        # Do not add score to sentence if it does not qualify based on max words per sentence
        if sent_word_count <= int(max_words):
            for word in words:
                if word in word_freq.keys():
                    sent_scores[sent] += word_freq[word]
            # Normalize the scores so the method does not bias longer sentences over shorter ones
            sent_scores[sent] = sent_scores[sent] / sent_word_count
    return sent_scores


def main():
    # Summarize the Gensim Wikipedia article
    dream_summ('https://en.wikipedia.org/wiki/Gensim')
    # Summarize the Apple's service agreement
    bed_summ('https://www.apple.com/legal/internet-services/itunes/', 'Apple Service Agreement')


if __name__ == '__main__':
    main()

"""
Text summarization program that displays most important sentences in their original order of appearance. Basically same
program as dream_summary.py but ensure that the order of the speech is maintained. See if output is better than that from
dream_summary.py.
"""
from collections import Counter
import re
import requests
import bs4
import nltk
from nltk.corpus import stopwords


# Define main() function to scrape webpage and assign speech to a var as a string
def main(text_url):
    # URL of MLK's speech
    url = text_url
    page = requests.get(url)
    # Check if download is successful
    page.raise_for_status()
    # Create a beautiful soup object, remove the HTML tags from page.text
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    # Get just the content (paragraphs) of the speech from the soup object
    p_elems = [element.text for element in soup.find_all('p')]

    # Join all the paragraphs together to get the content of the speech
    speech = ' '.join(p_elems)

    # Complete the main() function
    # First replace typo in the speech
    speech = speech.replace(')mowing', 'knowing')
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
    # Here is where the program changes
    # To keep the original order of the program go through the whole speech
    for sent in sent_scores:
        # Then loop through each sentence in summary (only top 5)
        for i in summary:
            # If the sentence is in the summary (top 5 importance) print it, keeping the original order
            if sent in i[0]:
                print(sent)


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


if __name__ == '__main__':
    main('http://www.analytictech.com/mb021/mlk.htm')

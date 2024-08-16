"""
Program that summarizes the Doyle's 'The Hounds of the Baskervilles' by chapter. Book can be found at the url:
http://www.gutenberg.org/files/2852/2852-h/2852-h.htm. Keep the summaries of the chapters short [~75 words].
"""
from collections import Counter
import re
import requests
import bs4
import nltk
from nltk.corpus import stopwords


# Define main() function to scrape webpage and assign text to a var as a string
def main(text_url):
    # URL of book
    url = text_url
    page = requests.get(url)
    # Check if download is successful
    page.raise_for_status()
    # Create a beautiful soup object, remove the HTML tags from page.text
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    # Get just the content (paragraphs) of the speech from the soup object
    chapter_elems = soup.select('div[class="chapter"]')
    chapters = chapter_elems[2:]
    # Use count to keep track of each chapter
    count = 1
    for chapter in chapters:
        text = [p_tag.get_text() for p_tag in chapter.find_all('p')]
        text = ' '.join(text)
        # Complete the main() function
        # Replace all extra white spaces with just 1 white space [\s+] = runs of whitespace
        text = re.sub('\s+', ' ', text)
        # Remove anything that is not a letter
        speech_edit = re.sub('[^a-zA-Z]', ' ', text)
        # Call the method to remove extra whitespaces since punctuation just got replaced by spaces
        speech_edit = re.sub('\s+', ' ', speech_edit)
        # will automatically set max words to be 25 and num_sentences to be 5
        max_words = 25
        num_sents = 5

        # Clean text by removing stop words
        speech_edit_no_stop = remove_stop_words(speech_edit)
        # Calculate frequency of words in text
        word_freq = get_word_freq(speech_edit_no_stop)
        # Score sentences based on the word frequency calculation
        sent_scores = score_sentences(text, word_freq, max_words)

        # Use the Counter method to rank the sentences returned
        counts = Counter(sent_scores)
        summary = counts.most_common(int(num_sents))
        print('\nCHAPTER %d SUMMARY:' % count)
        count += 1
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


if __name__ == '__main__':
    # Link to the Hounds of the Baskervilles'
    main('http://www.gutenberg.org/files/2852/2852-h/2852-h.htm')

"""
Program that uses gensim module to summarize Admiral William H. McRaven's 'Make Your Bed' speech.
"""
import requests
import bs4
from nltk.tokenize import sent_tokenize
# Make sure to install gensim version < 4.0 summarize was removed in all later versions
from gensim.summarization import summarize


# Step 1 define main, scraping web and preparing speech string
def main(url_text, title):
    url = url_text
    page = requests.get(url)
    page.raise_for_status()
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    # Get text of speech for each paragraph
    p_elems = [element.text for element in soup.find_all('p')]

    # Combine paragraphs into speech text
    speech = ' '.join(p_elems)

    # Step 2 - Summarizing the speech
    print('\nSummary of %s speech:' % title)
    # Set length of summary to 255 words
    summary = summarize(speech, word_count=255)
    sentences = sent_tokenize(summary)
    # Remove all duplicate sentences
    sents = set(sentences)
    # Since sets are unordered, this program rarely outputs the same results twice but overall summarizes the speech
    print(' '.join(sents))


if __name__ == '__main__':
    main('https://jamesclear.com/great-speeches/make-your-bed-by-admiral-william-h-mcraven', 'Make Your Bed')

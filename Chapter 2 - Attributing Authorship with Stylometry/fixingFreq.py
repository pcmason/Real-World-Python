"""
Challenge Project 3:
    Define new version of nltk.FreqDist() method that uses percentages rather than counts and use it to make the charts
    from stylometry.py. Help can be found at
    https://martinapugliese.github.io/plotting-the-actual-frequencies-in-a-FreqDist-in-nltk/
"""

import nltk
from nltk import punkt
from nltk.corpus import stopwords
import matplotlib.pyplot as plt

# Line style for plots
LINES = ['-', ':', '--']


# Part 2 - Loading text and building a word dictionary
def text_to_string(filename):
    """Read a text file and return a string"""
    # Use with to open the file so that it closes automatically regardless of termination
    with open(filename, encoding='utf-8', errors='ignore') as infile:
        # read() returns whole file as an individual string
        return infile.read()


def make_word_dict(strings_by_author):
    """Return dict of tokenized words by corpus by author"""
    words_by_author = dict()
    for author in strings_by_author:
        # Create list of tokens that serves as dict value for each author
        tokens = nltk.word_tokenize(strings_by_author[author])
        # Filter out numbers, punctuation, hyphenated words or names, also makes all words lowercase
        words_by_author[author] = ([token.lower() for token in tokens if token.isalpha()])
    return words_by_author


# Part 3 - Finding the shortest corpus
def find_shortest_corpus(words_by_author):
    """Return length of the shortest corpus"""
    word_count = []
    for author in words_by_author:
        # Append word count of each text and output for each
        word_count.append(len(words_by_author[author]))
        print('\nNumber of words for {} = {}\n'.
              format(author, len(words_by_author[author])))
    len_shortest_corpus = min(word_count)
    print('Length shortest corpus = {}\n'.format(len_shortest_corpus))
    return len_shortest_corpus


# Challenge Code - Add method that changes the FreqDist output to a ratio instead of count
def conv_out_count_to_ratio(fd):
    total = fd.N()
    for word in fd:
        fd[word] /= float(total)
    return fd


# Part 4 - Comparing word lengths
def word_length_test(words_by_author, len_shortest_corpus):
    """Plot word length freq by author, truncated to shortest corpus length"""
    by_author_length_freq_dist = dict()
    plt.figure(1)

    # Loop through authors in tokenized dictionary using i to create different line styles for each
    for i, author in enumerate(words_by_author):
        # Create list where each word is replaced by int representing the words length
        word_lengths = [len(word) for word in words_by_author[author][:len_shortest_corpus]]
        # Create data object of word frequency info that can be plotted
        by_author_length_freq_dist[author] = nltk.FreqDist(word_lengths)
        # Convert output for graph from count to ratio
        by_author_length_freq_dist[author] = conv_out_count_to_ratio(by_author_length_freq_dist[author])
        # Can plot graph directly without using plt, plot most frequently occuring sample first, then the next 15
        by_author_length_freq_dist[author].plot(15,
                                                linestyle=LINES[i],
                                                label=author,
                                                title='Word Length',
                                                show=False)
    plt.legend()
    # Need to change ylabel from count to an appropriate title
    plt.ylabel('Ratio')
    plt.show()


# Part 5 - Comparing stop words
def stopwords_test(words_by_author, len_shortest_corpus):
    """Plot stopwords freq by author, truncated to shortest corpus length"""
    stopwords_by_author_freq_dist = dict()
    plt.figure(2)
    # Get the stop words from nltk
    stop_words = set(stopwords.words('english'))  # Use set for speed
    #print('Number of stopwords = {}\n'.format(len(stop_words)))
    #print('Stopwords = {}\n'.format(stop_words))

    for i, author in enumerate(words_by_author):
        # Get all stopwords for each author's work
        stopwords_by_author = [word for word in words_by_author[author]
                               [:len_shortest_corpus] if word in stop_words]
        stopwords_by_author_freq_dist[author] = nltk.FreqDist(stopwords_by_author)
        # Convert graph output to ratio from count
        stopwords_by_author_freq_dist[author] = conv_out_count_to_ratio(stopwords_by_author_freq_dist[author])
        # Plot the top 50 stop words used for each author
        stopwords_by_author_freq_dist[author].plot(50,
                                                   label=author,
                                                   linestyle=LINES[i],
                                                   title='50 Most Common Stopwords',
                                                   show=False)
    plt.legend()
    plt.ylabel('Ratio')
    plt.show()


# Part 6 - Comparing parts of speech
def parts_of_speech_test(words_by_author, len_shortest_corpus):
    """Plot author use of parts-of-speech sudch as nouns, verbs, adverbs, etc"""
    by_author_pos_freq_dist = dict()
    plt.figure(3)
    for i, author in enumerate(words_by_author):
        # This replaces all words in the author's corpus into the corresponding POS tag
        pos_by_author = [pos[1] for pos in nltk.pos_tag(words_by_author[author]
                                                        [:len_shortest_corpus])]
        by_author_pos_freq_dist[author] = nltk.FreqDist(pos_by_author)
        # Convert graph output to ratio
        by_author_pos_freq_dist[author] = conv_out_count_to_ratio(by_author_pos_freq_dist[author])
        by_author_pos_freq_dist[author].plot(35,
                                             label=author,
                                             linestyle=LINES[i],
                                             title='Part of Speech',
                                             show=False)
    plt.legend()
    plt.ylabel('Ratio')
    plt.show()


# Part 7 - Comparing author vocabularies
def vocab_test(words_by_author):
    """Compare author vocabularies using the chi-squared statistical test"""
    chisquared_by_author = dict()
    for author in words_by_author:
        # Join each author's work with the unknown work, don't combine unknown with itself
        if author != 'unknown':
            combined_corpus = (words_by_author[author] + words_by_author['unknown'])
            author_proportion = (len(words_by_author[author]) / len(combined_corpus))
            combined_freq_dist = nltk.FreqDist(combined_corpus)
            # Get list of 1000 most common words in the combined text
            most_common_words = list(combined_freq_dist.most_common(1000))
            chisquared = 0
            # Loop through most common words list [('the', 7778), ...]
            for word, combined_count in most_common_words:
                # Get the observed count
                observed_count_author = words_by_author[author].count(word)
                # Get the expected count of the word
                expected_count_author = combined_count * author_proportion
                # Use these values to update the chi-squared value and add it to the dictionary for each author
                chisquared += ((observed_count_author - expected_count_author)**2 / expected_count_author)
                chisquared_by_author[author] = chisquared
            # Display result for each author
            print('Chi-squared for {} = {:.1f}'.format(author, chisquared))
    # Use the chisquared value to determine who authored the book based on vocabulary
    # Use built-in get method to use the key as min will look at the dict keys by default instead of the values
    most_likely_author = min(chisquared_by_author, key=chisquared_by_author.get)
    print('Most-likely author by vocabulary is {}\n'.format(most_likely_author))


# Part 8 - Calculating Jaccard similarity
def jaccard_test(words_by_author, len_shortest_corpus):
    """Calculate Jaccard similarity of each known corpus to unknown corpus"""
    jaccard_by_author = dict()
    # Use set to remove duplicate words
    unique_words_unknown = set(words_by_author['unknown'][:len_shortest_corpus])
    # Get the list of authors without unknown using a generator expression
    authors = (author for author in words_by_author if author != 'unknown')
    for author in authors:
        unique_words_author = set(words_by_author[author][:len_shortest_corpus])
        shared_words = unique_words_author.intersection(unique_words_unknown)
        # Calculate jaccard similarity [area of overlap / area of union]
        jaccard_sim = (float(len(shared_words)) / (len(unique_words_author)
                       + len(unique_words_unknown) - len(shared_words)))
        jaccard_by_author[author] = jaccard_sim
        print('Jaccard Similarity for {} = {}'.format(author, jaccard_sim))
    # Get the author that has the most in common with the unknown author and output the result
    most_likely_author = max(jaccard_by_author, key=jaccard_by_author.get)
    print('Most-likely author by similarity is {}'.format(most_likely_author))


# Part 1 - Define the main() function
def main():
    # Initialize dictionary to hold the text for each author
    strings_by_author = dict()
    strings_by_author['doyle'] = text_to_string('hound.txt')
    strings_by_author['wells'] = text_to_string('war.txt')
    strings_by_author['unknown'] = text_to_string('lost.txt')

    # Print first 300 lines of Hounds of the Baskervilles
    #print(strings_by_author['doyle'][:300])

    # Take strings_by_author dict, split the words in the strings and return a dict with the authors as keys and a
    # list of words as values
    words_by_author = make_word_dict(strings_by_author)
    # Truncate the works by the size of the shortest text so that they all have the same number of words
    len_shortest_corpus = find_shortest_corpus(words_by_author)
    # Next five methods perform the stylometric analysis [all defined above]
    word_length_test(words_by_author, len_shortest_corpus)
    stopwords_test(words_by_author, len_shortest_corpus)
    parts_of_speech_test(words_by_author, len_shortest_corpus)
    vocab_test(words_by_author)
    jaccard_test(words_by_author, len_shortest_corpus)


if __name__ == '__main__':
    main()


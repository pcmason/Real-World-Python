"""
Practice Project 1:
    Program that takes the hounds.txt file and outputs a dispersion plot for all the major characters. A dispersion plot
    outputs a line for each time a character is mentioned and for this scenario shows how those characters interact with
    each other as the story unfolds
"""
import nltk
import matplotlib.pyplot as plt
import stylometry


# Have to update this method from stylometry to return a list instead of a dict
def make_word_list(strings_by_author):
    """Return dict of tokenized words by corpus by author"""
    words_by_author = dict()
    # Create list of tokens that serves as dict value for each author
    tokens = nltk.word_tokenize(strings_by_author)
    # Filter out numbers, punctuation, hyphenated words or names, also makes all words lowercase
    words_by_author = ([token for token in tokens if token.isalpha()])
    return words_by_author


if __name__ == '__main__':
    # First load in the hounds.txt file as a string
    string_hounds = stylometry.text_to_string('hound.txt')
    # Now get a list of the words from hounds.txt
    words_hound = make_word_list(string_hounds)
    # Create the list of proper names
    char_names = ['Holmes', 'Watson', 'Mortimer', 'Henry', 'Barrymore', 'Stapleton', 'Selden', 'hound']
    # Use the disperion_plot from nltk.draw
    ax = nltk.draw.dispersion_plot(words_hound, char_names)
    # Since the y labels are reversed, here is a quick fix
    ax.set_yticks(list(range(len(char_names))), reversed(char_names), color="C0")
    plt.show()


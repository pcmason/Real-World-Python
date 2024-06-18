"""
Practice Project 2:
    Tokenize the 3 novels solely on punctuation. Focus on the use of semicolons. For each author plot a heatmap that
    displays semicolons as blue and all other marks as yellow or red. See if the results favor Doyle or Wells as the
    author.
"""
import string
import seaborn as sns
import nltk
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import stylometry
import numpy as np
import math


# Change make word list to only return the punctuation marks for each author's work
def make_punct_dict(strings_by_author):
    """Return dict of tokenized words by corpus by author"""
    words_by_author = dict()
    for author in strings_by_author:
        # Create list of tokens that serves as dict value for each author
        tokens = nltk.word_tokenize(strings_by_author[author])
        # Filter out numbers, punctuation, hyphenated words or names, also makes all words lowercase
        words_by_author[author] = ([token for token in tokens if token in string.punctuation])
    return words_by_author


# Create method to convert list of punctuation marks to numerical values for the heatmap
def convert_punct_to_num(punct_by_author, author):
    """Return list of punctuation marks where semicolons are 1 and all other puncts are 2"""
    heat_vals = []
    for char in punct_by_author[author]:
        if char == ';':
            value = 1
        else:
            value = 2
        heat_vals.append(value)
    return heat_vals


# Method that outputs the heat map for the punctuation
def punct_heatmap(punct_by_author):
    """So I believe that I should just be able to loop through punct_by_author authors and output heatmap with imshow()
    """
    for author in punct_by_author:
        # Convert punct list to ints
        heat = convert_punct_to_num(punct_by_author, author)
        # Trim to largest size for square array [honestly dont' get this]
        arr = np.array((heat[:6561]))
        arr_reshaped = arr.reshape(int(math.sqrt(len(arr))), int(math.sqrt(len(arr))))
        # Now plot the heat map for each author
        fig, ax = plt.subplots(figure=(7, 7))
        sns.heatmap(arr_reshaped,
                    cmap=ListedColormap(['blue', 'red']),
                    square=True,
                    ax=ax)
        ax.set_title('Heatmap Semicolons {}'.format(author))
    plt.show()


# Define the main() function
def main():
    # Initialize dictionary to hold the text for each author
    strings_by_author = dict()
    strings_by_author['doyle'] = stylometry.text_to_string('hound.txt')
    strings_by_author['wells'] = stylometry.text_to_string('war.txt')
    strings_by_author['unknown'] = stylometry.text_to_string('lost.txt')

    # Get the punctuation for each author in string_by_author
    punct_by_author = make_punct_dict(strings_by_author)
    # Let's see if the punct_heatmap method works
    punct_heatmap(punct_by_author)


if __name__ == '__main__':
    main()

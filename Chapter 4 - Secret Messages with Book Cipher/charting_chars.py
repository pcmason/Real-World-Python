"""
This program takes the char_dict from rebecca.py and outputs the frequency of each unique char in The Lost World as a
bar graph using matplotlib.
"""
# Import modules & define main()
import matplotlib.pyplot as plt
from collections import defaultdict, Counter


def main():
    # Set dataset
    infile = 'lost.txt'

    # Load in file and create char_dict from text
    text = load_file(infile)
    char_dict = make_dict(text)

    # Create empty list to hold count for each character
    char_count = []
    # Loop through values of the dict and append len to char_count
    for y in char_dict.values():
        char_count.append(len(y))
    # Create a new dict where the key is the keys from char_dict and values are char_count
    new_char_dict = dict(zip(char_dict.keys(), char_count))
    # Sort the dictionary so that the graph looks good, sorted returns list so wrap with dict
    new_char_dict = dict(sorted(new_char_dict.items(), key=lambda x: x[1], reverse=True))

    # Plot the frequency of the char_dict
    plt.bar(new_char_dict.keys(), new_char_dict.values())
    plt.title("Frequency of Occurrence of Characters in 'The Lost World'")
    plt.savefig('Frequency_chars_lost_world')
    plt.show()


# Loading a file and making a dictionary
def load_file(infile):
    """Read and return text file as string of lowercase letters"""
    with open(infile, encoding='utf-8', errors='ignore') as f:
        loaded_string = f.read().lower()
    return loaded_string


# Take string value as argument and return a new dictionary
def make_dict(text):
    """Return dictionary of chars and their indexes"""
    char_dict = defaultdict(list)
    for index, char in enumerate(text):
        char_dict[char].append(index)
    return char_dict


if __name__ == '__main__':
    main()

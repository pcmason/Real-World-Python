"""
Program extends rebecca.py to use words rather than letters. Since a lot of words do not appear in The Lost World, will
need to use 'first letter mode' to handle those words. This involves using only the first letter of each word between
flags. The start flag will be 'a a' and the end flag will be 'the the'. 
"""

# Part 1 - import modules & define main()
import sys
import os
import random
from collections import defaultdict, Counter


def main():
    # Prompt user for message to encrypt or decrypt
    message = input("Enter plaintext or ciphertext: ")
    process = input("Enter 'encrypt' or 'decrypt': ")
    while process not in ('encrypt', 'decrypt'):
        process = input("Invalid process. Enter 'encrypt' or 'decrypt': ")
    shift = int(input("Shift value (1-366) = "))
    while not 1 <= shift <= 366:
        shift = int(input("Invalid value. Enter digit from 1-366: "))
    # This will be 'lost.txt' for this file
    infile = input("Enter filename with extension: ")

    # Ensure file exists then load it in
    if not os.path.exists(infile):
        print("File {} not found. Terminating.".format(infile), file=sys.stderr)
        sys.exit(1)
    text = load_file(infile)
    char_text = load_str_file(infile)
    #print(text[:20])
    word_dict = make_dict(text, shift)
    char_dict = make_dict(char_text, shift)
    #print(word_dict) # This is where I left off

    # Specific actions to encrypt message
    if process == 'encrypt':
        char_decrypted = []
        word_decypted = []
        encrypted = []
        #decrypted = []
        message_words = message.split(' ')
        temp_word_holder = []

        # If the message contains 'a a' then it uses char dict for cipher
        count = message.count('a a')
        # Check if the pattern appears more than once
        if count > 0:
            for x in range(count):
                # Get the index of the important words
                i = message_words.index('a')
                k = message_words.index('the')
                # Actual start of the message
                j = i + 2
                cut_message = message_words[j:k]
                char_list = []
                # Get the first letter of each word
                for word in cut_message:
                    first_letter = word[0]
                    char_list.append(first_letter)
                # Encrypt the characters
                cipher = encrypt_chars(char_list, char_dict)
                encrypted.append(cipher)
                # Now these conditionals are dependent on where the words would be found for the message and how they should be appended
                if x % 2 == 0:
                    message_words = message_words[k+2:]
                    # If there are no more characters to be encrypted, then append the words
                    if count % 2 != 0:
                        temp_word_holder.append(message_words)
                else:
                    # Else, there are more words to be appended after the last characters
                    message_words = message_words[:i]
                    temp_word_holder.append(message_words)
                # Use temp_list for decryption so that the whole message can be output together at the end
                temp_list = []
                for i in cipher:
                    temp_list.append(char_text[i-shift])
                char_decrypted.append(temp_list)

        # Unsure why temp_word_holder is a list of lists, easy solution for that is to add [0]
        message = ' '.join(temp_word_holder[0])
        ciphertext = encrypt(message, word_dict)
        for cipher in ciphertext:
            encrypted.append(cipher)
        # If a key was duplicated, the encryption failed and the user has to try again
        if check_for_fail(ciphertext):
            print("\nProblem finding unique keys.", file=sys.stderr)
            print("Try again, change messsage, or change code book.\n", file=sys.stderr)
            sys.exit()

        print("encrypted ciphertext = \n {}\n".format(encrypted))
        print("decrypted plaintext = ")

        # Here get the words in a list, same logic as chars so they can be output in order
        temp_list = []
        for i in ciphertext:
            appended_word = text[i - shift]
            temp_list.append(appended_word)
            temp_list.append(' ')
        word_decypted.append(temp_list)

        # Print decrypted plaintext as check to ensure encryption worked
        for i in range(len(char_decrypted)-1):
            print(char_decrypted[i])
            print(word_decypted[i])
            print(char_decrypted[i+1])

    # Actions for encryption
    elif process == 'decrypt':
        plaintext = decrypt(message, text, shift)
        print("\ndecrypted plaintext = \n {}\n".format(plaintext))


# Loading a file and making a dictionary
def load_file(infile):
    """Read and return text file as string of lowercase letters"""
    with open(infile, encoding='utf-8', errors='ignore') as f:
        # This is changed to load in the text file as a list of words instaed of chars
        words = [word.lower() for line in f for word in line.split()]
        words_no_punct = ["".join(char for char in word if char.isalpha()) for word in words]
    return words_no_punct


# Load the file as a string
def load_str_file(infile):
    """Read and return text file as string of lowercase letters"""
    with open(infile, encoding='utf-8', errors='ignore') as f:
        loaded_string = f.read().lower()
    return loaded_string


# Take string and shift values as arguments and return a new dictionary
def make_dict(text, shift):
    """Return dictionary of chars and shifted indexes"""
    word_dict = defaultdict(list)
    for index, word in enumerate(text):
        # By adding shift, ensure that indexes will be unique for each message
        word_dict[word].append(index + shift)
    return word_dict


# Encrypting the message
def encrypt(message, word_dict):
    """Return list of indexes representing chars in a message"""
    encrypted = []
    message_words = message.split(' ')
    for word in message_words:
        print(word)
        # If there are > 1 indexes associated with char, will randomly choose one of the indexes
        if len(word_dict[word]) > 1:
            index = random.choice(word_dict[word])
        elif len(word_dict[word]) == 1:  # Random.choice fails if only 1 choice
            index = word_dict[word][0]
        # Conditional for if char does not appear in 'lost.txt' alerting user and continuing
        elif len(word_dict[word]) == 0:
            print("\nWord {} not in dictionary.".format(word), file=sys.stderr)
            continue
        encrypted.append(index)
    return encrypted


# Encrypting the message
def encrypt_chars(message, char_dict):
    """Return list of indexes representing chars in a message"""
    encrypted = []
    for char in message:
        # If there are > 1 indexes associated with char, will randomly choose one of the indexes
        if len(char_dict[char]) > 1:
            index = random.choice(char_dict[char])
        elif len(char_dict[char]) == 1:  # Random.choice fails if only 1 choice
            index = char_dict[char][0]
        # Conditional for if char does not appear in 'lost.txt' alerting user and continuing
        elif len(char_dict[char]) == 0:
            print("\nCharacter {} not in dictionary.".format(char), file=sys.stderr)
            continue
        encrypted.append(index)
    return encrypted


# Part 4 - Decrypting the message
def decrypt(message, text, shift):
    """Decrypt ciphertext list and return plaintext string"""
    plaintext = ''
    # Remove non digit chars, stringed together using dot notation
    indexes = [s.replace(',', ' ').replace('[', ' ').replace(']', ' ') for s in message.split()]
    for i in indexes:
        plaintext += text[int(i) - shift] + ' '
    return plaintext


# checking for failure and calling main()
def check_for_fail(ciphertext):
    """Return True if ciphertext contains any duplicate keys"""
    # Here create list of all the keys that occur more than once from dict used to make the ciphertext
    check = [k for k, v in Counter(ciphertext).items() if v > 1]
    if len(check) > 0:
        return True


if __name__ == '__main__':
    main()

"""
Thought process of solving this:
* Figure out what is going on with the word_dict and if that can be used to encrypt message with words that definitely appeard in the book. [DONE]
* Then use the char dict to be able to identify words that are not in The Lost World using the char_dict message from the original program [DONE[
* Should then encrypt a message 'sidi muftah with ten tanks' as 'a a so if do in my under for to all he the the with ten a a tell all night kind so the the' [DONE]
    * where 'a a' is the start of the char method and 'the the' signals the end
    
    
The biggest issue currently is that the for loop using i to index through the array values does not work super well. This can be improved to use the string.contains() method instead of checking if 
'a' is followed by 'a'. [DONE] (maybe could be better though???)

Now the only issue is that the middle part of the message (the words) is being ignored to do the letter part. Need to do the letter part, then do words then back to letters [DONE] (also could be better though!!)

Will be posting onto Github on 10/16/24 I have a solution that works, but is not the best. I will examine the book 
solution and update accordingly if the urge comes, but overall I am okay with my solution as it can encrypt somewhat
complex messages at the moment. Decryption is currently off the table though which is a problem and would not be ideal 
for the solution in most settings. 
"""


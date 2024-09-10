"""
Program that uses The Lost World novel as a cipher for sharing secret messages. Will take either an encrypted or
plaintext file and return a plaintext or encrypted file.
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
    char_dict = make_dict(text, shift)

    # Specific actions to encrypt message
    if process == 'encrypt':
        ciphertext = encrypt(message, char_dict)
        # If a key was duplicated, the encryption failed and the user has to try again
        if check_for_fail(ciphertext):
            print("\nProblem finding unique keys.", file=sys.stderr)
            print("Try again, change messsage, or change code book.\n", file=sys.stderr)
            sys.exit()
        # Print contents of char_dict to see how many times various chars occur, help guide what can be in messages
        print("\nCharacter and number of occurrences in char_dict: \n")
        print("{: >10}{: >10}{: >10}".format('Character', 'Unicode', 'Count'))
        for key in sorted(char_dict.keys()):
            print("{:>10}{:>10}{:>10}".format(repr(key)[1:-1],
                                              str(ord(key)),
                                              len(char_dict[key])))
        print("\nNumber of distinct characters: {}".format(len(char_dict)))
        print("Total number of characters: {:,}\n".format(len(text)))

        print("encrypted ciphertext = \n {}\n".format(ciphertext))
        print("decrypted plaintext = ")

        # Print decrypted plaintext as check to ensure encryption worked
        for i in ciphertext:
            print(text[i - shift], end='', flush=True)

    # Actions for encryption
    elif process == 'decrypt':
        plaintext = decrypt(message, text, shift)
        print("\ndecrypted plaintext = \n {}\n".format(plaintext))


# Part 2 - Loading a file and making a dictionary
def load_file(infile):
    """Read and return text file as string of lowercase letters"""
    with open(infile, encoding='utf-8', errors='ignore') as f:
        loaded_string = f.read().lower()
    return loaded_string


# Take string and shift values as arguments and return a new dictionary
def make_dict(text, shift):
    """Return dictionary of chars and shifted indexes"""
    char_dict = defaultdict(list)
    for index, char in enumerate(text):
        # By adding shift, ensure that indexes will be unique for each message
        char_dict[char].append(index + shift)
    return char_dict


# Part 3 - Encrypting the message
def encrypt(message, char_dict):
    """Return list of indexes representing chars in a message"""
    encrypted = []
    for char in message.lower():
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
        plaintext += text[int(i) - shift]
    return plaintext


# Part 5 - checking for failure and calling main()
def check_for_fail(ciphertext):
    """Return True if ciphertext contains any duplicate keys"""
    # Here create list of all the keys that occur more than once from dict used to make the ciphertext
    check = [k for k, v in Counter(ciphertext).items() if v > 1]
    if len(check) > 0:
        return True


if __name__ == '__main__':
    main()

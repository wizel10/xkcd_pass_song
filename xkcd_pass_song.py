#!/usr/bin/env python
# encoding: utf-8

import unidecode
import random
import os
import os.path
import argparse
import re
import math
import sys

# Python 3 compatibility
if sys.version_info[0] >= 3:
    raw_input = input
    xrange = range

# random.SystemRandom() should be cryptographically secure
try:
    rng = random.SystemRandom
except AttributeError as ex:
    sys.stderr.write("WARNING: System does not support cryptographically "
                     "secure random number generator or you are using Python "
                     "version < 2.4.\n")
    rng = random.Random


# locate in directory: ./xkcdpass/static
DEFAULT_WORDFILE = "spa-song-1"
MIN_LENGTH = 4
MAX_LENGTH = 9
NUM_WORDS = 4


def locate_wordfile(wordfile=None):
    """
    Locate a wordfile from provided name/path. Return a path to wordfile
    or use a default.
    """
    # clean/initialyzes source files
    common_word_file = ''
    # ensures the directory exist and adds full path
    static_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'songs')
    # print(static_dir)

    # if no file is given, use default, otherwise use provided
    if wordfile is None:
        # wordfile can be in static dir or provided as a complete path
        common_word_file = os.path.join(static_dir, DEFAULT_WORDFILE)
    else:
        common_word_file = os.path.join(static_dir, wordfile)

    print('Source file: %s' % (common_word_file))
    return common_word_file


def generate_wordlist(wordfile):
    """
    Generate a word list from a lyrics wordfile
    """

    words_list = []

    # read lines from file into wordlist
    # need the encoding to read the accented characters
    with open(wordfile, 'r', encoding='utf-8') as wlf:
        for line in wlf:
            # The method strip() returns a copy of the string
            # in which all chars have been stripped from the beginning
            # and the end of the string (default whitespace characters).
            thisline = line.strip()
            # thisline is of type 'unicode' need to unidecode (remove accents, ...)
            unaccented_thisline = unidecode.unidecode(thisline)
            # print(thisline, '-->', unaccented_thisline)
            words_list.extend(unaccented_thisline.split())
            # print(words_list)
    return list(set(words_list))  # deduplicate, just in case. "set" removes duplicates

def generate_validlist(wordlist, minlength):
    valid_list = []
    valid_list = [ word for word in wordlist if len(word) >= minlength ]
    return(valid_list)

def choose_words(wordlist, numwords):
    """
    Choose numwords randomly from wordlist
    """

    return [rng().choice(wordlist) for i in xrange(numwords)]

def main():
    """ Mainline code for this program. """

    my_wordfile = locate_wordfile(wordfile=DEFAULT_WORDFILE)
    my_wordlist = generate_wordlist(my_wordfile)
    # print(my_wordlist)
    my_validlist = generate_validlist(my_wordlist, minlength=MIN_LENGTH)
    # print(my_validlist)
    print("Your word list contains {0} words." .format(len(my_validlist)))
    my_password = choose_words(my_validlist, numwords=NUM_WORDS)
    print(my_password)

if __name__=='__main__':
    main()

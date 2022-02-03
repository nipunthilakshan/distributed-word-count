#!/usr/bin/env python

# Read and write data to STDIN and STDOUT.
import sys

# Read entire line from STDIN (standard input).
for line in sys.stdin:
    # Remove leading and trailing whitespace.
    line = line.strip()
    # Split the line into words.
    words = line.split()

    # Loop over the words array and printing the word with the count of 1 to the STDOUT
    for word in words:
        # Write the results to STDOUT,
        # what we output here will be the input for the
        # reduce step, i.e. the input for reducer.py
        value = 1
        print('{0}\t{1}'.format(word, value))

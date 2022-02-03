#!/usr/bin/env python

import sys

current_word = None
current_count = 0
word = None

# Read the entire line from STDIN.
for line in sys.stdin:
    # Remove leading and trailing whitespace.
    line = line.strip()
    # Splitting the data on the basis of tab we have provided in mapper.py.
    word, count = line.split("\t", 1)
    # Convert count (currently a string) to int.
    try:
        count = int(count)
    except ValueError:
        # Count was not a number, so silently ignore/discard this line
        continue

    # This IF-switch only works because Hadoop sorts map output
    # by key (here: word) before it is passed to the reducer
    if current_word == word:
        current_count += count
    else:
        if current_word:
            # Write result to STDOUT
            print("{0}\t{1}".format(current_word, current_count))
        current_count = count
        current_word = word

# Output the last word if needed!
if current_word == word:
    print("{0}\t{1}".format(current_word, current_count))

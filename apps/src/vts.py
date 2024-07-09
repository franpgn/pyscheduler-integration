import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
sys.path.append(project_root)

from apps.src.disassemble import disassemble

def VTS():
    word1 = 'amor'
    word2 = 'roma'
    # Initialize two dictionaries to count the frequency of each letter
    count1 = {}
    count2 = {}

    # Count the frequency of each letter in the first word
    for letter in word1:
        if letter in count1:
            count1[letter] += 1
        else:
            count1[letter] = 1

    # Count the frequency of each letter in the second word
    for letter in word2:
        if letter in count2:
            count2[letter] += 1
        else:
            count2[letter] = 1

    # Compare the two frequency dictionaries
    return count1 == count2

print(VTS())
disassemble(VTS)


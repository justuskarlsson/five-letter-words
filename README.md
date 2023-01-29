## Problem:
Find the maximum number of five-letter words which share no character.

I.e. (since the best solution is 5 words): 

**Find 5 five-letter words which share no character inbetween them.**

## Solution
Example solution:
```
jocks
muntz
glyph
vibex
dwarf
```
Time: 70 seconds (i5 13600k)

Because of the use of sets, will get a different solution each time.

If you don't like one of the chosen words, try adding it to the `banned_words`.

Usage: 
```
python main.py
```

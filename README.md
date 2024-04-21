# Bananagrams Engine - COMP3821 Project
An engine for solving the game bananagrams, a COMP3821 - Extended Algorithms Project.

Requires a recent download of the python implementation pypy at https://www.pypy.org/download.html to run the benchmarker.py and main.py files

To test an algorithm make sure your current directory is /src and run:
```
pypy3 benchmarker.py pletter1 letter2letter2
```
where letter1 refers to a player type according to the following:\
's': StandardPlayer,\
'r': StrandingPlayer,\
'p': PseudoPlayer,\
'd': StandardPlayerDangling,\
't': TwoLetterJunkStrandingPlayer,\
'n': NewStrandingPlayer\

and letter2 refers to a word scorer according to the following:\
'l': ScoreWordTwoLetter,\
'R': ScoreWordSimpleStrandingLongest,\
'H': ScoreWordHandBalanceLongest,\
'C': ScoreLetterCountLong\

Adjust the number of letters to add more algorithms to one game (up to 8).

Some sample runs in src/benchmark_runs

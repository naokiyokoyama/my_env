"""
Takes in one or two args. Prints integers from arg1 to arg2 on new lines.
Arg1 is 0 if only one arg is provided.
"""
import sys

if len(sys.argv[1:]) == 1:
    a, b = 0, sys.argv[1]
elif len(sys.argv[1:]) == 2:
    a, b = sys.argv[1:]
else:
    raise NotImplementedError

for i in range(int(a), int(b)):
    print(i)

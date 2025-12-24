import sys
from contextlib import redirect_stdout

# This text goes to standard output (console)
print("This line goes to the console.")

with open('output.txt', 'w') as f:
    with redirect_stdout(f):
        # All print statements within this 'with' block go to output.txt
        print("This text is redirected to the file.")
        print("So is this line.")
    # The 'with redirect_stdout(f):' block ends here, stdout is restored.

# This text goes back to standard output (console)
print("This line goes to the console again.")

import shlex
import os
text = 'ls -1 nonexistent 2> /tmp/bee/ant.md'
new_text = shlex.split(text)
if "2>" in new_text:
    operator_index = new_text.index("2>")
args = new_text[1:]
print(f"Arguments: {args}")
print(f"To use command with args: {new_text[:operator_index]}")
os.system(text)

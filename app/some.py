try:
    import readline
except ImportError:
    import pyreadline3 as readline

built_in = ['help', 'history', 'exit', 'help']

def auto_complete(text, state):
    matches = []
    for command in built_in:
        if command.startswith(text):
            matches.append(command+" ")
    if state < len(matches):
        return matches[state]
    else:
        None
    return matches[state] if state < len(matches) else None

readline.set_completer(auto_complete)
readline.parse_and_bind("tab: complete")

while True:
    command = input("$ ")
    print(f"You typed: {command}")

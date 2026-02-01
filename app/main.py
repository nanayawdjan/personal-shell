#!/usr/bin/env python3
import os
import sys
import shutil
import subprocess
import shlex
from contextlib import redirect_stdout 
try:
    import readline
except ImportError:
    import pyreadline3 as readline

def command_type(*args):
    if not args:
        print("type: missing operand")
    elif args and args[0] in commands:
        print(f"{args[0]} is a shell builtin")
    else: 
        if shutil.which(args[0]):
            print(f"{args[0]} is {shutil.which(args[0])}")
        else:
            print(f"{args[0]}: not found")


def change_directory(*args):
    if not args:
        print("cd: missing pathname")
    else:
        try:
            if args[0] == '~':
                os.chdir(os.path.expanduser("~"))
            else:
                os.chdir(args[0])
        except FileNotFoundError:
            print(f"cd: {args[0]}: No such file or directory")


commands = {
    "echo": lambda *args: print(' '.join(args)),
    "exit": lambda *args: sys.exit(),
    "type": command_type,
    "pwd": lambda *args: print(os.getcwd()),
    "cd": change_directory,
}

def auto_complete(text, state):
    """Autocomplete function for readline."""
    matches = []

    for command in commands:
        if command.startswith(text):
            matches.append(command)

    for path in os.environ.get("PATH", "").split(os.pathsep):
        if os.path.isdir(path):
            for file in os.listdir(path):
                if file.startswith(text) and os.access(os.path.join(path, file), os.X_OK):
                    matches.append(file)


    if state < len(matches):
        result = matches[state]
        if len(matches) == 1 and not result.endswith(" "):
            result += " "
        return result
    return None


def main():

    readline.set_completer(auto_complete)
    readline.parse_and_bind("tab: complete")
    
    while True:
        sys.stdin.flush()
        

        # Wait for user input
        try:
            command_with_args = shlex.split(input("$ "))
        except ValueError:
            continue

        # Check wheather the command is not empty
        if not command_with_args:
            continue

        stdout_target = None
        operator_index = None

        redirection_operators = ['1>', '>', '2>', '1>>', '>>', '2>>']

        for operator in redirection_operators:
            if operator in command_with_args:
                operator_index = command_with_args.index(operator)
                break
        
        command = command_with_args[0]
        args = command_with_args[1:]

        if operator_index is not None:
            stdout_target = command_with_args[operator_index + 1]    

            if command not in commands:
                if shutil.which(command):
                    os.system(f"{command} {' '.join(args)}")
                else:
                    print(f"{command}: command not found")
            else:
                if stdout_target:
                    os.system(f"{command} {' '.join(args)}")
        else:
            if command not in commands:
                if shutil.which(command):
                    subprocess.run([command, *args])
                else:
                    print(f"{command}: command not found")
            else:
                commands[command](*args)



if __name__ == "__main__":
    main()

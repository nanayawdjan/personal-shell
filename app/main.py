#!/usr/bin/env python3
import os
import sys
import time
import shutil
import subprocess
import shlex
from contextlib import redirect_stdout 

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


def chadir(*args):
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
    "cd": chadir
}


def main():
    
    while True:
        sys.stdin.flush()
        sys.stdout.write("$ ")
        

        # Wait for user input
        command_with_args = shlex.split(input())

        # Check wheather the command is not empty
        if not command_with_args:
            continue

        stdout_target = None
        operator_index = None

        if ">" in  command_with_args:
            operator_index = command_with_args.index(">")
        elif "1>" in command_with_args:
            operator_index = command_with_args.index("1>")
        elif "2>" in command_with_args:
            operator_index = command_with_args.index("2>")
            redirection_type = 'stderr'
        
        command = command_with_args[0]
        args = command_with_args[1:]

        if operator_index is not None:
            stdout_target = command_with_args[operator_index + 1]    

            if command not in commands:
                if shutil.which(command):
                    with open(stdout_target, "w") as file:
                        os.system(f"{command} {' '.join(args)}")
                else:
                    print(f"{command}: command not found")
            else:
                if stdout_target:
                    with open(stdout_target, "w") as file:
                        with redirect_stdout(file):
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

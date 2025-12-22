import os
import sys
import time
import shutil
import subprocess
import shlex

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


commands = {
    "echo": lambda *args: print(' '.join(args)),
    "exit": lambda *args: sys.exit(),
    "type": command_type,
    "pwd": lambda *args: print(os.getcwd())
}


def main():
    
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        # Wait for user input
        command_with_args = shlex.split(input())

        if not command_with_args:
            continue

        command = command_with_args[0]
        args = command_with_args[1:]

        if command not in commands:
            if shutil.which(command):
                subprocess.run([command, *args])
            else:
                print(f"{command}: command not found")
        else:
            commands[command](*args)


if __name__ == "__main__":
    main()

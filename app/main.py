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
        sys.stdout.write("$ ")
        sys.stdout.flush()

        # Wait for user input
        command_with_args = shlex.split(input())

        # Check wheather the command is not empty
        if not command_with_args:
            continue

        stdout_target = None
        operator_index = None
        if ">" in command_with_args or "1>" in command_with_args:
            if ">" in  command_with_args:
                operator_index = command_with_args.index(">")
            else:
                operator_index = command_with_args.index("1>") 

            stdout_target = command_with_args[operator_index + 1]    
            command_with_args = command_with_args[:operator_index]

        command = command_with_args[0]
        args = command_with_args[1:]

        if command not in commands:
            if shutil.which(command):
                if stdout_target:
                    with open(stdout_target, "w")as f:
                        subprocess.run([command, *args], stdout=f)
                else:
                    subprocess.run([command, *args])
            else:
                print(f"{command}: command not found")
        else:
            if stdout_target:
                with open(stdout_target, "w") as f:
                    f.write(*args)
            else:
                commands[command](*args)


if __name__ == "__main__":
    main()

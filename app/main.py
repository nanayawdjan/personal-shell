import sys
import time
import shutil

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
    "type": command_type
}


def main():
    
    while True:
        sys.stdout.write("$ ")

        # Wait for user input
        command_with_args = input().split()

        command = command_with_args[0]

        if command not in commands:
            print(f"{command}: command not found")
        else:
            commands[command](*command_with_args[1:])


if __name__ == "__main__":
    main()

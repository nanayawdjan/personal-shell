import sys
import time

def command_type(*args):
    if not args:
        print("type: missing operand")
    elif args and args[0] in commands:
        print(f"{args[0]} is a shell builtin")
    else: 
        print(f"{args[0]}: not found")

commands = {
    "echo": lambda *args: print(' '.join(args)),
    "exit": None,
    "type": command_type
}


def main():
    
    sys.stdout.write("$ ")

    # Wait for user input
    command_with_args = input().split()

    command = command_with_args[0]

    if command not in commands:
        print(f"{command}: command not found")
    elif command == "exit":
        sys.exit()
    else:
        commands[command](*command_with_args[1:])
    main()


if __name__ == "__main__":
    main()

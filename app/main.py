import sys
import time


def main():
    
    sys.stdout.write("$ ")

    # Wait for user input
    command = input()
    if command == "exit":
        sys.exit()
    else:
        sys.stdout.write(f"{command}: command not found\n")
    main()


if __name__ == "__main__":
    main()

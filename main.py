from executor import execute_from_args


def main():
    args = []

    while 'exit' not in args:
        command = input("\n>>> ")
        args = command.split()
        execute_from_args(args)


if __name__ == '__main__':
    main()

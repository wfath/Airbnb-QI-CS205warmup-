from Command import AverageCostCommand, FilterCommand, InfoCommand, HelpCommand, ShowCommand

class QueryInterface:

    def __init__(self):

        # The list of Command classes.
        commands = [
            AverageCostCommand.AverageCostCommand,
            FilterCommand.FilterCommand,
            InfoCommand.InfoCommand,
            HelpCommand.HelpCommand,
            ShowCommand.ShowCommand
        ]

        # Map Command string to Command objects.
        self.commands = {command.command: command() for command in commands}

        # Give HelpCommand the Command list.
        self.commands["help"].commands = commands

        # The boolean controlling the continuation of the command-line-interface.
        self.doRun = True


    def run(self):

        # Introduce program
        print("Query Interface")

        # Begin input loop
        while True:
            # Fetch and parse input.
            userInput = input("QueryI: ").lower()

            if userInput == "quit" or userInput == "exit":
                print("Goodbye")
                break

            # cut off args if they exist
            cmd = userInput[:userInput.find(" ")] if " " in userInput else userInput

            if cmd in self.commands:
                try:
                    self.commands[cmd].process(userInput[userInput.find(" "):])
                except KeyboardInterrupt as e:
                    raise
                except Exception as e:
                    print("An exception occurred while processing your command. Please try again with valid syntax.")


            else:
                print("Unrecognized command. Enter 'help' for a list of possible commands.")

            # Repeat


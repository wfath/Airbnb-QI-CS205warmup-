from Command import BaseCommand


class HelpCommand(BaseCommand.BaseCommand):

    # The Command syntax.
    command = "help"

    usageInfo = "help   Display usage information for all commands."

    def __init__(self, commands=[]):

        # Initialize with array of command classes.
        self.commands = commands
        super().__init__()

    def run(self):

        # Print usage-info for each Command.
        for command in self.commands:

            if command.usageInfo:
                print(command.usageInfo)
            else:
                # If Command is defined, but 'usageInfo' not, indicate 'no usage info'.
                if command.command:
                    print("%s - no usage information specified." % (command.command))

        return True

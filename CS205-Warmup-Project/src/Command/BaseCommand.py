import shlex


# TODO: Remove before merge.
# noinspection PyPep8Naming
class BaseCommand(object):

    # The Command syntax.
    command = ""

    usageInfo = ""

    def __init__(self):
        self.args = {}
        pass

    # parse args, run any checks, call self.run()
    # Returns true if command ran successfully, else prints usage info and ret false
    def process(self, cmdStr):
        self.args = {}
        if "=" in cmdStr:
            self.args = dict(token.split('=') for token in shlex.split(cmdStr))

        if not self.run():
            self.printErrorForInvalidSyntax()
            return False

        return True

    def run(self):
        """
        Executes the Command procedure.
        :return:
        """

        return True

    def printErrorForInvalidSyntax(self):
        """
        Displays an specific error message for this Command.
        :return: Self.
        """

        print("Invalid syntax. Here's the usage info:")
        print(self.usageInfo)

        return self

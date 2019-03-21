from Command.BaseCommand import BaseCommand
from db.models import Street, Listing
from texttable import Texttable


class ShowCommand(BaseCommand):

    command = "show"

    usageInfo = '''show [some=param] List some examples of Streets or Listings.
        streets  Show some examples of Streets
        listings Show some examples of Listings'''

    validParams = ["some"]
    validArgs = ["streets", "listings"]

    def run(self):

        # Return if there are no provided arguments for the Command.
        if not self.args:
            return False

        # Test for invalid parameters or arguments.
        if any(param not in self.validParams for param in self.args.keys()):
            return False
        if any(arg not in self.validArgs for arg in self.args.values()):
            return False

        table = Texttable()
        table.set_deco(Texttable.HEADER)

        if self.args["some"] == "streets":

            qs = Street.objects.order_by('?')[:10]

            table.set_cols_dtype(["i", "t", "t", "t"])
            table.set_cols_align(["l", "l", "l", "l"])
            table.set_cols_width([4, 50, 50, 8])
            table.add_row(["ID", "Name", "Neighborhood", "Zip-Code"])
            for street in qs:
                table.add_row([street.id, street.name, street.neighborhood, street.zip])

            print(table.draw())

        if self.args["some"] == "listings":

            qs = Listing.objects.order_by('?')[:10]

            table.set_cols_dtype(["i", "t", "t", "f"])
            table.set_cols_align(["l", "l", "l", "l"])
            table.set_cols_width([4, 50, 20, 8])
            table.add_row(["ID", "Street", "Property Type", "Price"])
            for listing in qs:
                table.add_row([listing.id, listing.street.name, listing.type, "$%s" % listing.price])

            print(table.draw())

        return True

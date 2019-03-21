from Command import BaseCommand
from db.models import Listing, Street
from texttable import Texttable
import shutil


class FilterCommand(BaseCommand.BaseCommand):
    # The Command syntax.
    command = "filter"
    validParams = ["price", "pricemax", "pricemin", "type", "street", "neighborhood", "zip"]
    usageInfo = '''filter [param=value]   Filter listings matching parameters, must specify at least one parameter. 
        price               Show only listings where the price matches exactly
        pricemin/pricemax   Show only listings where pricemin <= price <= pricemax
        type                Show only listings of a certain property type
        street              Show only listings on a specified street
        neighborhood        Show only listings in a neighborhood
        zip                 Show only listings in a zip code'''

    def run(self):
        """
        TODO: Write docs.
        :return:
        """

        if not self.args:
            return False

        if any(param not in self.validParams for param in self.args.keys()):
            return False

        qs = Listing.objects.all()

        # Filter listing parameters.
        if "price" in self.args:
            qs = qs.filter(price=self.args["price"])
        else:
            if "pricemin" in self.args:
                qs = qs.filter(price__gte=self.args["pricemin"])
            if "pricemax" in self.args:
                qs = qs.filter(price__lte=self.args["pricemax"])

        if "type" in self.args:
            types = [val["type"].lower() for val in Listing.objects.values('type').distinct()]
            if self.args["type"].lower() not in types:
                print("Invalid property type \"%s\". Valid property types are: %s" % (
                    self.args["type"], ", ".join('"{0}"'.format(t) for t in types)))
                return True
            qs = qs.filter(type__iexact=self.args["type"])

        # Perform foreign-key-parameters interpretation.
        if "street" in self.args:
            qs = qs.filter(street__name__iexact=self.args["street"])
        if "neighborhood" in self.args:
            qs = qs.filter(street__neighborhood__iexact=self.args["neighborhood"])
        if "zip" in self.args:
            qs = qs.filter(street__zip__iexact=self.args["zip"])

        if not qs.exists():
            print("No listings matching your criteria found. Try again with a less restrictive search.")

        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.set_cols_dtype(['i', 't', 't', 't', 'f'])
        table.set_cols_align(["l", "l", "l", "l", "l"])
        table.set_cols_width([4, 50, 35, 20, 8])
        table.add_row(["Id", "Street", "Neighborhood", "Type", "Price"])
        for listing in qs[:self.maxResults]:
            table.add_row(
                [listing.id, listing.street.name, listing.street.neighborhood, listing.type, "$%s" % listing.price])

        print(table.draw())

        # only show MAX_RESULTS
        if qs.count() > self.maxResults:
            print("Results trimmed. Showing %s of %s total matching listings." % (self.maxResults, qs.count()))

        return True

    def printErrorForInvalidSyntax(self):
        """ See parent. """

        print("You must specify arguments to filter Listings and Streets by. Usage of 'filter' is:")
        print(self.usageInfo)

        return self

    @property
    def maxResults(self):
        return int(shutil.get_terminal_size().lines - 4)  # terminal height - 4 lines for the other info

from Command import BaseCommand
from db.models import Listing
from django.db.models import Avg


class AverageCostCommand(BaseCommand.BaseCommand):

    # The command syntax.
    command = "average-cost"

    usageInfo = '''average-cost [param=value]   Get the average price of Listings.
        street          Show the average price of listings that are on this Street
        neighborhood    Show the average price of listings that are in this Neighborhood'''

    def run(self):

        # Return if there are no provided arguments for the Command.
        if not self.args:
            return False

        if "street" not in self.args and "neighborhood" not in self.args:
            return False

        # Fetch all of the listings from the database.
        qs = Listing.objects.all()

        # Define variables to contain query results and helper-values.
        streetIsGiven = False
        hoodIsGiven = False
        paramValue = str()
        streetValue = str()
        hoodValue = str()

        # Fetch the 'street' value if it exists.
        if "street" in self.args:
            streetIsGiven = True
            paramValue = self.args["street"]
            streetValue = paramValue
            qs = qs.filter(street__name__iexact=paramValue)

        # Fetch the 'neighborhood' value if it exists.
        if "neighborhood" in self.args:
            hoodIsGiven = True
            paramValue = self.args["neighborhood"]
            hoodValue = paramValue
            qs = qs.filter(street__neighborhood__iexact=paramValue)

        # Inform user if the provided street/neighborhood values do not exist.
        if not qs.exists():
            if streetIsGiven and hoodIsGiven:
                print("There are no listings in: %s, %s." % (streetValue, hoodValue))
            else:
                print("There are no listings in: %s" % paramValue)

        else:
            # Calculate and display the average listing price.
            avgListingPrice = round(qs.aggregate(Avg('price'))['price__avg'], 2)

            if streetIsGiven and hoodIsGiven:
                print("The average price for listings in %s, %s is: $%d" %
                      (self.args["street"], self.args["neighborhood"], avgListingPrice)
                      )
            else:
                print("The average price for listings in %s is: $%d" % (paramValue, avgListingPrice))

        return True

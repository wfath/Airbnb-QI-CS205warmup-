from Command import BaseCommand
from db.models import Listing, Street


class InfoCommand(BaseCommand.BaseCommand):
    command = 'info'
    usageInfo = '''info [param=value]   Show the information for a specific street or listing
        streetid     Show the info for the street that has the same ID as specified by the user
        listingid    Show the info for the listing that has the same ID as specified by the user'''

    def run(self):

        if not self.args:
            return False

        if "listingid" in self.args and "streetid" in self.args:
            print("Cannot specify both listing and street")
            return False

        # make sure either listing or street is in self.args
        if "listingid" not in self.args and "streetid" not in self.args:
            print("Must specify either listingid or streetid")
            return False

        # if its a listing
        if "listingid" in self.args:
            # make sure the id is a valid int
            try:
                int(self.args["listingid"])
            except ValueError:
                print("Listing ID is not a valid integer. Try again.")
                return False

            # if it exists
            if Listing.objects.filter(id=self.args["listingid"]).exists():
                listing = Listing.objects.get(id=self.args["listingid"])
                print("Street:       %s" % listing.street.name)
                print("Neighborhood: %s" % listing.street.neighborhood)
                print("Zip Code:     %s" % listing.street.zip)
                print("")
                print("Type:         %s" % listing.type)
                print("Price         $%s" % listing.price)

            else:
                # means invalid id, try again
                print("You have entered a listing id that does not exist. Try again.")

        # if its a street
        if "streetid" in self.args:
            # make sure the id is a valid int
            try:
                int(self.args["streetid"])
            except ValueError:
                print("streetid is not a valid integer. Try again.")
                return False

            # if it exists
            if Street.objects.filter(id=self.args["streetid"]).exists():
                street = Street.objects.get(id=self.args["streetid"])

                # checks to see whether there is a zip code listed or not (may have to change later)
                print("Street:       %s" % street.name)
                print("Neighborhood: %s" % street.neighborhood)
                print("Zip Code:     %s" % street.zip)

            else:
                # not a valid id
                print("You have entered a street id that does not exist. Try again.")
        return True

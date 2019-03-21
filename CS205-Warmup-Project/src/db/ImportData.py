import sys
import os
sys.path.insert(1, os.path.abspath(os.path.join(
    os.path.dirname(os.path.realpath(__file__)), os.pardir)))

import WarmupProject.djangoSetup
from WarmupProject import settings
from db.models import Listing, Street
import csv


def main():
    print("Importing data from %s" % (settings.CSV_FILE_PATH))
    with open(settings.CSV_FILE_PATH, "r", encoding="utf-8") as f:
        reader = csv.reader(f)

        # look at the headers and determine the indexes of the cols we care about
        headers = next(reader)
        indices = {
            "neighborhood": headers.index("neighbourhood"),
            "street": headers.index("street"),
            "zip": headers.index("zipcode"),
            "type": headers.index("room_type"),
            "price": headers.index("price")
        }

        for row in reader:
            if not Street.objects.filter(name=row[indices["street"]]).exists():
                street = Street.objects.create(
                    name=row[indices["street"]],
                    zip=row[indices["zip"]],
                    neighborhood=row[indices["neighborhood"]]
                )
            else:
                street = Street.objects.get(name=row[indices["street"]])

            # create the listign if one does not exist
            price = float(row[indices["price"]].replace(
                "$", "").replace(",", ""))
            roomType = row[indices["type"]]
            if not Listing.objects.filter(street=street, price=price, type=roomType).exists():
                Listing.objects.create(
                    street=street,
                    price=price,
                    type=roomType
                )

        print("Finished adding listings. %s total listings and %s streets in database." % (
            Listing.objects.all().count(), Street.objects.all().count()))


if __name__ == "__main__":
    main()

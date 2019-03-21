from db.models import Listing, Street
from django.db.utils import IntegrityError
from django.test import TestCase
from WarmupProject import settings
import os


class StreetTests(TestCase):

    def testSaveZip(self):
        street = Street.objects.create(
            zip="1010 AH", neighborhood="adasdasdasd", name="street")
        self.assertEqual(street.zip, "1010AH")

        street = Street.objects.create(
            zip="1234AH", neighborhood="adasdasdasd", name="street2")
        self.assertEqual(street.zip, "1234AH")

        street = Street.objects.create(
            zip="1010", neighborhood="adasdasdasd", name="street3")
        self.assertEqual(street.zip, "1010")

    def testUnique(self):
        Street.objects.create(
            zip="1231AB", neighborhood="adad", name="street4")

        with self.assertRaises(IntegrityError):
            Street.objects.create(
                zip="1231AB", neighborhood="adad", name="street4")


class ListingTests(TestCase):
    def setUp(self):
        street = Street.objects.create(
            zip="1010 AH", neighborhood="adasdasdasd", name="street")
        street.save()

    def testUnique(self):
        street = Street.objects.get(id=1)
        Listing.objects.create(
            street=street, price=123.45, type="Apt")
        with self.assertRaises(IntegrityError):
            Listing.objects.create(
                street=street, price=123.45, type="Apt")


class DataImportTests(TestCase):
    def testFileExists(self):
        # make sure the var is set in settings
        try:
            settings.CSV_FILE_PATH
        except AttributeError:
            self.fail("settings.CSV_FILE_PATH not defined")
        self.assertNotEqual(settings.CSV_FILE_PATH, None)

        # check if the file exists
        self.assertTrue(os.path.isfile(settings.CSV_FILE_PATH))

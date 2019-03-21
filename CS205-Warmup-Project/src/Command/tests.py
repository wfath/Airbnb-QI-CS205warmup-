# Set project path and do django setup
import sys
import os

sys.path.insert(0, os.path.abspath(os.pardir))
from WarmupProject import djangoSetup
# Imports
from django.test import TestCase
from Command import BaseCommand, InfoCommand, FilterCommand, AverageCostCommand
from db.models import Listing, Street


class BaseCommandTests(TestCase):

    def testArgParsing(self):
        cmd = BaseCommand.BaseCommand()

        status = cmd.process(
            'testint=123 testquotes="string" testquotesspaces="string with spaces" testdouble=123.4')
        self.assertTrue(status)
        self.assertEqual(int(cmd.args["testint"]), 123)
        self.assertEqual(float(cmd.args["testdouble"]), 123.4)
        self.assertEqual(cmd.args["testquotes"], "string")
        self.assertEqual(cmd.args["testquotesspaces"], "string with spaces")

        status = cmd.process("test='testing' test2='test with spaces'")
        self.assertTrue(status)
        self.assertEqual(cmd.args["test"], "testing")
        self.assertEqual(cmd.args["test2"], "test with spaces")

        status = cmd.process("")
        self.assertTrue(status)
        self.assertFalse(cmd.args)


class InfoCommandTests(TestCase):

    def setUp(self):
        self.info = InfoCommand.InfoCommand()

    def testBothArgs(self):
        status = self.info.process("listingid=12 streetid=12")
        self.assertFalse(status)

    def testNoArgs(self):
        status = self.info.process("")
        self.assertFalse(status)

    def testInvalidID(self):
        # note that database is empty at this point
        status = self.info.process("listingid=53")
        self.assertTrue(status)

        # same thing for street
        status = self.info.process("streetid=12")
        self.assertTrue(status)

    def testValidID(self):
        street = Street.objects.create(
            name="test street", neighborhood="test neighborhood", zip="1234FF")
        listing = Listing.objects.create(street=street, price=123, type="Apt")

        id = Listing.objects.first().id
        status = self.info.process("listingid=%s" % (id))
        self.assertTrue(status)

        id = Street.objects.first().id
        status = self.info.process("streetid=%s" % (id))
        self.assertTrue(status)

        Street.objects.all().delete()
        Listing.objects.all().delete()


class FilterCommandTests(TestCase):

    def setUp(self):
        self.filter = FilterCommand.FilterCommand()

    def testNoArgs(self):
        status = self.filter.process("")
        self.assertFalse(status)

    def testArgs(self):
        self.assertTrue(self.filter.process("price=50"))
        self.assertTrue(self.filter.process("pricemin=35"))
        self.assertTrue(self.filter.process("pricemax=57"))
        self.assertTrue(self.filter.process("type=50"))
        self.assertTrue(self.filter.process("street=st"))
        self.assertTrue(self.filter.process("neighborhood=\"some neighborhood\""))
        self.assertTrue(self.filter.process("zip=0000nn"))

        self.assertFalse(self.filter.process("test=test"))


class AverageCostCommandTests(TestCase):

    def setUp(self):
        self.averageCost = AverageCostCommand.AverageCostCommand()

    def testNoArgs(self):
        self.assertFalse(self.averageCost.process(""))

    def testArgs(self):
        self.assertTrue(self.averageCost.process("neighborhood=\"some neighborhood\""))
        self.assertTrue(self.averageCost.process("street=\"some street\""))

from django.db import models


class Street(models.Model):
    name = models.CharField(max_length=255, unique=True)
    neighborhood = models.CharField(max_length=255)
    # zip is 4 numeric digits followed by an optional 2 letters
    zip = models.CharField(max_length=6)


    class Meta:
        db_table = "street"

    def save(self, *args, **kwargs):
        self.zip = self.zip.replace(" ", "")
        super().save(*args, **kwargs)


class Listing(models.Model):
    street = models.ForeignKey(Street, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    type = models.CharField(max_length=255)

    class Meta:
        db_table = "listing"
        unique_together = (("street", "price", "type"))

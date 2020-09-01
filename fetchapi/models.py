from django.db import models

# Create your models here.
class Products(models.Model):
    year = models.CharField(max_length=100)
    petroleum_product = models.CharField(max_length=255)
    sale = models.IntegerField()

    def __str__(self):
        return self.petroleum_product

from django.db import models
from product.models import Product
from brand.models import BrandProfile

class Inspection(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    brand = models.ForeignKey(BrandProfile, on_delete=models.CASCADE)
    improvements_needed = models.TextField(blank=True)
    comments = models.TextField(blank=True)


    def __str__(self):
        return f"{self.product.name} - {self.brand.user.username}"

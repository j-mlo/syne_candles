from django.db import models

# Create your models here.
class Product(models.Model):
    SIZE_CHOICES = (
        ('180ml', '180ml'),
        ('500ml', '500ml')
    )

    name = models.CharField(max_length=254)
    description = models.TextField()
    size = models.CharField(choices=SIZE_CHOICES, default='180ml')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    sku = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

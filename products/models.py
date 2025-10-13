from django.db import models

# Create your models here.
class Product(models.Model):
    SIZE_CHOICES = (
        ('180ml', '180ml'),
        ('500ml', '500ml')
    )

    name = models.CharField(max_length=254)
    subtitle = models.TextField(null=True, blank=True)
    description = models.TextField()
    is_candle = models.BooleanField(default=True)
    size = models.CharField(choices=SIZE_CHOICES, default='180ml', null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    main_image = models.ImageField(upload_to='products/', null=True, blank=True)
    extra_image1 = models.ImageField(upload_to='products/', null=True, blank=True)
    extra_image2 = models.ImageField(upload_to='products/', null=True, blank=True)
    sku = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

import os
from django.db import models
from brand.models import BrandProfile
import uuid
from django.contrib.auth.models import User

def product_image_path(instance, filename):
    # Generate a unique ID for the image
    image_id = uuid.uuid4().hex

    # Rename the file using the unique ID
    ext = filename.split('.')[-1]
    filename = f'{image_id}.{ext}'

    # Create directory based on brand
    brand_directory = instance.brand.user.username

    # Construct the full path
    directory_path = os.path.join('D:\\School api\\destroyBit-master\\product\\product_images', brand_directory)

    # Create the directory if it doesn't exist
    os.makedirs(directory_path, exist_ok=True)

    # Set the image_id field value to match the filename without extension
    instance.image_id = image_id

    return os.path.join(directory_path, filename)

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    brand = models.ForeignKey(BrandProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    product_type = models.CharField(max_length=100)
    price = models.FloatField()
    food_additives = models.TextField()
    food_preservatives = models.TextField(default='null')  # Set default value here
    image = models.ImageField(upload_to=product_image_path)  # Update Image Field
    image_id = models.UUIDField(default=uuid.uuid4, editable=False)  # Add Image ID Field
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Cart: {self.user.username} - {self.product.name} ({self.quantity})"
    

class ProductReport(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Report {self.id}: {self.user.username} - {self.product.name} - Active: {self.active}"

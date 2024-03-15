from django.utils import timezone
from django.utils.text import slugify
from django.db import models
from vendor.models import Vendor

# Create your models here.
class Category(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def clean(self):
        self.category_name = self.category_name.capitalize()

    # def save(self, *args, **kwargs):
    #     # Generate slug based on category name and vendor ID
    #     if not self.slug:
    #         base_slug = slugify(f"{self.category_name}-{self.vendor.id}")
    #         self.slug = base_slug
    #         suffix = 1
    #         while Category.objects.filter(slug=self.slug).exists():
    #             self.slug = f"{base_slug}-{suffix}"
    #             suffix += 1
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.category_name
    
class FoodItem(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="fooditems")
    food_title = models.CharField(max_length = 50)
    slug = models.SlugField(max_length = 255, unique=True)
    description = models.TextField(max_length = 255, blank = True)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    image = models.ImageField(upload_to='foodImages')
    is_available = models.BooleanField(default = True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.food_title
    
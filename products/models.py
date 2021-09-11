from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Team(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    Sizes = (('XS', 'X-Small'), ('S', 'Small'), ('M', 'Medium'),
             ('L', 'Large'), ('XL', 'X-Large'))
    INTEGER_QTY = [tuple([x, x]) for x in range(1, 2500)]
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    team = models.ForeignKey(
        'Team', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    size = MultiSelectField(choices=Sizes, null=True, blank=True)
    qty = models.IntegerField(default='5')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


INTEGER_CHOICES = [tuple([x, x]) for x in range(1, 6)]


class Review(models.Model):
    """Saves a review model in database"""

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews')
    rating = models.IntegerField(
        choices=INTEGER_CHOICES, default='5')
    reviewer = models.ForeignKey(
        User, on_delete=models.CASCADE)
    date = models.DateTimeField(
        auto_now_add=True)
    review_title = models.CharField(
        max_length=50, null=False,
        blank=False)
    review = models.TextField(
        max_length=1024, null=False,
        blank=False)

    def __str__(self):
        return self.review_title

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Categories(models.Model):
    CATEGORY_CHOICES = [
        ('Toys', 'Toys'),
        ('Hardware', 'Hardware'),
        ('Electronics', 'Electronics')
        ]
    category = models.CharField(max_length=12, choices=CATEGORY_CHOICES)
    
    def __str__(self):
        return f"{self.category}"

class Listings(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=260)
    image = models.URLField(null="True")
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    start_bid = models.DecimalField(max_digits=11, decimal_places=2)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id}: {self.image} {self.title} ({self.category}). {self.description}. Bidding to start at {self.start_bid}. For sale by {self.seller}. Closed status is {self.closed}"
        
class Bids(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits=11, decimal_places=2)

class Comments(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)
    commentor = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=260)
    
class Watchlists(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}: {self.user}, {self.listing}"

class posts(models.Model):
    comment = models.CharField(max_length=265)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=False, auto_now_add=True)

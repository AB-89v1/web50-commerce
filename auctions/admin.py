from django.contrib import admin
from .models import Listings, User, Bids, Categories, Watchlists, posts
# Register your models here.
admin.site.register(Listings)
admin.site.register(User)
admin.site.register(Bids)
admin.site.register(Categories)
admin.site.register(Watchlists)
admin.site.register(posts)

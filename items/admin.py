from items.models import Category, Item, ItemUsageDurationType, ItemUsageRatingType
from django.contrib import admin

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(ItemUsageDurationType)
admin.site.register(ItemUsageRatingType)
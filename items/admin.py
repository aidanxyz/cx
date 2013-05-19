from items.models import Category, Item, ItemUsageDurationType, ItemUsageRatingType, ItemDeactivationReason, ItemEditReason, Specification, SpecificationType, Price
from django.contrib import admin

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(ItemUsageDurationType)
admin.site.register(ItemUsageRatingType)
admin.site.register(ItemDeactivationReason)
admin.site.register(ItemEditReason)
admin.site.register(Specification)
admin.site.register(SpecificationType)
admin.site.register(Price)

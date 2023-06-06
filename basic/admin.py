from django.contrib import admin
from .models import User, Ouds, Categories, Order, QuantityManagement,Tracker, ContactUs, Review, WebContents,Promos

class OudAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'base_price', 'category')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)

class TrackerDate(admin.ModelAdmin):
    readonly_fields = ('order_date',)

admin.site.register(User)
admin.site.register(Ouds, OudAdmin)
admin.site.register(Categories, CategoryAdmin)
admin.site.register(Order)
admin.site.register(QuantityManagement)
admin.site.register(Tracker,TrackerDate)
admin.site.register(ContactUs)
admin.site.register(Review)
admin.site.register(WebContents)
admin.site.register(Promos)


# Register your models here.

from django.contrib import admin
from .models import UserFavoriteBook, UserInformations, SubscriptionRecord, LendBook
from django_jalali.admin.filters import JDateFieldListFilter

# you need import this for adding jalali calander widget
import django_jalali.admin as jadmin

# Register your models here.
class UserInformationsAdmin(admin.ModelAdmin):
    list_filter = (
        ('birth_date', JDateFieldListFilter),
    )
    
admin.site.register(UserInformations)
admin.site.register(UserFavoriteBook)
admin.site.register(SubscriptionRecord)
admin.site.register(LendBook)
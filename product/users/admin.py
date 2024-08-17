from django.contrib import admin
from django.contrib.admin import ModelAdmin

from users.models import CustomUser, Balance, Subscription


# Register your models here.

@admin.register(CustomUser)
class userAdmin(ModelAdmin):
    pass

@admin.register(Balance)
class balanceAdmin(ModelAdmin):
    pass

@admin.register(Subscription)
class SubAdmin(ModelAdmin):
    pass

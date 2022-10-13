from django.contrib import admin
from .models import *
# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'phone', 'profile_pic', 'first_name', 'last_name', 'dob', 'gender',
    				'password','date_joined', 'last_login')
    list_filter = ('email', 'username')
    search_fields = ('email', 'username')


class ImageWareHouseAdmin(admin.ModelAdmin):
    list_display = ('user', 'image', 'is_active')
    list_filter = ('user', 'image')


admin.site.register(UserProfile, UserProfileAdmin)    
admin.site.register(ImageWareHouse, ImageWareHouseAdmin)    

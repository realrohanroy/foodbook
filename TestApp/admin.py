# OR Traditional way
# admin.site.register(Contact, ContactAdmin)
from django.contrib import admin
from .models import  CustomUser 
from .models import CustomUser , Recipe, Rating, Review 
from django.contrib.auth.admin import UserAdmin  
# Register your models here.


# Register the CustomUser  model
class CustomUser_Admin(UserAdmin):
    model = CustomUser 
    list_display = ['email', 'first_name', 'last_name', 'is_active', 'is_staff']  # Customize fields to display
    list_filter = ['is_active', 'is_staff']  # Add filters for the admin interface
    ordering = ['email']  # Order by email

admin.site.register(CustomUser , CustomUser_Admin)  

admin.site.register(Recipe)
admin.site.register(Rating)
admin.site.register(Review)
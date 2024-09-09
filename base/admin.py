from django.contrib import admin

# Register your models here.

from .models import Room, Topic, Message, User, Branch, Year

admin.site.register(User)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Year)
admin.site.register(Branch)
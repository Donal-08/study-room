from django.contrib import admin

# Register your models here.
# Register so that you can see your created models in the DB/admin

from .models import Room, Topic, Message

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)




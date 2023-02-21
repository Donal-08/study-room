from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Whenever you add model the first thing you do is makemigrations
# After u execute the command "python3 manage.py makemigrations", it will create a file in the migrations folder 
# => the class inside 0001.py basically shows all the mogrations we are gonna apply(staging area be4 we actually update the DB) 
# python3 manage.py migrate  => GO INTO THE LATEST MIGRATIONS AND IT WILL EXCUTE THOSE


class Topic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)   # a topic can have multiple rooms whereas a room can have only one topic (ONE-MANY relationship)
    name = models.CharField(max_length=100)                     # null=False is by default
    description = models.TextField(null=True, blank=True)  # when we run the save method i.e when we submit a form that form can also be empty
    # participants =           # store all the users active in a room
    participants = models.ManyToManyField(User, related_name='participants', blank=True)     # to be able to submit a form without having to check sth
    updated = models.DateTimeField(auto_now=True)       # auto_now=True => every time the save method is called , take a timestamp
    created = models.DateTimeField(auto_now_add=True)   #  auto_now_add=True => takes a tometamp only the first time we save/create this instance


    class Meta:
        ordering = ['-updated', '-created']               # newest would be first and hence the '-updated'

    def __str__(self):
        return str(self.name)

 
class Message(models.Model):           
    user = models.ForeignKey(User, on_delete=models.CASCADE)   # one to many relationship - A user can have many messages but a message can be by only one USER
    room = models.ForeignKey(Room, on_delete=models.CASCADE)   # Room is the parent, if there is no room in Room, no message should be there  # MANY TO ONE RELATIONSHIP with the class {{"ROOM"}}  i.e  MANY differnet messages in one class 
    body = models.TextField()                                  # we do want to force the user to write a message
    updated = models.DateTimeField(auto_now=True)        
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']      # newest first  

    def __str__(self):
        return self.body[:50]                       # in thr epreview we only want the first 40 characters

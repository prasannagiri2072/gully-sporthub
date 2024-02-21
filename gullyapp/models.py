from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Carousel(models.Model):
    title = models.CharField(max_length=200,null=True,blank=True)
    description =models.TextField(null=True,blank=True)
    image = models.FileField(null=True,blank=True)

    def __str__(self):
        return self.title
    
class Category(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

import math


from django.contrib.auth.models import User
from django.db import models
from django.db.models.functions import ACos, Cos, Radians, Sin

# models.py


from django.contrib.auth.models import User
from django.db import models

class ShownTeamsHistory(models.Model):
    team = models.ForeignKey('createTeam', on_delete=models.CASCADE)
    shown_team = models.ForeignKey('createTeam', related_name='shown_teams_history', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class createTeam(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    teamcaptain = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    contact = models.CharField(max_length=20)
    image = models.FileField(null=True, blank=True)
    noofplayers = models.CharField(max_length=20, null=True, blank=True)
    location = models.CharField(max_length=255, default="Unknown")
    shown_teams = models.ManyToManyField(ShownTeamsHistory, blank=True, related_name='teams_shown')


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.teamcaptain:
            self.teamcaptain = self._get_team_captain()

        super(createTeam, self).save(*args, **kwargs)

    def _get_team_captain(self):
        return User.objects.first()

    def update_location(self, latitude, longitude):
        # Update the team's location based on the provided latitude and longitude
        self.location = f"Latitude: {latitude}, Longitude: {longitude}"
        self.save()


# models.py
# models.py
from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    challenge_id = models.CharField(max_length=36, null=True, blank=True)  # Assuming challenge ID is a string

    is_read = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.message
from django.db import models

# 1. 👇 Add the following line
class Notifications(models.Model):
    message = models.CharField(max_length=100)
    
    def __str__(self):
        return self.message

# models.py
from django.db import models
from django.contrib.auth.models import User

class MatchRequest(models.Model):
    team = models.ForeignKey(createTeam, related_name='match_requests_sent', on_delete=models.CASCADE)
    opponent = models.ForeignKey(createTeam, related_name='match_requests_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.team.name} vs. {self.opponent.name} - {self.created_at}"




class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
   
    
    
    
class Userprofile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    image = models.FileField(null=True, blank=True)
   
    def __str__(self):
        return self.user.username
    


#notification



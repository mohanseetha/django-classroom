from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    branches = [
        ("CSE", "CSE"),
        ("CSM", "CSM"),
        ("CSD", "CSD"),
        ("CSC", "CSC"),
    ]
    years = [
        ("1st", "1st"),
        ("2nd", "2nd"),
        ("3rd", "3rd"),
        ("4th", "4th"),
    ]
    name = models.CharField(max_length=200, null=True)
    username = models.CharField(max_length=200, null=True, unique=True)
    email = models.EmailField(null=True)
    bio = models.TextField(null=True)
    branch = models.CharField(max_length=10, choices=branches, null=True, blank=True)
    year = models.CharField(max_length=10, choices=years, null=True, blank=True)
    avatar = models.ImageField(null=True, default='avatar.svg')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Branch(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
class Year(models.Model):
    yos = models.CharField(max_length=10)

    def __str__(self):
        return self.yos


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    year = models.ForeignKey(Year, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    desc = models.TextField(null=True, blank=True)
    followers = models.ManyToManyField(User, related_name="followers", blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created', ]

    def __str__(self):
        return self.name
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    file = models.FileField(null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created', ]

    def __str__(self):
        return self.body[:50]


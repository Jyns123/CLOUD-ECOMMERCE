from django.db import models

class User(models.Model):
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=100)
    
    def __str__(self):
        return self.username

class Doctor(models.Model):
    name = models.CharField(max_length=50)
    specialty = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

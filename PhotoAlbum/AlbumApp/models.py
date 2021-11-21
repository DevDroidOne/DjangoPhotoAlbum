from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Album(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100,null=False,blank= False)

    def __str__(self):
        return self.name

class Photo(models.Model):
    user = models.ManyToManyField(User)
    album = models.ForeignKey(Album, on_delete=models.SET_NULL,null=True,blank=True)
    image = models.ImageField(null=False,blank=False)
    description = models.TextField(null=True)
    geolocation = models.TextField(null=True)
    tags = models.TextField(null=True)
    captureDate = models.DateField(null=True)
    capturedBy = models.TextField(null=True)

    def __str__(self):
        return self.description



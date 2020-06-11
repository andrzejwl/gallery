from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    
    def __repr__(self):
        return str(self.name)

    def __str__(self):
        return str(self.name)

class Image(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default='sample.jpg', upload_to='images')
    description = models.TextField(null=True)
    upload_date = models.DateField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

class Settings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_width = models.IntegerField()
    display_height = models.IntegerField()
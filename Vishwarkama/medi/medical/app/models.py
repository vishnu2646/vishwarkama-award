from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
# Create your models here.
class Doctor(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True)
    qualification = models.CharField(max_length=50,null=True,blank=True)
    spelization = models.CharField(max_length=100,blank=True,null=True)
    location = models.CharField(max_length=100,blank=True,null=True)
    doctor = models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profile_pics')
    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse('pdetail', kwargs={'pk':self.pk})

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profile_pics')
    firstname = models.CharField(max_length=50,blank=True,null=True)
    lastname = models.CharField(max_length=50,blank=True,null=True)
    phone = models.IntegerField(null=True,blank=True)
    gender = models.CharField(max_length=50,blank=True,null=True)
    aboutme = models.TextField(null=True,blank=True)
    clinicname = models.CharField(max_length=100,blank=True,null=True)
    address = models.CharField(max_length=100,blank=True,null=True)
    contactaddress1 = models.CharField(max_length=100,blank=True,null=True)
    contactddress2 = models.CharField(max_length=100,blank=True,null=True)
    city = models.CharField(max_length=100,blank=True,null=True)
    state = models.CharField(max_length=100,blank=True,null=True)
    country = models.CharField(max_length=100,blank=True,null=True)
    postal = models.CharField(max_length=100,blank=True,null=True)
    price = models.CharField(max_length=100,blank=True,null=True,default="Free")
    spelization = models.CharField(max_length=100,blank=True,null=True)
    service = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Appoinment(models.Model):
    doctor_name = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.CharField(max_length=20)
    name = models.CharField(max_length=100,null=True,blank=True)
    phone = models.IntegerField()
    reason = models.TextField()
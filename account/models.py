from django.db import models
from django.contrib.auth.models import User, Permission

class TypeUser(models.Model):
    type = models.CharField(max_length=20)

    def __str__(self):
        return self.type

class User_TypeUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type_user = models.ForeignKey(TypeUser, on_delete=models.CASCADE)

GENDER = [
    ('m','Masculino'),
    ('f','Femenino'),
    ('o','Other')
]
MARITAL_STATUS = [
    ('s','Soltero'),
    ('e','Es Complicado'),
    ('c','Casado'),
    ('d','Divorsiado'),
    ('v','Viudo'),
    ('p','Prefiero no decirlo')
]

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    date_birth = models.DateField(blank=True,null=True)    
    gender = models.CharField(choices=GENDER,max_length=1,blank=True,null=True)
    marital_status = models.CharField(choices=MARITAL_STATUS,max_length=1,blank=True,null=True)
    about_me = models.TextField(help_text='Description about me.',blank=True,null=True)
    photo = models.ImageField(blank=True,upload_to='user/%Y/%m/%d/')

    def __str__(self):
        return f'Profile of {self.user.username}'

class SocialAddress(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True)
    url = models.CharField(max_length=250,blank=True,null=True)
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class AsignPermission(models.Model):
    name = models.CharField(max_length=200)
    type_user = models.ManyToManyField(TypeUser,related_name='aign_permission')
    permission = models.OneToOneField(Permission,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
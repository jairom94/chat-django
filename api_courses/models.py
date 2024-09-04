from django.db import models
from django.contrib.auth.models import User, AbstractUser

class Student(models.Model):
    dni = models.CharField(max_length=20)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username


class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.title

class Item(models.Model):
    item = models.TextField()

    def __str__(self):
        return self.item


class Content(models.Model):
    order =models.IntegerField()
    item = models.ForeignKey(Item,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.order}. {self.item}'
    
class Module(models.Model):
    order = models.IntegerField(unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    contents = models.ManyToManyField(Content,blank=True)


    def __str__(self):
        return f'{self.order}. {self.title}'
    
class Course(models.Model):
    subject = models.ForeignKey(Subject,related_name='subject',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User,related_name='owner',on_delete=models.CASCADE)
    modules = models.ManyToManyField(Module)
    students = models.ManyToManyField(Student)


    def __str__(self):
        return self.title
    


    

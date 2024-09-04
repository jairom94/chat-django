from django.db import models
from django.contrib.auth.models import User


class TypeNotification(models.Model):
    type = models.CharField(max_length=50)    
    def __str__(self):
        return self.type


class Notification(models.Model):
    detalle = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_notifications')
    type = models.ForeignKey(TypeNotification, on_delete=models.CASCADE, related_name='type_notifications')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.detalle
    
class NotificationUser(models.Model):
    notification = models.ForeignKey(Notification,on_delete=models.CASCADE)
    users = models.ManyToManyField(User,related_name='notifications_user')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.notification.detalle

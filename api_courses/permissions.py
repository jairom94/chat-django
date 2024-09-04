from rest_framework.permissions import BasePermission
from . import models


class isEnrolled(BasePermission):
    def has_object_permission(self, request, view, obj):
        student = models.Student.objects.get(user=request.user)        
        return obj.students.filter(id=student.id).exists()
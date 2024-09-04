from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from api_courses.models import Course, Student

@login_required
def course_chat_room(request,course_id):
    try:
        user = request.user   

        student = get_object_or_404(Student,user=user)    
        course = Course.objects.filter(id=course_id,students=student)
        #print(user)        
    except:        
        return HttpResponseForbidden()
    return render(request, 'chat/room.html',{'course':course.first()})

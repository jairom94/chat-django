from django.shortcuts import render,get_object_or_404

from rest_framework import generics,viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action


from . import serializers
from . import permissions
from . import models

class SubjectListView(generics.ListAPIView):
    queryset = models.Subject.objects.all()
    serializer_class = serializers.SubjectSerializer

class SubjectDetailView(generics.RetrieveAPIView):
    queryset = models.Subject.objects.all()
    serializer_class = serializers.SubjectSerializer

class CourseEnrollView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, pk, format=None):
        course = get_object_or_404(models.Course, pk=pk)
        course.students.add(request.user)
        return Response({'enrolled': True})
        
class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer

    @action(methods=['post'],
            detail=True,
            authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated])
    def enroll(self,request):
        course = self.get_object()
        user = request.user
        student = models.Student.objects.get(user=user)
        course.students.add(student)
        return Response({'enrolled': True})
    
    @action(methods=['get'],
            detail=True,
            serializer_class=serializers.CourseWithContentsSerializer,
            authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated, permissions.isEnrolled ]
            )
    def contents(self,request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    

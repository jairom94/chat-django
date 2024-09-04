from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

from . import models

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subject
        fields = ['id', 'title', 'slug']

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Module
        fields = ['order', 'title', 'description']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = ['dni', 'user']


class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)
    students = StudentSerializer(many=True, read_only=True)
    class Meta:
        model = models.Course
        fields = ['id', 'subject', 'title', 'slug',
                   'overview', 'created', 'owner',
                     'modules','students']

class ItemRelatedField(serializers.RelatedField):
    def to_representation(self, value):                
        return value.item

class ContentSerializer(serializers.ModelSerializer):
    item = ItemRelatedField(read_only=True)
    class Meta:
        model = models.Content
        fields = ['order', 'item']

class ModuleWithContentSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True)
    class Meta:
        model = models.Module
        fields = ['order', 'title', 'description', 'contents']

class CourseWithContentsSerializer(serializers.ModelSerializer):
    modules = ModuleWithContentSerializer(many=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = models.Course
        fields = ['id','subject','title','slug','overview','created','owner','modules']


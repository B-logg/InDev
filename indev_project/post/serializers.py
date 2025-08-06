from rest_framework import serializers
from .models import PostMassil
from route.serializers import RoutineSerializer

class PostMassilSerializer(serializers.ModelSerializer):
    routine = RoutineSerializer(read_only=True)

    class Meta:
        model = PostMassil
        fields = '__all__'
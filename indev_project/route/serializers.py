from rest_framework import serializers
from .models import Routine, VisitRoutine

class VisitRoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitRoutine
        fields = '__all__'

class RoutineSerializer(serializers.ModelSerializer):
    visit_points = VisitRoutineSerializer(many=True, read_only=True)

    class Meta:
        model = Routine
        fields = '__all__'
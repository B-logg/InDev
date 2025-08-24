from rest_framework import serializers
from .models import PostMassil
from route.serializers import RoutineSerializer
from customer.serializers import CustomerSerializer

class PostMassilSerializer(serializers.ModelSerializer):
    routine = RoutineSerializer(read_only=True)
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    user_name = serializers.CharField(source="user.nickname", read_only=True)
    user_character = serializers.IntegerField(source="user.character", read_only=True)

    class Meta:
        model = PostMassil
        fields = '__all__'
        read_only_fields = ["user"]
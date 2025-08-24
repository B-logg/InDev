from rest_framework import serializers
from .models import PostMassil
from route.serializers import RoutineSerializer
from customer.serializers import CustomerSerializer

class PostMassilSerializer(serializers.ModelSerializer):
    routine = RoutineSerializer(read_only=True)
    customer_id = serializers.IntegerField(source="customer.id", read_only=True)
    customer_name = serializers.CharField(source="customer.nickname", read_only=True)
    customer_character = serializers.IntegerField(source="customer.character", read_only=True)

    class Meta:
        model = PostMassil
        fields = '__all__'
        read_only_fields = ["customer"]
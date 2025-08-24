from rest_framework import serializers
from .models import PostMassil
from route.serializers import RoutineSerializer
from customer.serializers import CustomerSerializer
from customer.models import Customer

class PostMassilSerializer(serializers.ModelSerializer):
    routine = RoutineSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(source="customer", queryset=Customer.objects.all() ,write_only=True)
    customer_name = serializers.CharField(source="customer.nickname", read_only=True)
    customer_character = serializers.Field(source="customer.character.character_id", read_only=True)

    class Meta:
        model = PostMassil
        fields = '__all__'
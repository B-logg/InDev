from rest_framework import serializers
from .models import PostMassil
from route.serializers import RoutineSerializer
from customer.serializers import CustomerSerializer
from customer.models import Customer
from store.models import Store


class PostMassilSerializer(serializers.ModelSerializer):
    routine = RoutineSerializer(read_only=True)

    # 고객 정보
    customer_id = serializers.PrimaryKeyRelatedField(source="customer", queryset=Customer.objects.all() ,write_only=True, required=False)
    customer_name = serializers.CharField(source="customer.nickname", read_only=True)
    customer_character = serializers.IntegerField(source="customer.character.character_id", read_only=True)

    # 점주/가게 정보
    store_id = serializers.PrimaryKeyRelatedField(
        source="store", queryset=Store.objects.all(),
        write_only=True, required=False
    )
    store_name = serializers.CharField(source="store.name", read_only=True)



    class Meta:
        model = PostMassil
        fields = '__all__'
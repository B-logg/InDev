from rest_framework import serializers
from .models import Customer, Character

class CustomerSerializer(serializers.ModelSerializer):
    # character = CharacterSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = '__all__'
        
class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ['character_id', 'name', 'image']
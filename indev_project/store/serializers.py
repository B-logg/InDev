from rest_framework import serializers
from .models import Store, Analysis

class StoreSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Store
        fields = ['store_id', 'name', 'address', 'category', 'category_name']

class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = '__all__'

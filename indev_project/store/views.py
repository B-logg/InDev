from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Store, Analysis
from .serializers import StoreSerializer, AnalysisSerializer

class StoreView(APIView):
    def get(self, request, pk=None):
        if pk:
            store = get_object_or_404(Store, pk=pk)
            serializer = StoreSerializer(store)
            return Response(serializer.data)
        stores = Store.objects.all().values("store_id", "name", "address", "category", "category__name")
        return Response(list(stores))

    def post(self, request):
        serializer = StoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        store = get_object_or_404(Store, pk=pk)
        serializer = StoreSerializer(store, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        store = get_object_or_404(Store, pk=pk)
        store.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AnalysisView(APIView):
    def get(self, request, pk=None):
        if pk:
            analysis = get_object_or_404(Analysis, pk=pk)
            serializer = AnalysisSerializer(analysis)
        else:
            analyses = Analysis.objects.all()
            serializer = AnalysisSerializer(analyses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AnalysisSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        analysis = get_object_or_404(Analysis, pk=pk)
        serializer = AnalysisSerializer(analysis, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        analysis = get_object_or_404(Analysis, pk=pk)
        analysis.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

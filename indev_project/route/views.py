from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Routine, VisitRoutine
from .serializers import RoutineSerializer, VisitRoutineSerializer

# Routine CRUD
class RoutineView(APIView): 

    # 조회
    def get(self, request, pk=None):
        if pk:
            routine = get_object_or_404(Routine, pk=pk)
            serializer = RoutineSerializer(routine)
        else:
            routines = Routine.objects.all()
            serializer = RoutineSerializer(routines, many=True)
        return Response(serializer.data)
    
    # 생성
    def post(self, request):
        serializer = RoutineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 수정
    def put(self, request, pk):
        routine = get_object_or_404(Routine, pk=pk)
        serializer = RoutineSerializer(routine, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 삭제
    def delete(self, request, pk):
        routine = get_object_or_404(Routine, pk=pk)
        routine.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# VisitRoutine CRUD
class VisitRoutineView(APIView): 

    # 조회
    def get(self, request, pk=None):
        if pk:
            visit = get_object_or_404(VisitRoutine, pk=pk)
            serializer = VisitRoutineSerializer(visit)
        else:
            visits = VisitRoutine.objects.all()
            serializer = VisitRoutineSerializer(visits, many=True)
        return Response(serializer.data)

    # 생성
    def post(self, request):
        serializer = VisitRoutineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 수정
    def put(self, request, pk):
        visit = get_object_or_404(VisitRoutine, pk=pk)
        serializer = VisitRoutineSerializer(visit, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 삭제
    def delete(self, request, pk):
        visit = get_object_or_404(VisitRoutine, pk=pk)
        visit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
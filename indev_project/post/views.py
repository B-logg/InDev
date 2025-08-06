from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PostMassil
from .serializers import PostMassilSerializer

# CRUD
class PostMassilView(APIView):
    # 조회
    def get(self, request, pk=None):
        if pk:
            post = get_object_or_404(PostMassil, pk=pk)
            serializer = PostMassilSerializer(post)
        else:
            posts = PostMassil.objects.all()
            serializer = PostMassilSerializer(posts, many=True)
        return Response(serializer.data)
    
    # 생성
    def post(self, request):
        serializer = PostMassilSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 수정
    def put(self, request, pk):
        post = get_object_or_404(PostMassil, pk=pk)
        serializer = PostMassilSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 삭제
    def delete(self, request, pk):
        post = get_object_or_404(PostMassil, pk=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# post/views.py
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PostMassil
from .serializers import PostMassilSerializer

class PostMassilView(APIView):
    # 전체 조회 & 특정 조회
    def get(self, request, pk=None):
        if pk:
            post = get_object_or_404(PostMassil, pk=pk)
            serializer = PostMassilSerializer(post)
        else:
            posts = PostMassil.objects.all().order_by("-created_at")
            serializer = PostMassilSerializer(posts, many=True)
        return Response(serializer.data)

    # 생성
    def post(self, request):
        serializer = PostMassilSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save()
            return Response(PostMassilSerializer(post).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 수정
    def put(self, request, pk):
        post = get_object_or_404(PostMassil, pk=pk)
        serializer = PostMassilSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            post = serializer.save()
            return Response(PostMassilSerializer(post).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 삭제
    def delete(self, request, pk):
        post = get_object_or_404(PostMassil, pk=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

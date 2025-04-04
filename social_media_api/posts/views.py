
from django.shortcuts import render
from rest_framework import viewsets, status, Res
from rest_framework.viewsets import GenericViewSet
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.mixins import ListModelMixin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from .models import Post, Comment, Like
from notifications.models import Notification

# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'content']
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        
    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        post = generics.get_object_or_404(Post, pk=pk)
        user = request.user
        
        if Like.objects.filter(user=request.user, post=post).exists():
            return Response({"error": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)
        
        like = Like.objects.get_or_create(user=request.user, post=post)
        
        
        # Create Notification
        if post.author != user:
            Notification.objects.create(  recipient=post.author,
                actor=post.user,
                verb="liked your post",
                target=post 
            )
            
            return Response(LikeSerializer(like).data, status=status.HTTP_201_CREATED)
        
    
    @action(detail=True, methods=["post"])
    def unlike(self, request, pk=None):
        post = generics.get_object_or_404(Post, pk=None)
        
        like, created  = like.objects.get_or_create(user=request.user, post=post)
        if like:
            like.delete()
            return Response({"message": "Like removed."}, status=status.HTTP_200_OK)
        return Response({"error": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_pk']).order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        
        
class FeedViewSet(ListModelMixin, GenericViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()
        return Post.objects.filter(author__in=following_users).order_by('-created_at')

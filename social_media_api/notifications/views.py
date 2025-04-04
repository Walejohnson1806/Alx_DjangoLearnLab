
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework import permissions

# Create your views here.
class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        return Notification.objects.filter(recipient=user).order_by('-created_at')
    
    @action(detail=False, methods=['GET'])
    def unread(self, request):
        user = self.request.user
        notifications = Notification.objects.filter(recipient=user, read=False)
        return Response(NotificationSerializer(notifications, many=True).data)
    
    @action(detail=True, methods=['POST'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_queryset().filter(pk=pk).first()
        if notification:
            notification.read = True
            notification.save()
            return Response({"message": "Notification marked as read."}, status=200)
        return Response({"error": "Notification not found."}, status=404)

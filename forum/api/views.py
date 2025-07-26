#qs = Forum.objects.prefetch_related('comments') in the view for list.
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .serializers import ForumSerializer
from django.contrib.auth.models import User
from ..models import Forum, Comment, Reply

class ForumListApiView(generics.ListCreateAPIView):
    serializer_class = ForumSerializer
    permission_classes = [IsAuthenticated]

    #adding fetch for nested...
    def get_queryset(self):
        qs = Forum.objects.prefetch_related('comments').order_by('-created_at')
        return qs

    def get_serializer_context(self):
        return {'request': self.request}

    #adding the owner to the create and update post
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ForumDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer
    permission_classes = [IsAuthenticated]



    def get_serializer_context(self):
        return {'request': self.request}

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)
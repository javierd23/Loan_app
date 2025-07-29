from rest_framework.generics import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from .serializers import ForumSerializer, CommentSerializer
from django.contrib.auth.models import User
from ..models import Forum, Comment, Reply

#Forum list and create...
class ForumListApiView(generics.ListCreateAPIView):
    serializer_class = ForumSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    #pre-fetching not avoid overloading data...
    def get_queryset(self):
        qs = Forum.objects.prefetch_related('comments').order_by('-created_at')
        return qs

    #this is to add the request, so you can then use the self.request.user  to assign a user to it.
    def get_serializer_context(self):
        return {'request': self.request}

    #adding the owner to the creating and updating post for authenticated only, user can see but not create
    #if the user is not logged in or register.
    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(owner=self.request.user)
        else:
            raise PermissionDenied("In order to create a new forum, you must log in first.")

#Forum Detail...
class ForumRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ForumSerializer
    queryset = Forum.objects.all().order_by('-created_at')
    #permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        return {'request': self.request}

    #make sure that the owner of the forum is the only one that can update it...
    def perform_update(self, serializer):
        if serializer.instance.owner == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied("Your are either not the owner of the forum,"
                                   " or you are not entering right data.")

    # make sure that the owner of the forum is the only one that can delete it...
    def perform_destroy(self, instance):
        if self.request.user != instance.owner:
            raise PermissionDenied("You are not the owner of this forum.")
        instance.delete()

#Comment list and create
class CommentListCreateApiView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    #overriding the query so we can get the list of comment with the pk...
    def get_queryset(self):
        forum_pk = self.kwargs['pk']
        if not forum_pk:
            return Comment.objects.none()
        forum = get_object_or_404(Forum, pk=forum_pk)
        return Comment.objects.filter(forum=forum).order_by('-created_at')

    def get_serializer_context(self):
        return {'request': self.request }

    def perform_create(self, serializer):

        # Getting the creating based on the pk
        forum_pk = self.kwargs['pk']
        forum = get_object_or_404(Forum, pk=forum_pk)
        serializer.save(forum=forum, owner=self.request.user)


#we will get the comment of a forum and delete, update it.
class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Forum.objects.all()

    #modify the query since we need the comments of a specific forum...
    def get_object(self):
        forum_id = self.kwargs['pk']
        comment = get_object_or_404(Comment, id=forum_id)
        self.check_object_permissions(self.request, comment)
        return comment

    # adding the request...
    def get_serializer_context(self):
        return {'request': self.request}


    #adding the nested comment owner to the creating and updating, so we do not need to override the seria.
    def perform_update(self, serializer):

        #adding the owner of the comment on here, so no one else can upate if not the owner
        if serializer.instance.owner == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to update this comment.")

    # adding the owner of the comment on here, so no one else can upate if not the owner
    def perform_destroy(self, instance):
        if self.request.user != instance.owner:
            raise PermissionDenied("You are not the owner of this Comment.")
        instance.delete()








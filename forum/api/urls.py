from django.urls import path
from .views import ForumListApiView, CommentListCreateApiView, ForumRetrieveUpdateDestroyApiView, CommentRetrieveUpdateDestroyAPIView


urlpatterns = [
    path('', ForumListApiView.as_view(), name='forum-list'),
    path('<int:pk>/', ForumRetrieveUpdateDestroyApiView.as_view(), name='forum-detail'),
    path('<int:pk>/comment/', CommentListCreateApiView.as_view(), name='comment-list'),
    path('comment/<int:pk>/', CommentRetrieveUpdateDestroyAPIView.as_view(), name='forum-detail'),

]
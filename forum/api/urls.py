from django.urls import path
from .views import ForumListApiView, ForumDetailApiView

urlpatterns = [
    path('', ForumListApiView.as_view(), name='forum-list'),
    path('<int:pk>/', ForumDetailApiView.as_view(), name='forum-detail'),

]
from django.urls import path
from . import views

app_name = "forum"

urlpatterns = [
    path("forum/", views.ForumListView.as_view(), name="all"),
    path("forum/<int:pk>/", views.ForumDetailView.as_view(), name="forum_detail"),
    path("forum/create/", views.ForumCreateView.as_view(), name="forum_create"),
    path("forum/<int:pk>/update/", views.ForumUpdateView.as_view(), name="forum_update"),
    path("forum/<int:pk>/delete/", views.ForumDeleteView.as_view(), name="forum_delete"),

]
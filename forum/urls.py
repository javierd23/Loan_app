from django.urls import path
from . import views

app_name = "forum"

urlpatterns = [
    path("", views.ForumListView.as_view(), name="all"),
    path("forum/<int:pk>/", views.ForumDetailView.as_view(), name="forum_detail"),
    path("forum/create/", views.ForumCreateView.as_view(), name="forum_create"),
    path("forum/<int:pk>/update/", views.ForumUpdateView.as_view(), name="forum_update"),
    path("forum/<int:pk>/delete/", views.ForumDeleteView.as_view(), name="forum_delete"),

    #comments urls...
    path("forum/<int:pk>/comment/", views.CommentCreateView.as_view(), name="comment_create"),
    path("forum/<int:pk>/comment/delete", views.CommentDeleteView.as_view(), name="comment_delete"),
    path("forum/<int:pk>/comment/update", views.CommentUpdateView.as_view(), name="comment_update"),

    #reply urls...
    path('forum/<int:forum_pk>/comment/<int:comment_pk>/reply/', views.ReplyCreateView.as_view(), name="reply_create"),
    path('forum/<int:forum_pk>/<int:pk>/reply/update', views.ReplyUpdateView.as_view(), name="reply_update"),
    path('forum/<int:forum_pk>/<int:pk>/reply/delete', views.ReplyDeleteView.as_view(), name="reply_delete"),

    #replies and comments
    path("comment/<int:comment_pk>/reply", views.CommentReplyDetailView.as_view(), name="comment_reply_detail"),
    path("comment/<int:pk>/reply/delete", views.SingleRepyDeleteView.as_view(), name="single_reply_delete"),
    path("comment/<int:pk>/reply/update", views.SingleReplyUpdateView.as_view(), name="single_reply_update"),









]
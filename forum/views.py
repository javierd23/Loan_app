from django.shortcuts import render
from django.urls import reverse_lazy

from .models import Forum, Comment
from .owner import OwnerListView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView, OwnerDetailView


class ForumListView(OwnerListView):
    model = Forum



class ForumDetailView(OwnerDetailView):
    model = Forum
    template_name = "forum/forum_detail.html"

class ForumCreateView(OwnerCreateView):
    model = Forum
    template_name = "forum/forum_create.html"
    success_url= reverse_lazy('forum:all')

class ForumUpdateView(OwnerUpdateView):
    model = Forum
    template_name = "forum/forum_update.html"
    success_url = reverse_lazy('forum:all')

class ForumDeleteView(OwnerDeleteView):
    model = Forum
    template_name = "forum/forum_delete.html"
    success_url = reverse_lazy('forum:all')





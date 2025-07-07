from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from .models import Forum, Comment
from .owner import OwnerListView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView, OwnerDetailView


class ForumListView(OwnerListView):
    model = Forum



class ForumDetailView(OwnerDetailView):
    model = Forum
    template_name = "forum/forum_detail.html"


class ForumCreateView(OwnerCreateView):
    model = Forum
    fields = ['title', 'text']
    success_url= reverse_lazy('forum:all')

class ForumUpdateView(OwnerUpdateView):
    model = Forum
    fields = ['title', 'text']
    success_url = reverse_lazy('forum:all')

class ForumDeleteView(OwnerDeleteView):
    model = Forum
    success_url = reverse_lazy('forum:all')





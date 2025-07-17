from django.shortcuts import render
from .forms import CommentForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from .models import Forum, Comment
from .owner import OwnerListView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView, OwnerDetailView


class ForumListView(OwnerListView):
    model = Forum



class ForumDetailView(OwnerDetailView):
    model = Forum
    template_name = "forum/forum_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["CommentForm"] = CommentForm()
        context["comments"] = Comment.objects.filter(forum=self.object)
        return context


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





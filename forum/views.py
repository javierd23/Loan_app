from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from .forms import CommentForm
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from .models import Forum, Comment
from .owner import OwnerListView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView, OwnerDetailView



#Check owner.py to check the inherent from the generic view, with the modifications.
#List all the forums
class ForumListView(OwnerListView):
    model = Forum


class ForumDetailView(OwnerDetailView):
    model = Forum
    template_name = "forum/forum_detail.html"

    #adding the extra data, form of the comments and the comments itself
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


#Here we add the comment post

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):

        # We need to get the forum id, since we need to redict to the same page with the right forum...
        fq = get_object_or_404(Forum, pk=pk)

        form = CommentForm(request.POST) #wrap the post in the form
        if form.is_valid():
            comment = form.save(commit=False)
            comment.owner = request.user
            comment.forum = fq #here we get the forum_id for the comments to be fletch to the for forum id.
            comment.save()

            #We redirect to the detail forum and take the ride forum id, so it does the fletch
            return redirect(reverse("forum:forum_detail", args=[pk]))

        #If the form is not valid, we are taking the context and the form back.
        comments = Comment.objects.filter(forum=fq.id).order_by('-updated_at')
        context = {"form": form, "comments": comments, "pk": fq }

        return render(request, "forum/forum_detail.html", context)


class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "forum/comment_delete.html"

    #We need to take aditional data to the template, since we're redirecting to detail with the cancel buttom. so we need to add the pk
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["forum"] = Forum.objects.get(pk=self.object.forum_id)
        return context

    def get_success_url(self):
        #We need to invoke this func since with need to redirect to a url with a pk as detailview requires it.
        return reverse_lazy('forum:forum_detail', args=[self.object.forum_id])



class CommentUpdateView(OwnerUpdateView):
    model = Comment
    fields = ['title', 'text']
    template_name = "forum/comment_update.html"

    def get_success_url(self):
        # we need to get the pk as well
        return reverse_lazy('forum:forum_detail', args=[self.object.forum_id])









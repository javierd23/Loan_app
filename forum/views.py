#import URL_path, and redirect...
from keyword import kwlist

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse

#import form and models
from .models import Forum, Comment, Reply
from .forms import CommentForm, ReplyForm

#import generic views and base views.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from .owner import OwnerListView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView, OwnerDetailView

#Natural time import
from django.contrib.humanize.templatetags.humanize import naturaltime


#Check owner.py to check the inherent from the generic view, with the modifications.
#List all the forums
class ForumListView(OwnerListView):
    model = Forum

    #Ording the qs...
    def get_queryset(self):
        qs = Forum.objects.all().order_by('-created_at')
        return qs

#forum detail...
class ForumDetailView(OwnerDetailView):
    model = Forum
    template_name = "forum/forum_detail.html"

    #adding the extra data, form of the comments and the comments itself
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #forms..
        context["CommentForm"] = CommentForm()
        context["ReplyForm"] = ReplyForm()

        #fetching replies for each comment, so I can do comment.replies.all().
        # I use replies on the prefetching, bc that the relate_name in db
        comments = Comment.objects.filter(forum=self.object).prefetch_related('replies').order_by('-created_at')
        #Doing a loop to get the pagination in the replies...
        for comment in comments:
            comment.top_replies = comment.replies.all().order_by('-created_at')[:3]
        context["comments"] = comments

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


#Here I add the comment post, delete and update views
class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):

        # I need to get the forum id, since we need to redict to the same page with the right forum...
        fq = get_object_or_404(Forum, pk=pk)

        form = CommentForm(request.POST) #wrap the post in the form
        if form.is_valid():
            comment = form.save(commit=False)
            comment.owner = request.user
            comment.forum = fq #here we get the forum_id for the comments to be fletch to the for forum id.
            comment.save()

            #I redirect to the detail forum and take the ride forum id, so it does the fletch
            return redirect(reverse("forum:forum_detail", args=[pk]))

        #If the form is not valid, we are taking the context and the form back.
        comments = Comment.objects.filter(forum=fq.id).order_by('-updated_at')
        context = {"form": form, "comments": comments, "pk": fq }

        return render(request, "forum/forum_detail.html", context)


class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "forum/comment_delete.html"

    #I need to take aditional data to the template, since we're redirecting to detail with the cancel buttom. so we need to add the pk
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["forum"] = Forum.objects.get(pk=self.object.forum_id)
        return context

    def get_success_url(self):
        #I need to invoke this func since with need to redirect to a url with a pk as detailview requires it.
        return reverse_lazy('forum:forum_detail', args=[self.object.forum_id])



class CommentUpdateView(OwnerUpdateView):
    model = Comment
    fields = ['text']
    template_name = "forum/comment_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["forum"] = Forum.objects.get(pk=self.object.forum_id)
        return context

    def get_success_url(self):
        # I need to get the pk as well
        return reverse_lazy('forum:forum_detail', args=[self.object.forum_id])


#reply views...
class ReplyCreateView(LoginRequiredMixin, View):

    def post(self, request, forum_pk, comment_pk):
        #for this creating, I will get two pk to handle nested relations
        forum_id = get_object_or_404(Forum, pk=forum_pk) #grap the forum.
        comments_instance = get_object_or_404(Comment, pk=comment_pk, forum__pk=forum_pk)

        #assigning an owner, and comments to the reply and redirecting to forum details...
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.comment = comments_instance
            reply.owner = request.user
            reply.save()
            return redirect(reverse("forum:forum_detail", args=[forum_pk]))
        #rendering to details with erros if invalid reply...
        all_comments_forum = Comment.objects.filter(forum=forum_id).prefetch_related('replies')
        form = ReplyForm()
        context = {"form": form, "comments": all_comments_forum, "pk": forum_id}
        return render(request, "forum/reply.html", context)


class ReplyUpdateView(OwnerUpdateView):
    model = Reply
    form_class = ReplyForm
    template_name = "forum/reply_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["forum"] = self.object.comment.forum #I grap the instance reply traverse from Reply -> Comment -> Forum
        context["comment"] = self.object.comment #I grap the instance reply traverse from Reply -> Comment

        return context

    def get_success_url(self):
        forum_id = self.object.comment.forum.id
        return reverse_lazy('forum:forum_detail', args=[forum_id])

class ReplyDeleteView(OwnerDeleteView):
    model = Reply
    template_name = "forum/reply_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["forum"] = self.object.comment.forum

        return context

    def get_success_url(self):
        forum_id = self.object.comment.forum.id
        return reverse_lazy('forum:forum_detail', args=[forum_id])


#builing a detail view for comment to prefetch replies.
class CommentReplyDetailView(View):
    template_name = "forum/comment_reply_detail.html"

    def get(self, request, comment_pk):
        comment = get_object_or_404(Comment, pk=comment_pk)
        replies = Reply.objects.filter(comment=comment).order_by('-created_at')

        form = ReplyForm()
        context = {"comment": comment, "pk": comment_pk, "form": form, "replies": replies}
        return render(request, self.template_name, context)

    def post(self, request, comment_pk):
        comment = get_object_or_404(Comment, pk=comment_pk)

        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.comment = comment
            reply.owner = request.user
            reply.save()
            return redirect(reverse("forum:comment_reply_detail", args=[comment_pk]))

        context = {"comment": comment, "pk": comment_pk, "form": form}
        return render(request, self.template_name, context)


class SingleRepyDeleteView(OwnerDeleteView):
    model = Reply
    template_name = "forum/single_reply_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment"] = self.object.comment_id
        return context

    def get_success_url(self):
        comment_id = self.object.comment.id
        return reverse_lazy('forum:comment_reply_detail', args=[self.object.comment_id])


class SingleReplyUpdateView(OwnerUpdateView):
    model = Reply
    form_class = ReplyForm
    template_name = "forum/single_reply_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment"] = self.object.comment_id
        return context

    def get_success_url(self):
        comment_id = self.object.comment.id
        return reverse_lazy('forum:comment_reply_detail', args=[self.object.comment_id])











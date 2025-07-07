from django import forms

from loan_project.mysite.forum.models import Comment


class FormComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
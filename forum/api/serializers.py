from rest_framework import serializers, request
from django.contrib.auth.models import User
from ..models import Forum, Comment, Reply



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')
        read_only_fields = ('email', 'username')


class ReplySerializer(serializers.ModelSerializer):

    class Meta:
        model = Reply
        fields = ['text']
        read_only_fields = ['created_at', 'updated_at']

class CommentSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    reply = ReplySerializer(read_only=True, many=True, required=False)
    forum = serializers.StringRelatedField(read_only=True)


    class Meta:
        model = Comment
        fields = ['forum','id', 'text', 'owner', 'created_at', 'reply']
        read_only_fields = ['created_at', 'owner', 'reply']


class ForumSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    comment = CommentSerializer(many=True, required=False, source='comment_set', read_only=True)

    class Meta:
        model = Forum
        fields = ['id', 'title', 'text', 'owner', 'created_at', 'comment']
        read_only_fields = ['created_at', 'id']


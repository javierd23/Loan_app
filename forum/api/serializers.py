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

    class Meta:
        model = Comment
        fields = ['text', 'owner', 'created_at', 'reply']
        read_only_fields = ['created_at', 'owner']




class ForumSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, source='comment_set')

    class Meta:
        model = Forum
        fields = ['title', 'text', 'comments', 'created_at']
        read_only_fields = ['created_at']


    def create(self, validated_data):
        request = self.context.get('request')
        comments_data = validated_data.pop('comment_set', [])
        forum = Forum.objects.create(**validated_data)

        for comment_data in comments_data:
            Comment.objects.create(forum=forum,owner=request.user, **comment_data)
        return forum

    def update(self, instance, validated_data):
        comments_data = validated_data.pop('comment_set')
        comment = instance.comments
        instance.forum = validated_data.get('forum', instance.forum)
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.comments = validated_data.get('comments', instance.comments)
        instance.save()
        return instance









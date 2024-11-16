from rest_framework import serializers
from .models import Subreddit, Post, Comment

class SubredditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subreddit
        fields = ["id", "name", "description", "created_at"]

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "content", "created_at", "subreddit", "author"]

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "post", "author", "content", "created_at"]

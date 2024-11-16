from django import forms
from .models import Post, Subreddit, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'subreddit']

class SubredditForm(forms.ModelForm):
    class Meta:
        model = Subreddit
        fields = ['name', 'description']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

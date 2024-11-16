from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Subreddit, Post, Comment
from .forms import SubredditForm, PostForm
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SubredditSerializer, PostSerializer, CommentSerializer

# Home view for rendering the main page
def home(request):
    return render(request, 'reddit/home.html')

# View for rendering subreddit details (HTML)
def subreddit_detail(request, id):
    subreddit = get_object_or_404(Subreddit, id=id)
    posts = Post.objects.filter(subreddit=subreddit)
    context = {
        'subreddit': subreddit,
        'posts': posts,
    }
    return render(request, 'reddit/subreddit_detail.html', context)

def subreddit_list(request):
    subreddits = Subreddit.objects.all()
    return render(request, 'reddit/subreddit_list.html', {'subreddits': subreddits})

def upvote_post(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        if request.user in post.upvotes.all():
            post.upvotes.remove(request.user)
            upvoted = False
        else:
            post.upvotes.add(request.user)
            upvoted = True
        return JsonResponse({"success": True, "upvotes_count": post.upvotes.count(), "upvoted": upvoted})


# View for creating a subreddit (HTML form)
def create_subreddit(request):
    if request.method == "POST":
        form = SubredditForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('subreddit_list'))  # Redirect to subreddit list after creation
    else:
        form = SubredditForm()

    return render(request, 'reddit/create_subreddit.html', {'form': form})

# View for creating a post in a subreddit (HTML form)
def create_post(request, subreddit_id):
    subreddit = get_object_or_404(Subreddit, id=subreddit_id)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.subreddit = subreddit
            post.author = request.user
            post.save()
            return HttpResponseRedirect(reverse('subreddit_detail', args=[subreddit.id]))  # Redirect to subreddit details
    else:
        form = PostForm()

    return render(request, 'reddit/create_post.html', {'form': form, 'subreddit': subreddit})

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    comments = Comment.objects.filter(post=post)
    context = {
        'post': post,
        'comments': comments,
    }
    return render(request, 'reddit/post_detail.html', context)

def add_comment(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Comment.objects.create(post=post, author=request.user, content=content)
            return HttpResponseRedirect(reverse('post_detail', args=[id]))
    return render(request, 'reddit/add_comment.html', {'post': post})



# API View for listing all subreddits
class SubredditListAPI(APIView):
    def get(self, request):
        subreddits = Subreddit.objects.all()
        serializer = SubredditSerializer(subreddits, many=True)
        return Response(serializer.data)

# API View for listing all posts in a subreddit
class SubredditPostsAPI(APIView):
    def get(self, request, subreddit_id):
        posts = Post.objects.filter(subreddit_id=subreddit_id)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

# API View for creating a new subreddit
class CreateSubredditAPI(APIView):
    def post(self, request):
        serializer = SubredditSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# API View for creating a new post in a subreddit
class CreatePostAPI(APIView):
    def post(self, request, subreddit_id):
        subreddit = get_object_or_404(Subreddit, id=subreddit_id)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(subreddit=subreddit, author=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# API View for listing comments for a post
class PostCommentsAPI(APIView):
    def get(self, request, post_id):
        comments = Comment.objects.filter(post_id=post_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

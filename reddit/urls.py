from django.urls import path
from . import views

urlpatterns = [
    # API routes
    path("api/subreddits/", views.SubredditListAPI.as_view(), name="api_subreddits"),
    path("api/subreddit/<int:subreddit_id>/posts/", views.SubredditPostsAPI.as_view(), name="api_subreddit_posts"),
    path("api/subreddit/create/", views.CreateSubredditAPI.as_view(), name="api_create_subreddit"),
    path("api/subreddit/<int:subreddit_id>/create_post/", views.CreatePostAPI.as_view(), name="api_create_post"),
    path("api/post/<int:post_id>/comments/", views.PostCommentsAPI.as_view(), name="api_post_comments"),
    path("post/<int:post_id>/upvote/", views.upvote_post, name="upvote_post"),

    # HTML routes
    path("", views.home, name="home"),
    path("subreddit/", views.subreddit_list, name="subreddit_list"),  # Added this route
    path("subreddit/<int:id>/", views.subreddit_detail, name="subreddit_detail"),
    path("subreddit/create/", views.create_subreddit, name="create_subreddit"),
    path("subreddit/<int:subreddit_id>/create_post/", views.create_post, name="create_post"),
    path("post/<int:id>/", views.post_detail, name="post_detail"),
    path("post/<int:id>/add_comment/", views.add_comment, name="add_comment"),
]

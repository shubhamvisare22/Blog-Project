from django.db import models
from django.contrib.auth.models import User
from accounts.models import UserProfile


class Blog(models.Model):
    """
    Model representing a blog post.

    Attributes:
        name (str): The title of the blog.
        content (str): The content or body of the blog.
        author (User): The user who authored the blog.
        created_date (datetime): The date and time when the blog was created.
        modified_date (datetime): The date and time when the blog was last modified.
    """

    name = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} by {self.author.user.username}"


class Comment(models.Model):
    """
    Model representing a comment on a blog post.

    Attributes:
        blog (Blog): The blog post the comment is associated with.
        user (User): The user who wrote the comment.
        comment_text (str): The content of the comment.
        created_date (datetime): The date and time when the comment was created.
        modified_date (datetime): The date and time when the comment was last modified.
    """

    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.blog.name}"


class Response(models.Model):
    """
    Model representing a response (like or dislike) to a blog post.

    Attributes:
        blog (Blog): The blog post the response is associated with.
        user (User): The user who gave the response.
        like_or_not (bool): True if it's a like, False if it's a dislike.
        response_date (datetime): The date and time when the response was given.
    """

    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like_or_not = models.BooleanField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Response by {self.user.username} on {self.blog.name}"


# USERS = [
#     ('user', 'Reader'), ('author', 'Author')
# ]
# User.add_to_class("user_role", models.CharField(
#     max_length=10, choices=USERS, default='user'))

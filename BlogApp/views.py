from django.shortcuts import render, redirect
from .models import Blog, Response, User, Comment
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.db.models import Count, Q
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test


# def user_dashboard(request):
#     if request.user.is_authenticated:
#         if request.user.userprofile.is_author:
#             return render(request, "author_dashboard.html")
#         else:
#             return render(request, "user_dashboard.html")
#     else:
#         return render(request, "home.html")


class ProfileView(View):
    template_name = 'profile.html'
    author_template = "author_dashboard.html"
    reader_template = "user_dashboard.html"

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/auth/login')

        if request.user.userprofile.is_author:
            template = self.author_template
        else:
            template = self.reader_template

        return render(request, template)


def is_author(user):
    return user.is_authenticated and user.userprofile.is_author


class AuthorRequiredMixin:
    @method_decorator(user_passes_test(is_author))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


@method_decorator(csrf_exempt, name='dispatch')
class BlogView(LoginRequiredMixin, AuthorRequiredMixin, View):
    def create_blog(self, request):
        if request.method != "POST":
            return JsonResponse({"status": 0, "msg": "Invalid request method"})

        name = request.POST.get("name")
        content = request.POST.get("content")

        try:
            blog = Blog.objects.create(
                name=name, content=content, author=request.user.userprofile)
            return JsonResponse({"status": 1, "blog_id": blog.id})

        except Exception as e:
            return JsonResponse({"status": 0, "msg": str(e)})

    def update_blog(self, request, blog_id):
        if request.method != "POST":
            return JsonResponse({"status": 0, "msg": "Invalid request method"})

        name = request.POST.get("name")
        content = request.POST.get("content")

        try:
            blog = get_object_or_404(
                Blog, id=blog_id, author=request.user.userprofile)
            blog.name = name
            blog.content = content
            blog.save()
            return JsonResponse({"status": 1})

        except Exception as e:
            return JsonResponse({"status": 0, "msg": str(e)})

    def delete_blog(self, request, blog_id):
        if request.method != "POST":
            return JsonResponse({"status": 0, "msg": "Invalid request method"})

        try:
            blog = get_object_or_404(
                Blog, id=blog_id, author=request.user.userprofile)
            blog.delete()
            return JsonResponse({"status": 1})

        except Exception as e:
            return JsonResponse({"status": 0, "msg": str(e)})

    def show_blog(self, request, blog_id):
        if request.method != "GET":
            return JsonResponse({"status": 0, "msg": "Invalid request method"})

        try:
            blog = get_object_or_404(Blog, id=blog_id)
            data = {
                "status": 1,
                "blog_id": blog.id,
                "name": blog.name,
                "content": blog.content,
                "author": blog.author.user.username,
                "created_date": blog.created_date,
                "modified_date": blog.modified_date
            }
            return JsonResponse(data)

        except Exception as e:
            return JsonResponse({"status": 0, "msg": str(e)})
    
    def show_all_blogs(self,request):
        print(request.user.username)
        blog_obj = Blog.objects.filter(author__user__id = request.user.id).values()
        return JsonResponse({"blogs":list(blog_obj)}, safe=False)

    def blogs_by_author(self, request, author_id):
        # 1. Blogs of a Specific author/User with likes, dislikes, comments count
        blogs = Blog.objects.filter(author__user__id=author_id)
        data = self._get_blog_data(blogs)
        return JsonResponse(data, safe=False)

    def top_commented_blogs(self, request, author_id):
        # 2. Top 5 commented Blogs of the user
        blogs = Blog.objects.filter(author__user__id=author_id).annotate(
            comment_count=Count('comment')).order_by('-comment_count')[:5]
        data = [{'blog_id': blog.id, 'name': blog.name,
                 'comment_count': blog.comment_count, 'blog_content':blog.content} for blog in blogs]
        return JsonResponse(data, safe=False)

    def top_liked_disliked_blogs(self, request, author_id):
        # 3. Top 5 Liked and Top 5 disliked Blogs in the last 3 days
        three_days_ago = timezone.now() - timezone.timedelta(days=3)

        top_liked = Blog.objects.filter(author__user__id=author_id, response__like_or_not=True,
                                        response__created_date__gte=three_days_ago) \
            .annotate(likes_count=Count('response', filter=Q(response__like_or_not=True))) \
            .order_by('-likes_count')[:5]

        top_disliked = Blog.objects.filter(author__user__id=author_id, response__like_or_not=False,
                                           response__created_date__gte=three_days_ago) \
            .annotate(dislikes_count=Count('response', filter=Q(response__like_or_not=False))) \
            .order_by('-dislikes_count')[:5]

        liked_data = self._get_blog_data(top_liked, likes=True)
        disliked_data = self._get_blog_data(top_disliked, dislikes=True)

        return JsonResponse({'top_liked': liked_data, 'top_disliked': disliked_data})

    def my_recent_liked_blogs(self, request):
        # 4. My recent 5 liked blogs
        liked_blogs = Response.objects.filter(
            user=request.user, like_or_not=True).order_by('-created_date')[:5]
        data = self._get_blog_data(liked_blogs, likes=True)
        return JsonResponse(data, safe=False)

    def my_comment_history_for_blogs(self, request, blog_id):
        # 5. My comment history for specific blogs
        comments = Comment.objects.filter(user=request.user, blog__id=blog_id)
        data = [{'comment_id': comment.id, 'comment_text': comment.comment_text, 'created_date': comment.created_date}
                for comment in comments]
        return JsonResponse(data, safe=False)

    def my_comment_history_for_author(self, request, author_id):
        # 6. My comment history for a particular author
        comments = Comment.objects.filter(
            user=request.user, blog__author__user__id=author_id)
        data = [{'comment_id': comment.id, 'comment_text': comment.comment_text, 'created_date': comment.created_date}
                for comment in comments]
        return JsonResponse(data, safe=False)

    def _get_blog_data(self, blogs, likes=False, dislikes=False):
        data = []
        for blog in blogs:
            likes_count = Response.objects.filter(
                blog=blog, like_or_not=True).count() if likes else 0
            dislikes_count = Response.objects.filter(
                blog=blog, like_or_not=False).count() if dislikes else 0
            comments_count = Comment.objects.filter(blog=blog).count()

            data.append({
                'blog_id': blog.id,
                'name': blog.name,
                'likes_count': likes_count,
                'dislikes_count': dislikes_count,
                'comments_count': comments_count,
            })
        return data

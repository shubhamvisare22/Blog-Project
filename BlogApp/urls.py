from django.urls import path 
from . import views
blog_view = views.BlogView()
print(blog_view)

urlpatterns = [
    
    # path("user-dashboard", views.user_dashboard, name="user_dashboard"),
    # path("create-blog", views.create_blog, name="create_blog"),
    
    # ----------------------------- Author Blog Views --------------------------------
    path('create/', blog_view.create_blog, name='create_blog'),
    path('update/<int:blog_id>/', blog_view.update_blog, name='update_blog'),
    path('delete/<int:blog_id>/', blog_view.delete_blog, name='delete_blog'),
    path('show/<int:blog_id>/', blog_view.show_blog, name='show_blog'),
    path('by_author/<int:author_id>/', blog_view.blogs_by_author, name='blogs_by_author'),
    path('top_commented/<int:author_id>/', blog_view.top_commented_blogs, name='top_commented_blogs'),
    path('top_liked_disliked/<int:author_id>/', blog_view.top_liked_disliked_blogs, name='top_liked_disliked_blogs'),
    path('my_recent_liked/', blog_view.my_recent_liked_blogs, name='my_recent_liked_blogs'),
    path('my_comment_history/<int:blog_id>/', blog_view.my_comment_history_for_blogs, name='my_comment_history_for_blogs'),
    path('my_comment_history_for_author/<int:author_id>/', blog_view.my_comment_history_for_author, name='my_comment_history_for_author'),
]
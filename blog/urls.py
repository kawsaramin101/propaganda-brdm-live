from django.urls import path
from .views import (index, 
                    detail, 
                    create_blog_post, 
                    update_blog_post, 
                    delete_post, 
                    createcomment, 
                    create_comment_reply, 
                    category_post, 
                    like_view, 
                    dislike_view)

app_name = 'blog'


urlpatterns = [
    path('', index, name='index'),
    
    path('category/<str:category>', category_post, name='category_post'),
    
    path('detail/<int:id>', detail, name='detail'),
    path('create_blog/', create_blog_post, name='create_blog_post'),
    path('update_blog/<int:id>', update_blog_post, name='update-blog-post'),
    path('delete_blog/<int:id>', delete_post, name='delete-blog-post'),
    
    path('post/<int:id>/add_comment/', createcomment, name='create_comment'),
    path('comment/<int:id>/reply/', create_comment_reply, name='create_comment_reply'),
    
    path('like/<int:id>', like_view, name="like"),
    path('dislike/<int:id>', dislike_view, name="dislike"),
    
]
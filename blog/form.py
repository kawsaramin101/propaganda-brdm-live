from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from .models import BlogPost, BlogComment, CommentReply


class CreateBlogPost(ModelForm):
    class Meta:
        model = BlogPost 
        fields = ['title', 'body', 'category']
        
        

class CreateBlogComment(ModelForm):
    class Meta:
        model = BlogComment
        fields = ['body']
        
        
        
class CreateBlogCommentReply(ModelForm):
    class Meta:
        model = CommentReply
        fields = ['body']


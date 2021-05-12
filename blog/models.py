from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class BlogPostCategory(models.Model):
    category = models.CharField(max_length=200)
    
    def __str__(self):
        return self.category
    


class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author',)
    title = models.CharField(max_length=200)
    body = models.TextField()
    category = models.ManyToManyField(BlogPostCategory)
    date_created = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name="blog_post_likes", )
    dislikes = models.ManyToManyField(User, related_name="blog_post_dislikes", )
    
    class Meta:
        ordering = ['is_published']
    
    def __str__(self):
        return self.title
        
    def total_likes(self):
        return self.likes.count()
        
    def total_dislikes(self):
        return self.dislikes.count()
       
       
class BlogComment(models.Model):
    commented_on = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments',)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commentauthor',)
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    liked = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-date_created']
    
    def __str__(self):
        return  '%s - %s' % (self.commented_on.title, self.body)
     
     
     
class CommentReply(models.Model):
    replied_on = models.ForeignKey(BlogComment, on_delete=models.CASCADE, related_name='replies',)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commentreplyauthor',)
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    liked = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-date_created']
    
    def __str__(self):
        return  '%s - %s' % (self.commented_on.body[:10], self.body)
     
     
  
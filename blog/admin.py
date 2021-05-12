from django.contrib import admin
from .models import BlogPostCategory,BlogPost, BlogComment
# Register your models here.

class CommentInline(admin.StackedInline):
    model = BlogComment 
    extra = 3
    
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['author', 'title', 'is_published']
    inlines = [CommentInline]

admin.site.register(BlogPostCategory)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(BlogComment)
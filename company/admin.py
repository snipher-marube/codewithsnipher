from django.contrib import admin

from .models import Profile, Post, PostComment, Tag, Category

class CommentItemInline(admin.TabularInline):
    model = PostComment
    raw_id_fields = ['post']

class ProfileAdmin(admin.ModelAdmin):
    list_filter = ['first_name', 'last_name', 'email', 'twitter']
    search_fields = ['first_name', 'last_name', 'email', 'twitter']
    list_display = ['user', 'first_name', 'last_name', 'email', 'twitter']

class PostAdmin(admin.ModelAdmin):
    list_display = ['headline', 'slug', 'active', 'featured', 'category']
    search_fields = ['headline', 'sub_headline', 'tags', 'category']
    list_filter = ['headline', 'tags', 'category']
    prepopulated_fields = {'slug': ('headline',)}

class PostCommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'body', 'created']
    list_filter = ['author', 'post', 'created']
    search_fields = ['author', 'post']

class TagAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name']
    list_filter = ['name']

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title', 'slug']
    list_filter = ['title']
    prepopulated_fields ={'slug': ('title',)}

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostComment, PostCommentAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
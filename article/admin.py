from django.contrib import admin

# Register your models here.
from .models import ArticleColumn,ArticlePost
class ArticlePostAdmin(admin.ModelAdmin):
    list_display = ['author','title','body','create','total_views']


admin.site.register(ArticlePost,ArticlePostAdmin)
admin.site.register(ArticleColumn)
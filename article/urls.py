from os import name
from django.urls import path
from . import views
import article

app_name = 'article'

urlpatterns = [
    # path('article-list/',article_list,name='article_list'),
    path('article-list/', views.article_list, name='article_list'),
    path('article-list2/',views.article_list2,name='article_list2'),
    path('article-detail/<int:id>/',views.article_detail,name='article_detail'),
    path('article-create/',views.article_create,name='article_create'),
    path('article-delete/<int:id>/',views.article_delete,name='article_delete'),
    path('article-update/<int:id>/',views.article_update,name='article_update'),
    path('increase-likes/<int:id>/',views.IncreaseLikesView.as_view(),name='increase_likes')
]
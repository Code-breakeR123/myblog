from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [
    # 发表评论
    # 评论必须关联在某篇具体的博文里，因此传入博文的id，方便后续调用。
    path('post-comment/<int:article_id>/',views.post_comment,name='post_comment'),
    path('post-comment/<int:article_id>/<int:parent_comment_id>',views.post_comment,name='comment_reply')
]
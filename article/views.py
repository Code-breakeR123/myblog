from comment.models import Comment
from django.core import paginator
from article.models import ArticleColumn, ArticlePost
from django.shortcuts import render , get_object_or_404
# Create your views here.
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from comment.forms import CommentForm
from django.views import View

# 视图函数
'''
def article_list(request):
    # 取出所有博客文章
    article_list = ArticlePost.objects.all()
    # 每页显示一篇文章
    paginator = Paginator(article_list,6)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)

    context = {
        'articles':articles
    }
    return render(request,'article/list.html',context)
'''
# ---------------------------------------------------------------------
def article_list2(request):
    # 根据get请求中查询条件
    search = request.GET.get('search')
    order = request.GET.get('order')
    column  = request.GET.get('column')
    tag = request.GET.get('tag')

    # 初始化查询集
    article_list = ArticlePost.objects.all()

    # 搜索查询集
    if search:
        article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
    else:
        search = ""

    # 标签查询
    if tag and tag != 'None':
        article_list = article_list.filter(tags__name__in=[tag])

    # 栏目查询
    if column is not None and column.isdigit():
        article_list = article_list.filter(column=column)
    
    # 排序
    if order == 'total_views':
        article_list = article_list.order_by('-total_views')
    
    '''
    # 返回不同排序的对象数组
    if request.GET.get('order') == "total_views":
        article_list = ArticlePost.objects.all().order_by('-total_views')
        order = 'total_views'
    else:
        article_list = ArticlePost.objects.all()
        order = 'normal'
    '''
    # 每页显示6篇文章
    paginator = Paginator(article_list,6)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)
    context = {
        'articles':articles,
        'order':order,
        'search':search,
        'column':column,
        'tag':tag
    }
    return render(request,'article/list2.html',context)

# ---------------------------------------------------------------------
# 重写文章列表 不创建新的视图/路由，而是将排序功能融合到已有的视图/路由中。
def article_list(request):
    # 根据get请求中查询条件
    search = request.GET.get('search')
    order = request.GET.get('order')
    column  = request.GET.get('column')
    tag = request.GET.get('tag')

    # 初始化查询集
    article_list = ArticlePost.objects.all()

    # 搜索查询集
    if search:
        article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
    else:
        search = ""

    # 标签查询
    if tag and tag != 'None':
        article_list = article_list.filter(tags__name__in=[tag])

    # 栏目查询
    if column is not None and column.isdigit():
        article_list = article_list.filter(column=column)
    
    # 排序
    if order == 'total_views':
        article_list = article_list.order_by('-total_views')
    '''
    # 返回不同排序的对象数组
    if request.GET.get('order') == "total_views":
        article_list = ArticlePost.objects.all().order_by('-total_views')
        order = 'total_views'
    else:
        article_list = ArticlePost.objects.all()
        order = 'normal'
    '''
    # 每页显示6篇文章
    paginator = Paginator(article_list,6)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)
    context = {
        'articles':articles,
        'order':order,
        'search':search,
        'column':column,
        'tag':tag
    }
    return render(request,'article/list.html',context)


# ---------------------------------------------------------------------
import markdown
def article_detail(request,id):
    # 取出相应id的文章
    article = get_object_or_404(ArticlePost, id=id)
    # 取出评论
    comments = Comment.objects.filter(article=id)
    # 浏览量+1
    article.total_views += 1
    article.save(update_fields=["total_views"])
    comment_form = CommentForm()

    # 将markdown语法渲染成html样式
    md = markdown.Markdown(
        extensions=[
            # 包含缩写 表格等常用扩展
            'markdown.extensions.extra',
            # 语法高亮拓展
            'markdown.extensions.codehilite',
            # 'markdown.extensions.highlight',
            # 目录扩展
            'markdown.extensions.toc'
    ])
    article.body = md.convert(article.body)
    # 需要传递给模板的对象
    context = {'article':article,'toc':md.toc,'comments':comments,'comment_form':comment_form}
    # 载入模板，返回对象
    return render(request,'article/detail.html',context)

# 引入重定向
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ArticlePostForm
from django.contrib.auth.models import User

# ---------------------------------------------------------------------
# 写文章的视图
from django.contrib.auth.decorators import login_required
@login_required(login_url='/userprofile/login/')
def article_create(request):
    # 判断用户是否提交数据
    if request.method == 'POST':
        # 将提交的数据赋值给表单实例中
        article_post_form = ArticlePostForm(request.POST,request.FILES)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库
            new_article = article_post_form.save(commit=False)
            # 指定数据库中 id=1的用户为作者
            # 如果你进行过删除数据表的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入此用户的id
            ''' new_article.author = User.objects.get(id=1)'''  
            # 指定目前登录的用户为作者
            new_article.author = User.objects.get(id=request.user.id)

            if request.POST['column'] != "none":
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])

            # 将新文章保存到数据库中
            new_article.save()
            # 保存 tags 一对多的关系
            article_post_form.save_m2m()
            # 完成后返回到文章列表
            return redirect('article:article_list')
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse('表单内有错误，请重新填写')
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文
        columns = ArticleColumn.objects.all()
        context = {
            'article_post_form':article_post_form,
            'columns':columns
        }
        # 返回模板
        return render(request,'article/create.html',context)

# ---------------------------------------------------------------------
def article_delete(request,id):
    # 根据ID 获取需要删除的文章
    article = ArticlePost.objects.get(id=id)
    # 调用delete删除文章
    article.delete()
    # 完成时删除后返回文章列表
    return redirect('article:article_list')

# ---------------------------------------------------------------------
def article_update(request,id):
    '''
    更新文章的视图函数
    通过post方法提交表单，更新title body字段 
    GET方法进入初始表单页面
    id:文章的 id
    '''
    # 获取需要修改的具体文章对象
    article = ArticlePost.objects.get(id=id)

    # 过滤非作者的用户
    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章")

    # 判断用户是否为POST提交表单数据
    if request.method == 'POST':
        # 将提交的表单数据赋值到表单实例中
        article_post_form = ArticlePostForm(request.POST,request.FILES)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存新写入的 title body数据并保存
            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None
            if request.FILES.get('avatar'):
                article.avatar = request.FILES.get('avatar')
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.tags.set(*request.POST.get('tags').split(','), clear=False)
            article.save()
            # 完成后返回到修改后文章中,需要传入文章id值
            return redirect('article:article_detail',id=id)
        # 如果数据不合法,返回错误信息
        else:
            return HttpResponse('表单内容有误,请重新填写')
        
    # 如果用户get请求获取数据    
    else:
        # 创建表单实例类
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        # 赋值上下文,将article文章对象也传递进去,以便提取旧的内容
        context = {
            'article':article,
            'article_post_form':article_post_form,
            'columns':columns,
            'tags': ','.join([x for x in article.tags.names()]),
            }
        # 将响应返回到模板中
        return render(request,'article/update.html',context)

class IncreaseLikesView(View):
    def post(self, request, *args, **kwargs):
        article = ArticlePost.objects.get(id=kwargs.get('id'))
        article.likes += 1
        article.save()
        return HttpResponse('success')
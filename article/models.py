from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models.fields import PositiveBigIntegerField, PositiveIntegerField
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager
from PIL import Image
# from imagekit.models import ProcessedImageField
# from imagekit.processors import ResizeToFit

class ArticleColumn(models.Model):
    '''栏目的model'''
    # 栏目标题:
    title = models.CharField(max_length=100,blank=True,verbose_name='栏目标题')
    # 创建时间
    created = models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    class Meta:
        verbose_name = "栏目"
    def __str__(self):
        return self.title


class ArticlePost(models.Model):
    # 文章作者
    author = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='作者')

    # 文章标签
    tags = TaggableManager(blank=True,verbose_name='文章标签')

    # 文章标题。models.CharField
    title = models.CharField(max_length=100,verbose_name='文章标题')

    # 正文TextField
    body = models.TextField(verbose_name='正文')

    # 文章创建时间，创建数据时默认写入当前时间
    create = models.DateTimeField(default=timezone.now,verbose_name='创建时间')

    # 文章更新时间。 参数auto_now = True 指定每次数据更新时自动写入当前时间
    update = models.DateTimeField(auto_now=True,verbose_name='最新更新时间')

    # 文章浏览量
    total_views = models.PositiveIntegerField(default=0,verbose_name='浏览量')

    # 标题图
    avatar = models.ImageField(upload_to='article/%Y%m%d',blank=True,verbose_name='标题图')

    # 点赞
    likes = models.PositiveIntegerField(default=0)

    # 保存时处理图片
    def save(self,*args,**kwrags):
        # 调用原有save()
        article = super(ArticlePost,self).save(*args,**kwrags)
        # 固定宽度缩放图片大小
        if self.avatar and not kwrags.get('update_fields'):
            image = Image.open(self.avatar)
            (x,y) = image.size
            new_x = 400 
            new_y = int(new_x * (y / x))
            resized_image = image.resize((new_x,new_y),Image.ANTIALIAS)
            resized_image.save(self.avatar.path)
        return article

    # avatar = ProcessedImageField(
    #     upload_to='article/%Y%m%d',
    #     processors=[ResizeToFit(width=400)],
    #     format='JPEG',
    #     options={'quality': 100},
    # )
    # 文章栏目一对多的外键
    column = models.ForeignKey(
        ArticleColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article',
        verbose_name='文章栏目',
    )

    def get_absolute_url(self):
        return reverse('article:article_detail',args=[self.id])

    def was_created_recently(self):
        diff = timezone.now() - self.create

        # if diff.days <= 0 and diff.seconds < 60:
        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            return True
        else:
            return False


    class Meta:
        # 改表名
        db_table = 'ArticleInfo'
        verbose_name = '文章信息'
        # ordering 指定模型返回的数据排列顺序
        # '-create' 表明数据倒叙排列
        ordering = ('-create',)

    def __str__(self) -> str:
        return self.title
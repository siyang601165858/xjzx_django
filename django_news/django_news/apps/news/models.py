from django.db import models

# Create your models here.
from django_news.utils.models import BaseModel
from users.models import User


class Category(BaseModel):
    """新闻分类"""

    name = models.CharField(max_length=64, verbose_name='新闻分类')

    class Meta:
        db_table = 'tb_category'
        verbose_name = '新闻分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class News(BaseModel):
    """新闻"""

    title = models.CharField(max_length=256, verbose_name='新闻标题')  # 新闻标题
    source = models.CharField(max_length=64, verbose_name='新闻来源')  # 新闻来源
    digest = models.CharField(max_length=512, verbose_name='新闻摘要')  # 新闻摘要
    content = models.TextField(verbose_name='新闻内容')  # 新闻内容
    clicks = models.IntegerField(default=0, verbose_name='浏览量')  # 浏览量
    index_image_url = models.CharField(max_length=256, verbose_name='图片路径')  # 新闻列表图片路径
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='新闻分类')
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='新闻作者')

    status = models.IntegerField(default=0, verbose_name='当前审核状态')  # 当前新闻状态 如果为0代表审核通过，1代表审核中，-1代表审核不通过
    reason = models.CharField(max_length=256, verbose_name='审核不通过理由')  # 未通过原因，status = -1 的时候使用

    class Meta:
        db_table = 'tb_news'
        verbose_name = '新闻'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Comment(BaseModel):
    """评论"""
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='评论者')
    news = models.ForeignKey(News, on_delete=models.CASCADE, verbose_name='评论新闻')
    content = models.TextField(verbose_name='评论内容')

    parent = models.ForeignKey('self', on_delete=models.PROTECT, related_name='parent_comment', verbose_name='父评论')

    like_count = models.IntegerField(default=0, verbose_name='点赞条数')  # 点赞条数

    class Meta:
        db_table = 'tb_comment'
        verbose_name = '评论'
        verbose_name_plural = verbose_name


class CommentLike(BaseModel):
    """评论点赞"""
    # 多对多,第三张表

    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='被赞的评论')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='点赞的人')

    class Meta:
        db_table = 'tb_comment_like'
        verbose_name = '用户与点赞评论的关联表'
        verbose_name_plural = verbose_name

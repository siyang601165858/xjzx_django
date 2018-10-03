from django.contrib.auth.models import AbstractUser
from django.db import models


# from news.models import News


# Create your models here.


class User(AbstractUser):
    """用户"""

    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    avatar_url = models.CharField(max_length=256, verbose_name='头像路径')  # 用户头像路径
    signature = models.CharField(max_length=512, verbose_name='签名')  # 用户签名
    gender = models.IntegerField(default=1, verbose_name='性别')

    # 当前用户收藏的所有新闻:
    collection_news = models.ForeignKey("news.News", on_delete=models.PROTECT, verbose_name='该用户收藏的新闻', null=True,
                                        blank=True)  # 用户收藏的新闻
    # 用户所有的粉丝:那些人关注过我,related_name表示反向查找
    followers = models.ForeignKey('self', on_delete=models.PROTECT, related_name='followed', verbose_name='该用户的粉丝',
                                  null=True, blank=True)

    # 用户的偶像:我关注过哪些人
    # followed = models.ForeignKey('self', on_delete=models.PROTECT, related_name='followers', verbose_name='该用户的偶像')

    # 当前用户所发布的新闻:在新闻那边关联外键,这边是1,那边是多(一个人可以有很多新闻,一个新闻只能有一个作者)
    # news_list = models.ForeignKey("News", on_delete=models.PROTECT, verbose_name='该用户发表的新闻')

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

# class Followers(models.Model):
#     '''
#     用户的粉丝表
#     '''
#     followers = models.ForeignKey(User)

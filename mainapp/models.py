from django.db import models

# Create your models here.
from tinymce.models import HTMLField


class User(models.Model):
    name = models.CharField(max_length=50,unique=True,verbose_name='用户名')
    passwd = models.CharField(max_length=200,verbose_name='密码')
    phone = models.CharField(max_length=12,verbose_name='电话')
    image = models.ImageField(max_length=200,upload_to='user/images',verbose_name='用户头像')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

class Blob(models.Model):
    blob_type = (
        (0, '美食'),
        (1, '科技'),
        (2, '教育'),
        (3, '娱乐'),
        (4, '财经'),
        (5, '影视'),
        (6, '体育'),
    )

    title = models.CharField(max_length=50,verbose_name='标题')
    btype = models.IntegerField(choices=blob_type,verbose_name='类型')
    summary = models.TextField(default='',verbose_name='概要')
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)  #所属用户
    content = HTMLField(default='',verbose_name='文章内容')
    cnt = models.IntegerField(default=0,verbose_name='点击量')
    publish_time = models.DateTimeField(auto_now=True,verbose_name='发布时间')

    @property
    def type_name(self):
        return self.blob_type[self.btype][1]

#用户评论
class Replay(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,verbose_name='用户')
    blob = models.ForeignKey(Blob,on_delete=models.CASCADE,verbose_name='博客')
    content = HTMLField(default='',verbose_name='评论')
    reply_time = models.DateTimeField(auto_now=True,verbose_name='评论时间')
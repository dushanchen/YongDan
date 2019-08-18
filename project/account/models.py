from django.db import models


STATUS = [
        (0,'正常'),
        (1,'暂停'),
    ]

visible = [
        (0,'可见'),
        (1,'不可见')
    ]

MONITOR_TYPE = [(0,'1:1'),(1,'1:N'),(2,'布控')]


class Authority(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '权限字典表'

    name = models.CharField(max_length=100, verbose_name='权限名称')
    parent = models.ForeignKey('Authority', null=True, blank=True, verbose_name='父权限', on_delete=models.CASCADE)
    url = models.CharField(max_length=100, default='', blank=True, verbose_name='请求url')
    method = models.IntegerField(choices=[(0,'POST'), (1,'GET')], default=0, verbose_name='请求方式')
    detail = models.CharField(max_length=200, default='', blank=True, verbose_name='描述')

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.detail


class Role(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '角色'

    name = models.CharField(max_length=50, verbose_name='角色名称')
    authority = models.ManyToManyField('Authority', blank=True, verbose_name='权限')
    detail = models.CharField(max_length=200, default='', blank=True, verbose_name='描述')

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


class User(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '用户'
        indexes = [
            models.Index(
                fields=['name'],
                name='name_idx',
            ),
        ]
        
    name = models.CharField(max_length=50, unique=True, verbose_name='会员号', default='')
    phone = models.CharField(max_length=11, null=True, verbose_name='手机号')
    password = models.CharField(max_length=16, verbose_name='密码')
    status = models.IntegerField(choices=STATUS, blank=True, null=True, default=0, verbose_name='状态')
    
    role = models.ManyToManyField(Role, blank=True, verbose_name='角色')

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

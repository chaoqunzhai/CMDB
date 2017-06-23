from django.db import models

# Create your models here.

class Userprofile(models.Model):
    name = models.CharField(max_length=8,unique=True)
    email = models.EmailField(max_length=16,null=True,blank=True)
    status_type = (
        (0,'值班'),
        (1,'休息'),
        (2,'协同')
    )
    onwatch = models.SmallIntegerField(choices=status_type,default=2)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = '运维人员'


class Hostname(models.Model):
    ip = models.GenericIPAddressField(max_length=15,unique=True)
    disk = models.CharField(max_length=8,null=True,blank=True)
    cpu = models.CharField(max_length=8,null=True,blank=True)
    kernel = models.CharField(max_length=24,null=True,blank=True)
    species_type = models.ForeignKey('Species',verbose_name='业务线经理',null=True,blank=True)
    role_type = models.ManyToManyField('Userprofile',blank=True,null=True,default=1)
    source_choirce = (
        (0,'B28'),
        (1,'B2C'),
        (2,'大数据'),
        (3,'开发测试'),
        (4,'运维开发'),
    )
    source = models.SmallIntegerField(choices=source_choirce)
    def __str__(self):
        return self.ip
    class Meta:
        verbose_name_plural = '主机'

class Species(models.Model):
    species_name = models.CharField(max_length=16,unique=True)
    date = models.DateField(auto_now_add=True)
    phone = models.PositiveIntegerField(blank=True,null=True)


    def __str__(self):
        return self.species_name
    class Meta:
        verbose_name_plural = '业务线'




class Saltrun(models.Model):
    ip = models.ForeignKey('Hostname')
    fun = models.CharField(max_length=16,verbose_name='SALT模块')
    fun_args = models.CharField(max_length=32,verbose_name='执行命令')
    salt_callable =  models.TextField(null=True,blank=True)
    job = models.CharField(max_length=64)
    date = models.DateTimeField(auto_now_add=True)
    status_choirce = (
        (0,'成功'),
        (1,'失败'),
        (2,'定时任务'),
        (3,'进行中'),
        ('NUll','第一次配置'),
    )
    statues = models.PositiveSmallIntegerField(choices=status_choirce,default=2)
    histroy = models.CharField(max_length=16,null=True,blank=True)
    def __unicode__(self):

        return '%s' %self.fun_args

    class Meta:
        verbose_name_plural = '操作命令'
        unique_together = (("ip", "job"),)

class Server(models.Model):
    salt_leader = models.ManyToManyField('Saltrun')
    server_name = models.CharField(max_length=16,verbose_name='服务名称')
    port = models.CharField(max_length=8)
    files = models.CharField(max_length=32)
    url = models.URLField(null=True,blank=True)

    def __str__(self):
        return self.server_name
    class Meta:
        verbose_name_plural = '服务'
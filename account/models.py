from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from .fields import OrderField
from django.db.models.signals import post_save


# Create your models here.
class UserPost(models.Model):

    name = models.CharField('职位',max_length=150)
    active= models.BooleanField(default=True,verbose_name='是否启用')
    order = OrderField(blank=True,verbose_name='排序')

    class Meta:
        ordering = ['order']
        verbose_name = '岗位'
        verbose_name_plural = '岗位管理'

    def __str__(self):
        return self.name

class Department(models.Model):

    name = models.CharField('部门名称',max_length=200)
    active = models.BooleanField(default=True,verbose_name='是否启用')
    order = OrderField(blank=True,verbose_name='排序')

    class Meta:
        ordering = ['order']
        verbose_name = '部门'
        verbose_name_plural = '部门管理'

    def __str__(self):
        return self.name

class Profile(models.Model):

    GENDER_CHOICES=(
        ('M','男'),('F','女'),
    )
    JOB_CHOICES=(
        ('ON','在职'),('OUT','离职'),
    )
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    gender = models.CharField('性别',max_length=10,choices=GENDER_CHOICES)
    phone = models.PositiveIntegerField('联系方式',blank=True)
    date_of_birth = models.DateField('出生日期',blank=True,null=True)
    post = models.ForeignKey(UserPost,related_name='post_Profile',on_delete=models.CASCADE,verbose_name='岗位')
    department = models.ForeignKey(Department,related_name='Profiles',on_delete=models.CASCADE,verbose_name='部门')
    status = models.CharField('人员状态',max_length=10,choices=JOB_CHOICES,help_text="员工是否在职")

    def __str__(self):
        return "{}详细信息".format(self.user.username)

def create_user_profile(sender,instance,created,**kwargs):
    if created:
        profile,created = Profile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile,sender=User)

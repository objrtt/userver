from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Audit(models.Model):
    username = models.IntegerField(max_length=11, verbose_name='手机号')
    real_name = models.CharField(max_length=12, verbose_name='真实姓名')
    id_card = models.CharField(max_length=18, verbose_name='身份证号码')
    id_card_posi = models.CharField(max_length=16, verbose_name='身份证正面云链接')
    id_card_nega = models.CharField(max_length=16, verbose_name='身份证反面云链接')
    hand_card_posi = models.CharField(max_length=16, verbose_name='手持身份证云链接')
    audit_pass = models.IntegerField(default=False, verbose_name='通过与否')

    class Meta:
        db_table = 'audittable'  # 指明数据库表名
        verbose_name = '未审核用户'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name

    def __str__(self):
        """定义每个数据对象的显示信息"""
        return self.username

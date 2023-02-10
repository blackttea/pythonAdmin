from django.db import models


# Create your models here.
class Menu(models.Model):
    id = models.BigAutoField(primary_key=True)
    parent_id = models.CharField(max_length=30, verbose_name='父级菜单')
    name = models.CharField(max_length=30, verbose_name='路径名')
    url = models.CharField(max_length=30, verbose_name='路径名')
    component = models.CharField(max_length=30, verbose_name='组件路径')
    redirect = models.CharField(max_length=30, verbose_name='定向')
    meta = models.CharField(max_length=30, verbose_name='配置')
    role = models.CharField(max_length=30, verbose_name='角色')

    class Meta:
        db_table = 'sys_menu'  # 指明数据库表名
        verbose_name = '菜单'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称

    def __str__(self):
        """定义每个数据对象的显示信息"""
        return self.name

from django.db import models


# Create your models here.
class BookInfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=20, verbose_name='名称')
    create_date = models.DateField(verbose_name='发布日期')
    read_num = models.IntegerField(default=0, verbose_name='阅读量')
    discuss_num = models.IntegerField(default=0, verbose_name='评论量')

    class Meta:
        db_table = 'bk_tool'  # 指明数据库表名
        verbose_name = '文章'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称

    def __str__(self):
        """定义每个数据对象的显示信息"""
        return self.btitle

from django.conf import settings
from django.db import models
import jwt
import datetime


# Create your models here.
class Book(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True)
    cover = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=2, max_digits=50)
    is_delete = models.IntegerField()

    class Meta:
        db_table = 'book'


class Role(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True)
    menu = models.CharField(max_length=5000)
    page = models.JSONField()
    level = models.CharField(max_length=255)

    class Meta:
        db_table = 'sys_role'
        ordering = ['id']


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=255, null=True)
    page = models.JSONField(null=True)
    img = models.ImageField()
    menu = models.CharField(max_length=255, null=True)
    level = models.IntegerField(verbose_name='权限级别')

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        token = jwt.encode({
            'exp': datetime.datetime.now() + datetime.timedelta(days=1),
            'iat': datetime.datetime.now(),
            'data': {
                'username': self.username
            }
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.encode("utf-8").decode('utf-8')

    class Meta:
        db_table = 'sys_user'
        verbose_name = 'user'
        verbose_name_plural = verbose_name


class Code(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    code = models.CharField(max_length=255, null=True)
    updateTime = models.DateField()

    class Meta:
        db_table = 'code'

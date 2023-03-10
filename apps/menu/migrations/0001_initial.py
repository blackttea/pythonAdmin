# Generated by Django 4.1 on 2022-09-02 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('parent_id', models.CharField(max_length=30, verbose_name='父级菜单')),
                ('title', models.CharField(max_length=30, verbose_name='路径名')),
                ('path', models.CharField(max_length=30, verbose_name='路径名')),
                ('component', models.CharField(max_length=30, verbose_name='组件路径')),
                ('redirect', models.CharField(max_length=30, verbose_name='定向')),
                ('meta', models.CharField(max_length=30, verbose_name='配置')),
                ('role', models.CharField(max_length=30, verbose_name='角色')),
            ],
            options={
                'verbose_name': '菜单',
                'verbose_name_plural': '菜单',
                'db_table': 'sys_menu',
            },
        ),
    ]

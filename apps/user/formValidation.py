from django import forms
from django.core.validators import ValidationError, RegexValidator


# 自定义名称敏感校验器
class NameValidation:
    def __call__(self, value):
        """
            自定义验证
            :param value: value表示要验证的数据
            :return: 如果ValidationError表示验证失败 正常结束表验证通过
        """
        nameList = ["笑嘻嘻", "妈蛋", "滚犊子"]
        for name in nameList:
            if value.find(name) != -1:
                raise ValidationError("名称不能含有敏感词汇")


# Book 表单验证器
class BookFrom(forms.Form):
    """验证Book表单"""
    name = forms.CharField(
        required=True,
        max_length=10,
        min_length=2,
        validators=[
            # 自定义验证器
            NameValidation()
        ],
        error_messages={
            "required": "名称必填",
            "max_length": "名称不能超过十位",
            "min_length": "名称至少是两位"
        })
    author = forms.CharField(
        required=True,
        error_messages={
            "required": "作者必填"
        })



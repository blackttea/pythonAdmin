import os
from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import render
from PIL import Image, ImageDraw, ImageFont

from user.check import request_verify
from utils.common import response_success


def wordToImg(request):
    img = request.FILES.get('file')

    CHILD_W = CHILD_H = 16
    txt = request.POST.get('text')
    font = ImageFont.truetype("D:/pythonProject/djangoProject/apps/tool/CJK.ttf", CHILD_W)  # 字体及大小
    imgSrc = Image.open(BytesIO(img.read()))  # 打开原图像
    w, h = imgSrc.size  # 原图像宽高

    imageChild = Image.new("RGB", (CHILD_W, CHILD_H))  # 新建子图
    imageDst = Image.new("RGB", (CHILD_W * w, CHILD_H * h))  # 新建子图
    a, b, textW, textH = font.getbbox("迷")  # 取单个文字的宽高信息
    offsetX = (CHILD_W - textW) >> 1  # 居中
    offsetY = (CHILD_H - textH) >> 1

    charIndex = 0  # 记录文字下标
    draw = ImageDraw.Draw(imageChild)  # 取最小绘图对象，用于绘制文字
    for y in range(h):
        for x in range(w):
            color = imgSrc.getpixel((x, y))
            draw.rectangle((0, 0, CHILD_W, CHILD_H), fill=color)
            draw.text((offsetX, offsetY), txt[charIndex], font=font, fill="white")
            imageDst.paste(imageChild, (x * CHILD_W, y * CHILD_H))
            charIndex = (charIndex + 1) % len(txt)
    out = BytesIO()
    # 图片保存管道中,png格式
    imageDst.save(out, 'png')
    # 读取得时候指针回零0
    out.seek(0)
    # 把图片返回到浏览器上，通过response对象返回浏览器上
    response = HttpResponse(content_type='image/png')
    # 从管道把图片读取出来
    response.write(out.read())
    response['Content-length'] = out.tell()
    print(response['Content-length'])
    return response

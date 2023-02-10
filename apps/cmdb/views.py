from django.shortcuts import HttpResponse

from apps.cmdb.models import BookInfo


# Create your views here.
def index(request):
    print(BookInfo.objects.all())
    return HttpResponse('hello world')

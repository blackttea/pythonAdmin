from django.utils.deprecation import MiddlewareMixin


class MyMdd1(MiddlewareMixin):
    def process_request(self, request):
        print(request)
        print('自定义中间件 process_request 方法一')
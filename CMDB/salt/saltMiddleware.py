from django.shortcuts import HttpResponse,redirect


#钩子middleware方法！
#在setting中添加配置，相当于全局都需要过这个middeware插件
#setting中的MIDDLEWARE 是从上到下顺序执行，如果上面中有一个MIDDLEWARE没有通过,那后面也都不会执行
class SimpleMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response



    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == int('404'):
            #print("middleware",type(response.status_code))
            return redirect('/error')
        return response

    #进入视图之前会先进入这里
    #捕用户访问view的时候，就会先经过这里，然后才去调用view视图函数，所以这里可以拿到很多信息
    def process_view(self,request,view_func,view_args,view_kwargs):
        #在视图调用之前调用的这个 process_view
        ##所以可以拿到很多对端的各种信息，例如IP，请求头的所以东西等等

        print("process_view____视图调用之前会先执行这个process_view:",self,request,view_func,view_args,view_kwargs)
        # if request.META.get("REMOTE_ADDR") == "127.0.0.1":
        #     return HttpResponse("拒绝本地访问")



    #如果view里面出现了错误，就会定位到这里，可以做自定制的错误页面
    def process_exception(self,request,exception):

        print("proces exception",request,exception)

        return HttpResponse("<h1>您访问的页面%s不存在！错误信息:%s,%s</h1>" %(exception,request,exception))
    # def process_template_respone(self,request,response):
    #     print("process_template",request,response)
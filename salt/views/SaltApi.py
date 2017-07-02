
from django.views.generic import View
from django.shortcuts import render,HttpResponse
from salt import models
class SaltLogin(View):
    def get(self,request):

        return render(request, "salt/salt_login.html")

class SaltApi(View):
    def get(self,request,*args,**kwargs):
        return  render(request, 'salt/salt_api.html')

    def post(self,request,*args,**kwargs):
        Tag=0
        salt_api_id=request.POST.getlist('salt_api_id')
        salt_api_name = request.POST.getlist('salt_api_name')
        salt_api_tage = request.POST.getlist('salt_api_tage')
        if salt_api_id and salt_api_name and salt_api_tage:
            Tag=1
        print('salt_api',salt_api_id,salt_api_name,salt_api_tage)
        return render(request, 'salt/salt_api.html', {'Tag':Tag})

class SaltMap(View):

    def get(self,request):
        hosts = models.Hostname.objects.all()
        print(hosts)
        test = '业务类型'
        return render(request, "salt/salt_map.html", {'test':test})
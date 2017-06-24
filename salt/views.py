from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required
from salt import models

from django.views.generic import View
from salt.plugins.source import SourceBase
from salt.plugins.Asset import Asset
from salt.forms import Hostname
from salt.plugins.getcookis import get_cookies
import json
obj=SourceBase.instance()




class Hsotlist(View):
    def get(self, request, *args, **kwargs):

        objdata = Asset(request.GET.get('page',1))
        hostname_form=Hostname()
        _ ,contacts =objdata.response
        val = get_cookies(request)
        pgae_obj = Asset(pgae_number=val)
        print('val',pgae_obj.page_number)
        return render(request, "hostlist.html",{'source_type_dict':obj.sorce_type,'articles':contacts,'hostname_form':hostname_form})
    def post(self,request,*args, **kwargs):
        error_msg=''
        print('test',request.POST.get('ip'),request.POST.get('source'))
        hostname_form = Hostname(request.POST)
        if request.POST.get('ip'):


            hostname_dict = {'ip':request.POST.get('ip'),'kernel':request.POST.get('kernel'),'source':request.POST.get('source_name')}
            if hostname_form.is_valid():

                hostname_ip = models.Hostname.objects.filter(ip=request.POST.get('ip'))
                if hostname_ip:
                    error_msg = '主机已经存在'
                else:
                    models.Hostname.objects.create(**hostname_dict)
                return render(request, 'hostlist.html', {'error_msg': error_msg, 'source_type_dict': obj.sorce_type,'hostname_form':hostname_form})
            else:
                print('error',hostname_form.errors)
        else:
            error_msg='NOT index IP'
            return render(request,'hostlist.html',{'error_msg':error_msg,'source_type_dict':obj.sorce_type,'hostname_form':hostname_form})
        return render(request, "hostlist.html",{'source_type_dict':obj.sorce_type,'hostname_form':hostname_form})
    def delete(self,request,*args,**kwargs):
        uid = request.body
        print('uid',uid.decode())
        uid = uid.decode()
        hostname = models.Hostname.objects.filter(id=uid).delete()
        return HttpResponse(uid)

class APItDetailView(View):
    def get(self,request,nid):
        print('APItDetailView',nid)
        return render(request,'salt/asset_detail.html',{'nid':nid})

class SaltApiJSON(View):

    def get(self,request):
        val = get_cookies(request)
        objconfig = Asset(request.GET.get('page'),val)
        hostlist,_=objconfig.response
        return HttpResponse(json.dumps(hostlist))

class SaltMap(View):

    def get(self,request):
        hosts = models.Hostname.objects.all()
        print(hosts)
        test = '业务类型'
        return render(request, "salt/salt_map.html",{'test':test})



class SaltLogin(View):
    def get(self,request):

        return render(request, "salt/salt_login.html")

class SaltApi(View):
    def get(self,request,*args,**kwargs):
        return  render(request,'salt/salt_api.html')

    def post(self,request,*args,**kwargs):
        Tag=0
        salt_api_id=request.POST.getlist('salt_api_id')
        salt_api_name = request.POST.getlist('salt_api_name')
        salt_api_tage = request.POST.getlist('salt_api_tage')
        if salt_api_id and salt_api_name and salt_api_tage:
            Tag=1
        print('salt_api',salt_api_id,salt_api_name,salt_api_tage)
        return render(request, 'salt/salt_api.html',{'Tag':Tag})

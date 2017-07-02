from django.shortcuts import render,HttpResponse

from salt import models

from django.views.generic import View
from salt.plugins.source import SourceBase
from salt.plugins.Asset import Asset
from salt.forms import Hostname
from salt.plugins.getcookis import get_cookies
import json
obj=SourceBase.instance()



class SaltApiJSON(View):
    """
    :sal_api_json 是数据源
    """
    def get(self,request):
        val = get_cookies(request)
        # objconfig = Asset(request.GET.get('page'),val)
        objconfig= Asset(request,val)
        hostlist,contacts=objconfig.response
        print('[View.SaltApiJSON.get]   中,每页分%s,Page函数中的值%s,筛选器是%s' % (val, objconfig.page_number, contacts))
        return HttpResponse(json.dumps(hostlist))

class Hsotlist(View):

    def get(self, request, *args, **kwargs):

        val = get_cookies(request)
        objdata = Asset(request,val)
        hostname_form=Hostname()

        _, contacts = objdata.response

        print('[View.Hsotlist.get]   中,每页分%s,Page函数中的值%s,筛选器是%s'%(val,objdata.page_number,contacts))


        return render(request, "hostlist.html", {'source_type_dict':obj.sorce_type, 'articles':contacts, 'hostname_form':hostname_form})
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
                return render(request, 'hostlist.html', {'error_msg': error_msg, 'source_type_dict': obj.sorce_type, 'hostname_form':hostname_form})
            else:
                print('error',hostname_form.errors)
        else:
            error_msg='NOT index IP'
            return render(request, 'hostlist.html', {'error_msg':error_msg, 'source_type_dict':obj.sorce_type, 'hostname_form':hostname_form})
        return render(request, "hostlist.html", {'source_type_dict':obj.sorce_type, 'hostname_form':hostname_form})
    def delete(self,request,*args,**kwargs):
        uid = request.body
        print('uid',uid.decode())
        uid = uid.decode()
        hostname = models.Hostname.objects.filter(id=uid).delete()
        return HttpResponse(uid)

class APItDetailView(View):
    def get(self,request,nid):
        print('APItDetailView',nid)
        return render(request, 'salt/asset_detail.html', {'nid':nid})









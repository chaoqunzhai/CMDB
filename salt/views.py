from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required
from salt import models
import json
from django.views.generic import View
from salt.plugins.source import SourceBase
from salt.plugins.pagelist import page
obj=SourceBase.instance()



class Hsotlist(View):
    def get(self, request, *args, **kwargs):
        print('Hsotlist测试',request.GET.get('p',1))

        return render(request, "hostlist.html",{'source_type_dict':obj.sorce_type})
    def post(self,request,*args, **kwargs):
        print('test',request.POST.get('ip'),request.POST.get('source'))

        if request.POST.get('ip'):
            hostname_ip = models.Hostname.objects.filter(ip=request.POST.get('ip'))
            if hostname_ip:
                error_msg='主机已经存在'
                return render(request, 'hostlist.html',{'error_msg': error_msg, 'source_type_dict': obj.sorce_type})
            models.Hostname.objects.create(ip=request.POST.get('ip'),kernel=request.POST.get('kernel'),source=request.POST.get('source_name'))
        else:
            error_msg='NOT index IP'
            return render(request,'hostlist.html',{'error_msg':error_msg,'source_type_dict':obj.sorce_type})
        return render(request, "hostlist.html",{'source_type_dict':obj.sorce_type})
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
        #返回列名
        #返回数据
        #数据库中的数据
        '''
        一个@表示从数据库返回数据取
        2个@@表示从全局数据取
        '''

        response = {'status': True, 'data': None, 'message': ''}
        try:
                table_config = [
                {
                    'q': None,
                    'title': '选择',
                    'display': True,
                    'type': {'tpl': "<input type='checkbox' />", 'kwargs': {'db': 'id'}},
                    'attr': {}
                },
                {
                    'q': 'id',
                    'title': '主机ID',
                    'display': True,
                    'type': {'tpl': '{db}', 'kwargs': {'db': '@id'}},
                    'attr': {}
                },
                {
                    'q': 'disk',
                    'title': '磁盘',
                    'display': True,
                    'type': {'tpl': '{db}', 'kwargs': {'db': '@disk'}},
                    'attr': {}
                },
                {
                    'q': 'ip',
                    'title': 'IP地址',
                    'display': True,
                    'type': {'tpl': '{db}', 'kwargs': {'db': '@ip'}},
                    'attr': {}
                },
                {
                    'q': 'kernel',
                    'title': '主机系统',
                    'display': True,
                    'type': {'tpl': '{db}', 'kwargs': {'db': '@kernel'}},
                    'attr': {}
                },
                {
                    'q': 'role_type__name',
                    'title': '运维人员',
                    'display': True,
                    'type': {'tpl': '{db}', 'kwargs': {'db': '@role_type__name'}},
                },
                {
                    'q': 'source',
                    'title': '业务类型',
                    'display': True,
                    'type': {'tpl': '{db}', 'kwargs': {'db': '@@Source_choirce'}},
                    'attr': {'name': 'source', 'id': '@source', 'origin': '@source',
                             'edit-enable': 'true',
                             'edit-type': 'select',
                             'global-name': 'source'}
                },
                {
                    'q': 'saltrun__statues',
                    'title': '状态',
                    'display': True,
                    'type': {'tpl': '{db}', 'kwargs': {'db': '@@Salt_run_status'}},
                    'attr': {'name': 'source', 'id': '@source', 'origin': '@source',
                             'edit-enable': 'true',
                             'edit-type': 'select',
                             'global-name': 'source'}
                },
                {
                    'q': None,
                    'title': '操作',
                    'display': True,
                    'type': {'tpl': "<a href='/salt/salt_api_{db}'>查看详情</a> | <a href='/salt/salt_api_{db}'>编辑</a>  ", 'kwargs': {'db': '@id'}},
                },

            ]
                # print(models.Hostname.objects.filter(**{}).values('role_type__salt_run__statues'))
                # print(models.Saltrun.status_choirce)
                query_list = []
                for item in table_config:
                    if not item['q']:
                        continue
                    # elif item['q'] == 'role_type__salt_run__statues':
                    #     table_data_salt_run = models.Hostname.objects.filter(**{}).values('role_type__salt_run__statues')
                    query_list.append(item['q'])
                # 拿到字典
                # 查数据返回的是queryset，json只能去转换python的数据类型  所以外部加个list对queryset进行转换,拿内部就包裹一个字典
                data = (
                    models.Hostname.objects.filter(**{}).values(*query_list).order_by('-id'))
                table_data= []
                #去重操作
                for data_item in data:
                    if data_item in table_data:
                        continue
                    else:
                        table_data.append(data_item)
                # 就拿到了元组
                # table_data = models.Hostname.objects.filter(**{}).values_list('ip', 'role_type')
                #gloab_config 是从内存中得到数据
                #table_config 是上面配置的
                #table_data 是从数据库中取到数据
                #下面是第一种方法
                response = {
                    'table_config': table_config,
                    'table_data': table_data,
                    'gloab_config': {
                        "Source_choirce": models.Hostname.source_choirce,
                        "Salt_run_status":models.Saltrun.status_choirce
                    }
                }
                test=page(table_data)
                print('test111',test)
        except Exception as e:
                response['status'] = False
                response['message'] = str(e)
        return HttpResponse(json.dumps(response))


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

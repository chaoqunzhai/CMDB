from salt import models
from salt.plugins.base import BaseServiceList
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from salt.plugins.getcookis import get_cookies
import json


class Asset(BaseServiceList):
    def __init__(self,request,cookies_number,pgae_number=10):
        #返回列名
        #返回数据
        #数据库中的数据
        '''
        一个@表示从数据库返回数据取
        2个@@表示从全局数据取
        '''
        self.request  = request
        self.page_number = pgae_number
        self.cookies_number = cookies_number
        condition_config={}
        response = {'status': True, 'data': None, 'message': ''}
        try:
            self.table_config = [
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
                    'type': {'tpl': "<a href='/salt/salt_api_{db}'>查看详情</a> | <a href='/salt/salt_api_{db}'>编辑</a>  ",
                             'kwargs': {'db': '@id'}},
                },

            ]
            # print(models.Hostname.objects.filter(**{}).values('role_type__salt_run__statues'))
            # print(models.Saltrun.status_choirce)
            query_list = []
            for item in self.table_config:
                if not item['q']:
                    continue
                query_list.append(item['q'])
            # 拿到字典
            # 查数据返回的是queryset，json只能去转换python的数据类型  所以外部加个list对queryset进行转换,拿内部就包裹一个字典
            data = (
                models.Hostname.objects.filter(**{}).values(*query_list).order_by('-id'))
            self.table_data = []
            # 去重操作
            for data_item in data:
                if data_item in self.table_data:
                    continue
                else:
                    self.table_data.append(data_item)
            # 就拿到了元组
            # table_data = models.Hostname.objects.filter(**{}).values_list('ip', 'role_type')
            # gloab_config 是从内存中得到数据
            # table_config 是上面配置的
            # table_data 是从数据库中取到数据
            # 下面是第一种方法



        except Exception as e:
            response['status'] = False
            response['message'] = str(e)

        super(Asset,self).__init__(condition_config=condition_config,table_config=self.table_config)

    @property
    def response(self):
        page = self.request.GET.get('page')
        paginator = Paginator(self.table_data, self.cookies_number)  # 分页功能  5的意思是一页分5条
        if page:
           pass
        else:
            page = 1
            print('Asset.py         [如果cookies中没值,就默认第一页]')
            # page = self.request.GET.get('page')  # 前端发送一个page  去url里面取page的值
        #
        print('Aset.py[前端筛选到每页%s数据,分%s页]'%(self.cookies_number,page))
        try:
            self.contacts = paginator.page(page)  # 如果不是整理
        except PageNotAnInteger:

            self.contacts = paginator.page(1)
        except EmptyPage:  # 如果是空页
            self.contacts = paginator.page(paginator.num_pages)

        # print('contacts',self.contacts,paginator.page(page).object_list)
        try:
            self.response_base = {
                'table_config': self.table_config,
                'table_data': paginator.page(page).object_list,
                'gloab_config': {
                    "Source_choirce": models.Hostname.source_choirce,
                    "Salt_run_status": models.Saltrun.status_choirce
                }
            }
            print('Asset.py       [总共%s,每页显示%s,当前页是%s,筛选器是%s]'%(paginator.count, self.page_number,page,self.contacts))
        except Exception as e:
            self.response_base = {
                'table_config': self.table_config,
                'table_data': paginator.page(1).object_list,
                'gloab_config': {
                    "Source_choirce": models.Hostname.source_choirce,
                    "Salt_run_status": models.Saltrun.status_choirce
                }
            }


        return self.response_base,self.contacts,

    # @property
    # def contactall(self):
    #
    #     return self.contacts
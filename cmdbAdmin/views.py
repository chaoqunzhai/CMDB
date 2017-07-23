from django.shortcuts import render
from cmdbAdmin import app_config
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from cmdbAdmin.admin_base import site
from cmdbAdmin.plugins.getcookis import get_cookies


def app_index(request):

    return render(request, 'cmdbAdmin/app_index.html', {'site': site})


def get_filter_objs(request,admin_class):
    """
    更具前端提交的表单数据来过滤，，，返回filter的结果
    :param request:
    :param admin_class:
    :return:
    """
    filter_condtions = {}
    for k,v in request.GET.items():
        print('kv',k,v)
        if k == '_page':continue
        if v and v != '---------':
            filter_condtions[k]=v
    querset = admin_class.model.objects.filter(**filter_condtions)
    print('前端提交过滤',filter_condtions)
    return querset,filter_condtions

def model_table_list(request, app_name, model_name):
    '''
    1，拿到表对象，取表的里的数据
    2.拿到此表对应的amdin class

            #前端根据model_class  获取表里的数据
            #前端根据admin_class  决定要显示什么地段   (这个参数在amdin_base中基类中定义,和在cmdb_admin中定义字段)
            #locals  python的内建函数 locals()可以直接将函数中所有的变量全部传给模板
    :param request:
    :param app_name:
    :param model_name:
    :return:
    '''
    # 判断这个APP是否已经注册
    print('app_name----',app_name,model_name)
    pgae_number = get_cookies(request)
    if app_name in site.registered_admins:
        if model_name in site.registered_admins[app_name]:
            admin_class = site.registered_admins[app_name][model_name]
            queyset = admin_class.model.objects.all()
            '''filter_conditions 是前端选择过滤的字段,然后在传递给buid_filetr_ele 去做前端option selected '''
            queyset,filter_conditions = get_filter_objs(request,admin_class)
            print('存在--',queyset)
            paginator = Paginator(queyset, pgae_number)
            page = request.GET.get('_page')
            try:
                queyset = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                queyset = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                queyset = paginator.page(paginator.num_pages)

            print('总共',paginator.count)
            return render(request, "cmdbAdmin/model_table_list.html", locals())


print("注册的admin list:", site.registered_admins)

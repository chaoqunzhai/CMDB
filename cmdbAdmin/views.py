from django.shortcuts import render
from cmdbAdmin import app_config

from cmdbAdmin.admin_base import site



def app_index(request):

    return render(request, 'cmdbAdmin/app_index.html', {'site': site})


def model_table_list(request, app_name, model_name):
    '''
    1，拿到表对象，取表的里的数据
    2.拿到此表对应的amdin class

            #前端根据model_class  获取表里的数据
            #前端根据admin_class  绝对要显示什么地段   (这个参数在amdin_base中基类中定义,和在cmdb_admin中定义字段)
            #locals  python的内建函数 locals()可以直接将函数中所有的变量全部传给模板
    :param request:
    :param app_name:
    :param model_name:
    :return:
    '''
    # 判断这个APP是否已经注册
    print('app_name----',app_name,model_name)
    if app_name in site.registered_admins:
        if model_name in site.registered_admins[app_name]:
            model_class, admin_class = site.registered_admins[app_name][model_name]
            queyset = model_class.objects.all()
            print('存在--',model_class)
            return render(request, "cmdbAdmin/model_table_list.html", locals())


print("注册的admin list:", site.registered_admins)

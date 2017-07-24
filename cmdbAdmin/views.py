from django.shortcuts import render
from cmdbAdmin import app_config
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from cmdbAdmin.admin_base import site
from cmdbAdmin.plugins.getcookis import get_cookies
from django.db.models import Q

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
        '''这里跳过的意思,前端进行分页操作,然后name=参数 传递到这，是不需要去数据库中过滤的
        _q 是搜索字段,也是不用去这个过滤操作中的，所以跳过。具体search操作在其他函数中
        '''
        if k in ['_page','_q','_o']:continue


        if v and v != '---------':
            filter_condtions[k]=v
    print('前端提交过滤', filter_condtions)
    querset = admin_class.model.objects.filter(**filter_condtions).order_by('-id')

    return querset,filter_condtions

def get_search_objs(request,queyset,admin_class):
    """
    1.拿到_q的值
    2.拼接Q查询条件      q obj (OR: ('ip', '111'), ('fun', '111'))
    3.调用filter里面的(Q条件)
    4.返回结果
    :param request:
    :param queyset:
    :param admin_class:
    :return:
    """
    q_val = request.GET.get('_q')

    if q_val:
        q_obj = Q()
        q_obj.connector = "OR"
        for search_field in admin_class.search_fields:
            q_obj.children.append(("%s__contains" %search_field,q_val))
        print('q_obj',q_obj)
        search_results = queyset.filter(q_obj)
    else:
        search_results = queyset
    return search_results,q_val

def get_order_objs(request,queyset):
    """
    排序,
    1.获取_o的正负值,来确定下次排序是顺序
    2.调用oder_by(_o的值)
    3.处理整
    :param request:
    :param queyset:
    :return:
    """
    #orderby_key 是拿到前端的字段
    #orderby_column 对哪个字段进行了排序,只是用来给前端判断是对同一个字段排序
    #orderby_result 是排序后的数据
    #new_order_key
    #last_orderby_key 就是用来下一页的记住当前的_o=  参数
    orderby_key =request.GET.get('_o')
    #设置返回给前端为空,如果是none 会出错
    last_orderby_key = orderby_key or ''

    if orderby_key:
        orderby_column = orderby_key.strip('-')
        orderby_result = queyset.order_by(orderby_key)


        #正序，倒叙
        if orderby_key.startswith('-'):
            new_order_key = orderby_key.strip('-')
        else:
            new_order_key = "-%s" %orderby_key
        return orderby_result,new_order_key,orderby_column,last_orderby_key
    else:
        return queyset,None,None,last_orderby_key



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
            '''get_filter_objs数据过滤,把所有参数拼成一个字典,
            filter_conditions 是前端选择过滤的字段,然后在传递给buid_filetr_ele 去做前端option selected '''
            #过滤后的数据
            queyset,filter_conditions = get_filter_objs(request,admin_class)
            #对已经过滤后的数据,在进行search,q_val 是让前端可以显示
            queyset,q_val = get_search_objs(request,queyset,admin_class)
            #排序
            queyset, new_order_key, orderby_column,last_orderby_key = get_order_objs(request,queyset)

            print('存在--',queyset)
            paginator = Paginator(queyset, pgae_number)
            page = request.GET.get('_page')
            try:
                queyset = paginator.page(page)
            except PageNotAnInteger:

                queyset = paginator.page(1)
            except EmptyPage:

                queyset = paginator.page(paginator.num_pages)

            print('总共',paginator.count)
            return render(request, "cmdbAdmin/model_table_list.html", locals())


print("注册的admin list:", site.registered_admins)

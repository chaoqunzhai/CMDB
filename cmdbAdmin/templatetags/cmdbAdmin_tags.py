from django.template import Library
from django.utils.safestring import mark_safe


register = Library()


##前端传入变量 这个simple_tag用来把你的表verbose_name_plural 列出来
@register.simple_tag()
def get_model_verbose_name(admin_class):

    return admin_class.model._meta.verbose_name_plural

@register.simple_tag()
def get_app_name(model_class):
    return model_class._meta.model_name



@register.simple_tag()
def get_model_name(model_class):

    return model_class._meta.app_label


@register.simple_tag()
def build_table_row(row,admin_class):
    '''
    1.循坏list_dispaly,反射出每个字段的值
    2.判断是否是第一个字段,如果是，加<a>标签

    :param row:
    :param admin_class:
    :return:
    '''
    row_ele = "<tr>"
    for index,colomn_name in enumerate(admin_class.list_display):
        fileds_obj = row._meta.get_field(colomn_name)  #获取字段属性 这里只去判断是否是choices
        if fileds_obj.choices:
            colomn_display_func = getattr(row,"get_%s_display"%(colomn_name))

            colomn_val = colomn_display_func()
        else:
            colomn_val =getattr(row,colomn_name)
        if index == 0:
            td_ele = "<td><a href='#'>{colomn_val}</td>".format(colomn_val=colomn_val)
        else:
            td_ele = "<td name='11'>{colomn_val}</td>".format(colomn_val=colomn_val)
        row_ele +=td_ele

    row_ele += "</tr>"
    return row_ele


@register.simple_tag()
def  get_abs_value(page,curent_page_number):
    """返回当前页与循环页 差的绝对值,,目的是来限制 标签的数过多"""

    return abs(page - curent_page_number)
@register.simple_tag()
def get_filter_condtions_string(filter_conditions,q_val):

    """增加分页后，点击下一页，还是让前端显示选中的option的selected"""
    condtion_str = ""
    for k,v in filter_conditions.items():

        condtion_str +="&%s=%s" %(k,v)

    print("condtion_str",condtion_str)

    """拼接search字段,下一页的时候，还是带search的值"""
    if q_val:
        condtion_str += "&_q=%s" %q_val
    return condtion_str


@register.simple_tag()
def generate_orderby_icon(new_order_key):
    if new_order_key.startswith('-'):
        icon_ele = """<i class="fa fa-angle-up" aria-hidden="true"></i>"""
    else:
        icon_ele = """<i class="fa fa-caret-down" aria-hidden="true"></i>"""
    return mark_safe(icon_ele)

@register.simple_tag()
def buid_filetr_ele(filter_column,admin_class,filter_conditions):
    '''
    1.拿到要过滤字段的对象,filed_obj
    2.调用field_obj.get_choices()
    3.生成select元素
    4.循环choice列表,生成option元素
    5.
    :param filter_column: 是过滤的字段
    :param admin_class:  显示的字段
    :param filter_conditions   filter_optioon做的作用就是用来把选中的字段在返回给前端,这样能知道 是通过什么字段过滤的
    :return
    '''

    fields_obj = admin_class.model._meta.get_field(filter_column).get_choices()
    print('1111111111',filter_column)
    filter_option = filter_conditions.get(filter_column)
    #filter_optioon做的作用就是用来把选中的字段在返回给前端,这样能知道 是通过什么字段过滤的
    #会得到2种情况
    #1.None  代表没有对这个字段进行过滤
    #2.有值，，这个值就是前端选中的具体的option的val值

    select_ele = "<select class='form-control' name=%s>" %filter_column
    print('filter_option',filter_option)
    if filter_option:  #字段是否过滤.当用到多个过滤条件的时候
        for choices in fields_obj:
            if filter_option == str(choices[0]):
                selected = "selected"
            else:
                selected = ''
            option_ele = "<option value=%s %s>%s</option>" %(choices[0],selected,choices[1])
            select_ele += option_ele
    else:

        for choices in fields_obj:
            option_ele = "<option value=%s>%s</option>" % (choices[0],choices[1])
            # option_ele = "<option value=''>---------</option>"
            select_ele += option_ele
        print('---------', fields_obj)
    select_ele += "</select>"
    return mark_safe(select_ele)
    # # print('bulid——filter',admin_class.model._meta.get_field(filter_column))
    # print('getchioice',admin_class.model._meta.get_field(filter_column).choices)
from salt import models
from cmdbAdmin.admin_base import site,BaseAdmin


class CustomerAdmin(BaseAdmin):
    list_display = ['id','ip','disk','cpu','kernel','species_type','source']      #显示字段
    list_filter = ['species_type','source']   #过滤配置 这必须是外键 有关联的字段才可以,不然会报 'NoneType' object has no attribute 'model' 错误
    # list_per_page = 5
    search_fields = ['ip','kernel','species_type__species_name','role_type__name']


class Saltrun(BaseAdmin):
    list_display = ['ip', 'fun', 'fun_args', 'job','statues']
    list_filter = ['ip','statues']

    search_fields = ['ip__ip','fun','fun_args','job']


site.register(models.Saltrun,Saltrun)
site.register(models.Hostname,CustomerAdmin)
print('----Admin[salt]---')
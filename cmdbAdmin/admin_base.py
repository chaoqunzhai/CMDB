
#基类  以后功能直接在这上面加就行
class BaseAdmin(object):
    list_display = ()
    list_filter = ()

class Adminsite(object):
    def __init__(self):
        self.registered_admins = { }

    def register(self, model_or_iterable, admin_class=None, **options):
            """
            负责把每个App下的表注册self.registered_admins集合里
            model_or_iterable:里面是自定义的admin中的表传入过来的表名
            registerd_admins 里是自定义的数据

            registerd_admins ={
                app1:{
                '表':[admin_class,model_class]
                },
                app2:{
                '表':[admin_class,model_class]
                }
            }
             #model_or_iterable 表的一个对象
             #model_or_iterable._meta.model_name 获取这个表对象的名字
            :param self:
            :param model_or_iterable:
            :param admin_class:
            :param options:
            :return:
            """
            app_label = model_or_iterable._meta.app_label #通过表获取app的名字

            if app_label not in self.registered_admins:  #如果不在这个集合内就新建一个app的key
                self.registered_admins[app_label] = {}
            self.registered_admins[app_label][model_or_iterable._meta.model_name] = [model_or_iterable,admin_class]




site = Adminsite()

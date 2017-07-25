from django.forms import ModelForm


def __new__(cls,*args,**kwargs):
    """
    base_fields 会把这个表内的所有字段都拿到
    :param cls:  类本身
    :param args:
    :param kwargs:
    :return:
    """

    for field_name  in cls.base_fields:
        '''filed 就是字段的对象'''
        filed = cls.base_fields[field_name]

        attr_dic = {

                    'class':'form-control'
                    }

        '''更新到filed里面'''
        filed.widget.attrs.update(attr_dic)
        # print('dir(filed)', dir(filed))

    '''这样你就先加上自己的自定义属性，在继承modeform'''
    return ModelForm.__new__(cls)

def create_dynamic_modelform(model_class):

    class Meta:
        model = model_class
        fields = "__all__"

    #使用type来创建类
    dynmaic_modelform = type("DynamicModelForm",(ModelForm,),{'Meta':Meta,'__new__':__new__})
    return dynmaic_modelform
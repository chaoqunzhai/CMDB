from django.template import Library


register = Library()


##前端传入变量 这个simple_tag用来把你的表verbose_name_plural 列出来
@register.simple_tag()
def get_model_verbose_name(model_class):
    print('plural',model_class)
    return model_class._meta.verbose_name_plural

@register.simple_tag()
def get_app_name(model_class):
    return model_class._meta.model_name



@register.simple_tag()
def get_model_name(model_class):

    return model_class._meta.app_label
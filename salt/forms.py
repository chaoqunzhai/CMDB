from django.forms import Form
from django.forms import widgets
from django.forms import fields



class Hostname(Form):
    ip = fields.GenericIPAddressField(
        max_length=15,
        min_length=11,
        label='主机IP',
        widget=widgets.TextInput(attrs={'class':'form-control','placeholder':'192.168.22.100'}),
        error_messages={
            'required':'不能为空',
            'min_length':'最小为11个字符',
            'max_length':'最多为15个字符',
        }
    )
    kernel = fields.CharField(
        max_length=24,
        min_length=4,
        label='主机系统',
        widget=widgets.TextInput(attrs={'class':'form-control','placeholder':'Centos7'}),
        error_messages={
            'required':'不能为空',
            'min_length':'最小为4个字符',
            'max_length':'最多为24个字符',
        }
    )

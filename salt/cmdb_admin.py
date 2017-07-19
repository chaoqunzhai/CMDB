from salt import models
from cmdbAdmin.admin_base import site,BaseAdmin


class CustomerAdmin(BaseAdmin):
    list_display = ['ip','fun','fun_args','job']



site.register(models.Saltrun,CustomerAdmin)
print('----Admin[salt]---')
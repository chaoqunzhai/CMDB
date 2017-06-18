from django.contrib import admin

from salt import models

class Userlist(admin.ModelAdmin):
    list_display = ('name','email')


class Saltrun(admin.ModelAdmin):
    list_display = ('ip','fun','fun_args','job','date','statues')
    search_fields = ('job',)
    #快速选择下拉
    list_editable = ('statues',)

class Specieslist(admin.ModelAdmin):
    list_display = ('species_name','date','phone')

class Hostname(admin.ModelAdmin):
    list_display = ('ip','disk','cpu','kernel','source')
    #过滤-admin显示右侧栏目
    list_filter = ('ip','kernel','source')
    #搜索
    search_fields = ('ip','source')

class Server(admin.ModelAdmin):
    list_display = ('server_name','port','files','url')
    list_filter = ('server_name','port')






admin.site.register(models.Userprofile,Userlist)
admin.site.register(models.Hostname,Hostname)
admin.site.register(models.Saltrun,Saltrun)
admin.site.register(models.Server,Server)
admin.site.register(models.Species,Specieslist)

from django.conf.urls import url,include

from cmdbAdmin import views
urlpatterns = [

    url(r'^$', views.app_index,name="cmdbAdmin"),
    url(r'(\w+)/(\w+)/$', views.model_table_list,name="model_table_list"),

]

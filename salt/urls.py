from django.conf.urls import url,include


from salt import views


urlpatterns = [
    url(r'^hostlist', views.Hsotlist.as_view(), name="hostlist"),

    url(r'^salt_api_(?P<nid>\d+)$',views.APItDetailView.as_view()),
    url(r'^salt_api_json$', views.SaltApiJSON.as_view()),

    url(r'^salt_map$', views.SaltMap.as_view(), name="salt_map"),
    url(r'^salt_api$', views.SaltApi.as_view(), name="salt_api"),
]

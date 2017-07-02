from django.conf.urls import url,include


from salt.views import SaltApi
from salt.views import hostlist

urlpatterns = [
    url(r'^hostlist', hostlist.Hsotlist.as_view(), name="hostlist"),

    url(r'^salt_api_(?P<nid>\d+)$',hostlist.APItDetailView.as_view()),
    url(r'^salt_api_json$', hostlist.SaltApiJSON.as_view()),

    url(r'^salt_map$', SaltApi.SaltMap.as_view(), name="salt_map"),
    url(r'^salt_api$', SaltApi.SaltApi.as_view(), name="salt_api"),
]

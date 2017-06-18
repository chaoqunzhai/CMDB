from django.conf.urls import url,include


from salt import views


urlpatterns = [
    url(r'^salt_api$', views.APIView.as_view(), name="salt_api"),
    url(r'^salt_api_(?P<nid>\d+)$',views.APItDetailView.as_view()),
    url(r'^salt_api_json$', views.SaltApiJSON.as_view()),
    url(r'^salt_run$', views.SaltRun.as_view(), name="salt_run"),

]

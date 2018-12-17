from .views import UploadView
from django.conf.urls import url
from upload import views

urlpatterns = [

    url(r'^usernames/(?P<username>\w{1,11})/count/$', views.UploadView.as_view()),
]

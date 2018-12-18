from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^upload/', views.UploadView.as_view()),
    url(r'^audit/', views.AuditView.as_view()),
]

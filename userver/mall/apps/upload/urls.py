from django.conf.urls import url
from apps.upload import views

urlpatterns = {

    url(r'^/', views.UploadView.as_view(), name='upload'),
    url(r'^audit/', views.AuditView.as_view(), name='audit'),
}

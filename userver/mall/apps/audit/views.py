
from django.shortcuts import render

# Create your views here.
from userver.mall.apps.upload.models import Audit
from .models import models
from django.shortcuts import render

#定义人工审核函数
def audit(request,username):
    audit_list = models.Audit.objects.get(username=username)
    return render(request, 'audit.html', {"audit_list":audit_list})

def audit_pass(request):
    if request.method == "GET":
        if request.class="auditno"
        upload = Audit.objects.create(
            audit_pass = True
        )



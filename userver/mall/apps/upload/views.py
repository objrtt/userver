from django.shortcuts import render

import base64
# Create your views here.
import json
import os
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.views.generic import View
from .models import Audit
from django.http import JsonResponse, HttpResponse, request
from django.db import models

class UploadView(View):

    def get(self, request):
        """
        查询username
        路由：GET /upload/
        """
        queryset = Audit.objects.all()
        username_list = []
        for username in queryset:
            username_list.append({
                'username': username.id,
                'real_name': username.name,
            })
        return JsonResponse(username_list, safe=False)

    def post(self, request):
        """
        新增上传信息
        路由：POST /upload/
        """
        json_bytes = request.body
        json_str = json_bytes.decode()

        # base64_data = base64.b64encode(json_str)

        upload_dict = json.loads(json_str)



        upload = Audit.objects.create(
            username=base64.b64encode(upload_dict.get('username')),
            real_name=base64.b64encode(upload_dict.get('real_name')),
        )

        return JsonResponse({
            'username': upload.username,
        }, safe=False)

    def uploadimage(request):

        # <input type="file" name="image1"/># <input type="file" name="image1"/># <input type="file" name="image1"/>

        if request.POST:
            if request.method == 'POST':
                img = Audit(img_url=request.FILES.get('img'))
                img.save()

        return HttpResponseRedirect('/index/')



"""
# https://blog.csdn.net/c_beautiful/article/details/79755368
# https://blog.csdn.net/Rainbowsmile1/article/details/80403742
"""
import base64
import pickle
from django.views.generic import View
from .models import Audit
from django.http import HttpResponse
from .models import models
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import AuditSerializer
from rest_framework.response import Response


# class UploadView(View):
#     # 定义上传视图
#
#     def get(self, request):
#         """
#         查询username
#         路由：GET /upload/
#         """
#         queryset = Audit.objects.all()
#         username_list = []
#         for username in queryset:
#             username_list.append({
#                 'username': username.id,
#                 'real_name': username.name,
#             })
#         return JsonResponse(username_list, safe=False)
#
#     def post(self, request):
#         """
#         新增上传信息
#         路由：POST /upload/
#         """
#         json_bytes = request.body
#         json_str = json_bytes.decode()
#
#         # base64_data = base64.b64encode(json_str)
#
#         upload_dict = json.loads(json_str)
#
#
#
#         upload = Audit.objects.create(
#             username=base64.b64encode(upload_dict.get('username')),
#             real_name=base64.b64encode(upload_dict.get('real_name')),
#         )
#
#         return JsonResponse({
#             'username': upload.username,
#         }, safe=False)
#
#     def uploadimage(request):
#
#         # <input type="file" name="image1"/>#
#         # <input type="file" name="image2"/>#
#         # <input type="file" name="image3"/>
#
#         if request.POST:
#
#             img1 = request.FILES.get('image1')
#             img2 = request.FILES.get('image2')
#             img3 = request.FILES.get('image3')
#
#             upload = Audit.objects.create(
#
#                 id_card_posi=base64.b64encode(img1),
#                 id_card_nage=base64.b64encode(img2),
#                 hand_card_posi=base64.b64encode(img3)
#             )
#
#         return JsonResponse({"msg": "图片上传成功, 等待审核!"})


class UploadView(APIView):

    def post(self,request):
        # 接收数据
        data = request.data
        # 创建序列化器
        serializer = AuditSerializer(data=data)
        # 进行数据验证
        serializer.is_valid(raise_exception=True)
        # 数据入库
        id_card_image1 = serializer.data.get('id_card_posi')
        id_card_image2 = serializer.data.get('id_card_nega')
        hand_card_image3 = serializer.data.get('hand_card_posi')
        # 首先将json字符串转换为bytes类型
        # 正面
        image1 = pickle.dumps(id_card_image1)
        # 反面
        image2 = pickle.dumps(id_card_image2)
        # 手持
        image3 = pickle.dumps(hand_card_image3)
        # 在用base64对bytes类型的数据进行加密
        id_card_posi = base64.b64encode(image1)
        id_card_nega = base64.b64encode(image2)
        hand_card_posi = base64.b64encode(image3)
        serializer.save()
        # 返回响应
        return Response(
            serializer.data
        )



class AuditView(View):

    # 定义人工审核视图
    def audit(request, username):

        audit_list = models.Audit.objects.get(username='username')

        # 显示在前端页面
        return render(request, 'audit.html', {"audit_list":audit_list})


    def audit_pass(request):

        if request.method == "GET":

            return HttpResponse('审核失败')

        elif request.method == 'POST':

            a = Audit.objects.get(
                username='username'
            ).update(audit_pass=True)

            return HttpResponse(a, msg='审核成功')



"""
# https://blog.csdn.net/c_beautiful/article/details/79755368
# https://blog.csdn.net/Rainbowsmile1/article/details/80403742
"""




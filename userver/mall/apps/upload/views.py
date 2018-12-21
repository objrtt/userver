from django.views.generic import View
from crypt1.crypt1 import encrypt, decrypt
from fastdfs.fastdfs import MyStorage
from utils.get_filename.get_filename import Path_Name_fileExt
from apps.upload.models import Audit
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import AuditSerializer
from rest_framework.response import Response
from mall import settings
from rest_framework.authentication import SessionAuthentication    # 认证管理
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser   # 权限管理

import os

print(os.getcwd())

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

    # 认证管理  # 认证管理一般和权限管理配合使用
    authentication_classes = [SessionAuthentication]

    # 权限管理  # 通过python manager createsuperuser 就可以创建一个管理员账号,登录之后就可以访问
    permission_classes = [IsAuthenticated]

    def post(self,request):

        # 接收数据
        data = request.data

        # 创建序列化器
        serializer = AuditSerializer(data=data)

        # 进行数据验证
        serializer.is_valid(raise_exception=True)

        # 数据提取
        username = serializer.data.get('username')
        real_name = serializer.data.get('real_name')
        id_card = serializer.data.get('id_card')
        id_card_image1 = serializer.data.get('id_card_posi')
        id_card_image2 = serializer.data.get('id_card_nega')
        hand_card_image3 = serializer.data.get('hand_card_posi')

        # 提取图片名称
        image_path1, image_name1, image_extension1 = Path_Name_fileExt(id_card_image1)
        image_path2, image_name2, image_extension2 = Path_Name_fileExt(id_card_image2)
        image_path3, image_name3, image_extension3 = Path_Name_fileExt(hand_card_image3)

        # 对用户上传的各项信息 和 返回路径 加密,得到bytes类型
        # username = encrypt(username)
        real_name = encrypt(real_name)
        id_card = encrypt(id_card)
        id_card_posi = encrypt(id_card_image1)
        id_card_naga = encrypt(id_card_image2)
        hand_card_posi = encrypt(hand_card_image3)

        # 加密后图片存入fastdfs 返回各自路径,ip
        id_card_posi = MyStorage._save(image_name1, id_card_posi)
        id_card_naga = MyStorage._save(image_name2, id_card_naga)
        hand_card_posi = MyStorage._save(image_name3, hand_card_posi)


        # 加密后的数据存入mysql,此时图片类信息为bytes类型
        data = {
            username: 'username',
            real_name: 'real_name',
            id_card: 'id_card',
            id_card_posi: 'id_card_posi',
            id_card_naga: 'id_card_naga',
            hand_card_posi: 'hand_card_posi',
            }

        serializer.save()
        # 返回响应
        return Response(
            serializer.data
        )




class AuditView(View):

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAdminUser]  # 仅管理员用户

    # 定义人工审核视图
    def audit(request, username):

        # 数据库中提取出各项数据
        audit_list = Audit.objects.get(username='username')

        # 将数据解密得到原始数据和图片存储路径
        username = decrypt(audit_list.username)
        real_name = decrypt(audit_list.real_name)
        id_card = decrypt(audit_list.id_card)
        id_card_posi = decrypt(audit_list.id_card_image1_url)
        id_card_naga = decrypt(audit_list.id_card_image2_url)
        hand_card_posi = decrypt(audit_list.hand_card_image3_url)

        ip = settings.FDFS_URL

        # 将图片的存储路径补全
        id_card_posi = ip + id_card_posi
        id_card_naga = ip + id_card_naga
        hand_card_posi = ip + hand_card_posi

        data = {
            username: 'username',
            real_name: 'real_name',
            id_card: 'id_card',
            id_card_posi: 'id_card_posi',
            id_card_naga: 'id_card_naga',
            hand_card_posi: 'hand_card_posi',
        }

        # 显示在前端页面
        return render(request, 'audit.html', data)


    def audit_pass(request):

        if request.method == "GET":

            return HttpResponse(msg='审核失败')

        elif request.method == 'POST':

            a = Audit.objects.get(
                username='username'
            ).update(audit_pass=True)

            return HttpResponse(a, msg='审核成功')





"""
# https://blog.csdn.net/c_beautiful/article/details/79755368
# https://blog.csdn.net/Rainbowsmile1/article/details/80403742
"""




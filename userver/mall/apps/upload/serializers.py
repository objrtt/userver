import base64
from rest_framework import serializers
from .models import Audit
import re
import pickle
import sys
import os


class AuditSerializer(serializers.Serializer):

    # id = serializers.IntegerField(read_only=True, lable='ID')
    # username = serializers.CharField(max_length=11, label='手机号')
    # real_name = serializers.CharField(max_length=12, label='真实姓名')
    # id_card = serializers.CharField(max_length=18, label='身份证号码')
    # id_card_posi = serializers.CharField(required=True, label='身份证正面照片')
    # id_card_nage = serializers.CharField(required=True, label='身份证反面照片')
    # hand_id_posi = serializers.CharField(required=True, label='手持身份证照片')

    class Meta:
        model = Audit
        fields = ('id','username','real_name','id_card','id_card_posi','id_card_nage','hand_card_posi')


    # def validate_username(self, value):
    #
    #     if not re.match('1[3-9]{9}', value):
    #         raise serializers.ValidationError('手机号不符合格式')
    #     return value


    def validate_id_card(self, value):

        if not re.match('/(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/',value):
            raise serializers.ValidationError('身份证号码不符合格式')
        return value


    def validate_image(self, attrs):

        id_card_image1 = attrs.get('id_card_posi')
        id_card_image2 = attrs.get('id_card_nage')
        id_card_image3 = attrs.get('hand_card_posi')

        # 分别将json转化为byte
        image1 = pickle.dumps('id_card_posi')
        image2 = pickle.dumps('id_card_posi')
        image3 = pickle.dumps('hand_card_posi')

        # 再用base64加密
        id_card_posi = base64.b64encode('imageq')
        id_card_nage = base64.b64encode('image2')
        hand_card_posi = base64.b64encode('image3')


    def create(self, validated_data):

        user = Audit.objects.create(**validated_data)

        user.save()

        return user

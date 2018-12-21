import base64
from rest_framework import serializers
from upload.models import Audit
import re
import pickle


class AuditSerializer(serializers.Serializer):

    id = serializers.IntegerField(label='ID', read_only=True)
    username = serializers.CharField(label='手机号', max_length=11)
    real_name = serializers.CharField(label='真实姓名', max_length=12)
    id_card = serializers.CharField(label='身份证号码', max_length=18)
    id_card_posi = serializers.CharField(label='身份证正面照片', required=True, )
    id_card_nage = serializers.CharField(label='身份证反面照片', required=True, )
    hand_id_posi = serializers.CharField(label='手持身份证照片', required=True, )
    token = serializers.CharField(label='登录状态token', read_only=True)  # 增加token字段

    class Meta:
        model = Audit
        fields = ('id','username','real_name','id_card','id_card_posi','id_card_nage','hand_card_posi','token')


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

        # 生成token
        from rest_framework_jwt.settings import api_settings

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        # 1. jwt_paylaod_handler 自动生成一个二进制
        payload = jwt_payload_handler(user)

        # 2. 需要对 payload 进行编码，编码之后的才是token
        token = jwt_encode_handler(payload)

        user.token = token

        return user



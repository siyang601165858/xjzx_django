import re

from django_redis import get_redis_connection
from rest_framework import serializers


class SMSSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11, min_length=11, required=True)
    image_code = serializers.CharField(max_length=4, min_length=4, required=True)
    image_code_id = serializers.CharField(required=True)

    def validate(self, attrs):
        mobile = attrs['mobile']
        image_code = attrs['image_code']
        image_code_id = attrs['image_code_id']

        if not re.match(r'^1[3-9]\d{9}$', mobile):
            raise serializers.ValidationError('手机号不正确')
        conn = get_redis_connection('image_code')
        try:
            real_image_code = conn.get('ImageCode_' + image_code_id)
            if real_image_code:
                real_image_code = real_image_code.decode()
                conn.delete("ImageCode_" + image_code_id)
        except:
            raise serializers.ValidationError("获取图片验证码失败")

        if not real_image_code:
            raise serializers.ValidationError("验证码已过期")

        if image_code.lower() != real_image_code.lower():
            raise serializers.ValidationError('验证码输入错误')

        return attrs

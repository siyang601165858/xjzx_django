import re
from datetime import datetime

from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework.response import Response

from django_news.utils.response_code import RET
from users.models import User


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


class RegisterSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11, min_length=11, required=True)
    smscode = serializers.CharField(max_length=6, min_length=6, required=True, write_only=True)
    password = serializers.CharField(min_length=8, max_length=20, required=True, write_only=True)

    # class Meta:
    #     model = User
    #     fields = ['id', 'username', 'mobile']

    def validate(self, attrs):
        mobile = attrs['mobile']
        smscode = attrs['smscode']
        password = attrs['password']

        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return Response({'errno': RET.PARAMERR, 'errmsg': '手机号格式不正确'})

        if not re.match(r'^\w{8,20}$', password):
            return Response({'errno': RET.PARAMERR, 'errmsg': '密码不符要求,需要在8-20位之间'})

        conn = get_redis_connection('sms_code')
        try:
            real_sms_code = conn.get('sms_' + mobile)
        except:
            return Response({'errno': RET.DBERR, 'errmsg': '获取本地验证码失败'})

        if not real_sms_code:
            return Response({'errno': RET.NODATA, 'errmsg': "短信验证码过期"})

        if smscode != real_sms_code.decode():
            print(smscode)
            print(real_sms_code)
            return Response({'errno': RET.DATAERR, 'errmsg': "短信验证码错误"})

        # 从redis中删除短信验证码
        try:
            conn.delete('sms_' + mobile)
        except:
            print('删除短信验证码失败')

        return attrs

    def create(self, validated_data):
        # 获取数据
        mobile = validated_data['mobile']
        password = validated_data['password']
        # 创建对象
        user = User()
        # 设置属性
        user.username = mobile
        user.mobile = mobile
        user.set_password(password)
        # 改最后一次登录时间
        user.last_login = datetime.now()
        # 保存
        user.save()

        # 将用户信息保存到session中
        request = self.context['request']
        request.session['user_id'] = user.id
        request.session['username'] = user.username
        request.session['mobile'] = user.mobile

        return Response({'errno': RET.OK, 'errmsg': "创建用户成功"})


class LoginSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11, min_length=11, required=True)
    password = serializers.CharField(min_length=8, max_length=20, required=True, write_only=True)

    def validate(self, attrs):
        mobile = attrs['mobile']
        password = attrs['password']

        try:
            user = User.objects.get(mobile=mobile)
        except:
            return Response({'errno': RET.USERERR, 'errmsg': '用户不存在'})

        # 验证密码
        result = user.check_password(password)

        if not result:
            return Response({'errno': RET.PWDERR, 'errmsg': '密码错误'})

        # 放在这里,后面的视图要用
        attrs['user'] = user

        return attrs

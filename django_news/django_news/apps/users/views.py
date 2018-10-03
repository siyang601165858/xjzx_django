import random

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from django_news.libs.yuntongxun.sms import CCP
from django_news.utils.captcha.captcha import captcha
from django_news.utils.response_code import RET
from users.models import User
from users.serializers import SMSSerializer


class GetImageCode(APIView):

    def get(self, request):
        """
            获取图片验证码
            :return:
            """
        # 1. 获取到当前的图片编号id
        code_id = request.query_params.get('code_id')
        # 2.生成验证码
        name, text, image = captcha.generate_captcha()
        conn = get_redis_connection('image_code')
        try:
            # 保存当前生成的图片验证码内容到redis中
            conn.setex('ImageCode_' + code_id, 60 * 5, text)
        except:
            return Response({'errno': RET.DATAERR, 'errmsg': '保存图片验证码失败'})

        response = HttpResponse(image, content_type='image/jpg')
        print(text)
        return response


class SendSMSCode(APIView):

    def post(self, request):
        """
            1. 接收参数并判断是否有值
            2. 校验手机号是正确
            3. 通过传入的图片编码去redis中查询真实的图片验证码内容
            4. 进行验证码内容的比对
            5. 生成发送短信的内容并发送短信
            6. redis中保存短信验证码内容
            7. 返回发送成功的响应
            :return:
            """
        # 反序列化验证数据
        serializer = SMSSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 获取数据
        mobile = serializer.validated_data.get('mobile')
        # 另外2个就不需要再获取了,毕竟没用

        # 查一下看看该手机号是否已经注册过了
        try:
            user = User.objects.get(mobile=mobile)
        except:
            user = None

        if user:
            return Response({'errno': RET.DATAEXIST, 'errmsg': '该手机已被注册'})

        # 生成验证码
        sms_code = '%06d' % random.randint(0, 999999)
        print(sms_code)
        result = CCP().send_template_sms(mobile, [sms_code, 300 / 60], "1")
        # if result != 0:     # 不再发送短信
        #     return Response({'errno': RET.THIRDERR, 'errmsg': '发送短信失败'})

        # 将短信保存到redis中
        conn = get_redis_connection('sms_code')
        try:
            conn.setex('sms_' + mobile, 300, sms_code)
        except:
            return Response({'errno': RET.DBERR, 'errmsg': '保存短信失败'})

        return Response({'errno': RET.OK, 'errmsg': "发送成功"})

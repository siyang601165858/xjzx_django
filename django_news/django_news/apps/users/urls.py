from django.conf.urls import url
from users import views

urlpatterns = [
    url(r'^passport/image_code/$', views.GetImageCode.as_view()),
    url(r'^passport/sms_code/$', views.SendSMSCode.as_view()),
    url(r'^passport/register/$', views.RegisterView.as_view()),
    url(r'^passport/login/$', views.LoginView.as_view()),
]

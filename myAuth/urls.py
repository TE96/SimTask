from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from myAuth import views

# router = routers.DefaultRouter()
# router.register(r'api/v1/users', views.MyUserViewSet)

urlpatterns = [
    # url(r'^', include(router.urls)),
    url(r'^api/v1/users/registration', views.UserRegisterAPIView.as_view(), name='user-register'),
    url(r'^api/v1/users/login', views.UserLoginAPIView.as_view(), name='user-login'),
]

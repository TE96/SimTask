# coding=utf8
from django.core.cache import cache
from django.contrib.auth.hashers import check_password

from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import MyUser
from .serializers import MyUserRegisterSerializer, MyUserLoginSerializer


# Create your views here.

class UserLoginAPIView(APIView):
    """
    用户登录
    """
    queryset = MyUser.objects.all()
    serializer_class = MyUserLoginSerializer
    permission_classes = (AllowAny,)
    TIME_OUT = 60 * 60 * 18  # 单位：秒

    def get(self, request):
        data = request.data
        if data.get('uid'):
            user = MyUser.objects.filter(uid=data.get('uid'))
            serializer = MyUserLoginSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = MyUserLoginSerializer(self.__class__.queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        data = request.data
        uid = data.get('uid')
        password = data.get('password')
        try:
            user = MyUser.objects.get(uid=uid)
            if check_password(password, user.password):
                serializer = MyUserLoginSerializer(user)
                self.request.session['uid'] = user.uid
                token = Token.objects.get_or_create(user=user)
                print(dir(token), token)
                cache.set(user.uid, token, self.__class__.TIME_OUT)
                return Response({
                    'status': 'SUCCESS',
                    'token': token[0].key
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status': 'FAILED',
                    'error': '密码错误'
                }, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({
                'status': 'FAILED',
                'error': '该用户不存在'
            }, status=status.HTTP_400_BAD_REQUEST)


class UserRegisterAPIView(APIView):
    queryset = MyUser.objects.all()
    serializer_class = MyUserRegisterSerializer
    permission_classes = ()

    def post(self, request, format=None):
        data = request.data
        uid = data.get('uid')
        if MyUser.objects.filter(uid=uid):
            return Response({
                'status': "FAILED",
                'error': '该用户已被注册'
            }, status=status.HTTP_400_BAD_REQUEST)
        # print(data.get('username'))
        serializer = MyUserRegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = {
                "status": "SUCCESS",
                "userProfile": serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)


# class MyUserViewSet(viewsets.ModelViewSet):
#     queryset = MyUser.objects.all()
#     serializer_class = MyUserLoginSerializer
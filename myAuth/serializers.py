from rest_framework import serializers

from .models import MyUser


class MyUserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = []
        model = MyUser
        fields = ('uid', 'email', 'username', 'password', 'phone', 'gender')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        print(validated_data)
        user = MyUser(
            uid=validated_data['uid'],
            email=validated_data['email'],
            username=validated_data['username'],
            phone=validated_data['phone'],
            gender=validated_data['gender']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class MyUserLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ('uid', 'password')

from rest_framework import serializers
from user.models import CustomUser


class UserCreateSerializer (serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            'email',
            'nick_name',
            'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        email = validated_data.pop('email') 
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(
            email, password, **validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        email = data['username']
        password = data['password']
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to login.')
        if password is None:
            raise serializers.ValidationError(
                'A password is required to login.')
        if not CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'A user with this email was not found.')
        return data


class UserSerializer(serializers.Serializer):
    pass

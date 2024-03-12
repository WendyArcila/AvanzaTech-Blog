from rest_framework import serializers 
from user.models import CustomUser


class UserListSerializer (serializers.ModelSerializer):
    
    class Meta: 
        model = CustomUser
        fields = ['team','email', 'nick_name', 'is_admin', 'is_active', 'password' ]
        read_only_fields = ['team', 'is_admin', 'is_active']
        extra_kwargs = {'password': {'write_only': True}}
    
        def create(self, validated_data):
            user = CustomUser(
                email =  validated_data['email'],
                username = validated_data['nick_name']
            )
            user.set_password(validated_data['password'])
            user.save()
            return user
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['nick_name']
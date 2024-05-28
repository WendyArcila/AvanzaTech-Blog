# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from user.api.serializers import UserSerializer, UserCreateSerializer, UserLoginSerializer
from rest_framework import status



class UserCreateView(CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)


class UserLoginView(GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            serializer = UserLoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            user = authenticate(request, email=email, password=password)

            
            if user is None:
                raise AuthenticationFailed('Invalid Credentials')
            login(request, user)
            team_name = user.team.name if hasattr(user, 'team') else 'No Team Assigned'
            return Response(
                {"message": "Successfully Authenticated",
                    "id": user.id,
                    "nick_name": user.nick_name,
                    "team_name": team_name
                }, status=status.HTTP_200_OK)
        except AuthenticationFailed as e:
            return Response({"error": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(GenericAPIView):
    
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)

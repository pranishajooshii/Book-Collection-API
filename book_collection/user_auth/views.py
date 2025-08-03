from django.shortcuts import render
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
   
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            return Response({"message":"User registered successfully","user":serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
      serializer=LoginSerializer(data=request, context={'request': request})
      if serializer.is_valid():
            user=serializer.validated_data['user']
            token, created= Token.objects.get_or_create(user=user)  
            return Response({
                "message": "Login successful",
                "user": {
                    "email": user.email,
                    "fullname": user.fullname,
                },
                "token": token.key
            }, status=status.HTTP_200_OK)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
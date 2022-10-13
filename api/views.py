from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from api.serializers import *
from rest_framework import viewsets, status
from rest_framework import generics


# Create your views here.
def api(request):
	return HttpResponse("Initial API.")


class RegisterUser(APIView):

    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)

        if not serializer.is_valid():
        	return Response({'status': 403, 'error': serializer.errors, 'message': 'Something went wrong!'})

        serializer.save()

        user_obj = UserProfile.objects.get(username=serializer.data['username'])
        token_obj , _ = Token.objects.get_or_create(user=user_obj)

        return Response({'status': 201, 'data': serializer.data, 'token': str(token_obj)})



class ImageUpload(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ImageWareHouseSerializer

    def get_queryset(self):
        return ImageWareHouse.objects.filter(user=self.request.user, is_active=True)

    def perform_create(self, serializer):
        serializer = ImageWareHouseSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user, is_active=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



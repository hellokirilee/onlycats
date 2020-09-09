from django.http import Http404
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import CustomUser
from .serializers import CustomUserSerializer, LoginSerializer


class CustomUserList(APIView):

    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)


class CustomUserDetail(APIView):
    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        data = request.data
        serializer = CustomUserSerializer(
            instance=user,
            data=data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
   
   
class CreateUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class Login(APIView):
    permission_classes = [AllowAny]

    def get_object(self, username):
        try:
            return CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise Http404

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = self.get_object(username)
        if not user.check_password(password):
            return Response(
                {"error": "Incorrect password"},
                status=status.HTTP_400_BAD_REQUEST
            )

        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})

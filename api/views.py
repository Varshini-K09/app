from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, ProfileSerializer
from .models import User, Profile
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

class UserProfile(APIView):

    def post(self, request):

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():

            user = serializer.save()
            Profile.objects.create(user=user)

            return Response(
                {
                    "message": "User created successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    
    def delete(self, request):

        user_id = request.data.get('id')

        if not user_id:
            return Response(
                {"error": "User id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(id=user_id)
            user.delete()

            return Response(
                {
                    "message": "User deleted successfully"
                },
                status=status.HTTP_204_NO_CONTENT
            )

        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

class LoginView(APIView):

    def post(self, request):

        email = request.data.get('email')
        password = request.data.get('password')

        try:

            user = User.objects.get(email=email)

            if user.password != password:

                return Response(
                    {"error": "Invalid password"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            request.session['user_id'] = user.id

            return Response(
                {
                    "message": "Login successful",
                    "user_id": user.id
                },
                status=status.HTTP_200_OK
            )

        except User.DoesNotExist:

            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

class ProfileView(APIView):

    def get(self, request):

        user_id = request.session.get('user_id')

        if not user_id:

            return Response(
                {"error": "Login required"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:

            user = User.objects.get(id=user_id)

            profile = Profile.objects.get(user=user)

            serializer = ProfileSerializer(profile)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        except Profile.DoesNotExist:

            return Response(
                {"error": "Profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )


    def patch(self, request):

        user_id = request.session.get('user_id')

        if not user_id:

            return Response(
                {"error": "Login required"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:

            user = User.objects.get(id=user_id)

            profile = Profile.objects.get(user=user)

            serializer = ProfileSerializer(
                profile,
                data=request.data,
                partial=True
            )

            if serializer.is_valid():

                serializer.save()

                return Response(
                    {
                        "message": "Profile updated successfully",
                        "data": serializer.data
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        except Profile.DoesNotExist:

            return Response(
                {"error": "Profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )
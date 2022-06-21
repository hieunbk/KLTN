from django.db.migrations import serializer
from rest_framework.viewsets import ViewSet
from .serializers import UserProfileSerializer
from core.models import UserProfile
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
import orjson
from django.db.models import F


class UserViewSet(ViewSet):
    def list(self, request):
        users = UserProfile.objects.all().values()
        return Response(users)

    def create(self, request, *args, **kwargs):
        if not request.body:
            return Response("Data invalid", status=status.HTTP_204_NO_CONTENT)
        data = orjson.loads(request.body)

        username = data.get("username", None)
        username_check = UserProfile.objects.filter(username=username).first()
        if username_check:
            return Response("Username is existed", status=status.HTTP_400_BAD_REQUEST)
        password = data.get("password", None)
        email = data.get("email", None)
        email_check = UserProfile.objects.filter(email=email).first()
        if email_check:
            return Response("Email is existed", status=status.HTTP_400_BAD_REQUEST)

        gender = data.get("gender", None)
        date_of_birth = data.get("date_of_birth", None)
        identity_num = data.get("identity_num", None)
        mobile_number = data.get("mobile_number", None)
        country = data.get("country", None)
        address = data.get("address", None)
        province_info = data.get("province_info", None)
        district_info = data.get("district_info", None)
        ward_info = data.get("ward_info", None)

        user = UserProfile.objects.create(
            username=username,
            password=make_password(password),
            email=email,
            gender=gender,
            date_of_birth=date_of_birth,
            identity_num=identity_num,
            mobile_number=mobile_number,
            country=country,
            address=address,
            province_info=province_info,
            district_info=district_info,
            ward_info=ward_info,
        )
        user.save()
        if not user:
            return Response("Errol", status=status.HTTP_400_BAD_REQUEST)
        return Response("Successful", status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        if not request.body:
            return Response("Data invalid", status=status.HTTP_204_NO_CONTENT)
        data = orjson.loads(request.body)

        user_id = data.get("user_id", None)
        if not user_id:
            return Response("Miss user id", status=status.HTTP_400_BAD_REQUEST)

        username = data.get("username", None)
        email = data.get("email", None)
        gender = data.get("gender", None)
        date_of_birth = data.get("date_of_birth", None)
        identity_num = data.get("identity_num", None)
        mobile_number = data.get("mobile_number", None)
        country = data.get("country", None)
        address = data.get("address", None)
        province_info = data.get("province_info", None)
        district_info = data.get("district_info", None)
        ward_info = data.get("ward_info", None)

        user = UserProfile.objects.filter(id=user_id).first()
        if not user:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)
        if username:
            user.username = username
        if email:
            user.email = email
        if gender:
            user.gender = gender
        if date_of_birth:
            user.date_of_birth = date_of_birth
        if identity_num:
            user.identity_num = identity_num
        if mobile_number:
            user.mobile_number = mobile_number
        if country:
            user.country = country
        if address:
            user.address = address
        if province_info:
            user.province_info = province_info
        if district_info:
            user.district_info = district_info
        if ward_info:
            user.ward_info = ward_info
        serializer_data = UserProfileSerializer(user)
        return Response(serializer_data.data, status=status.HTTP_200_OK)
    
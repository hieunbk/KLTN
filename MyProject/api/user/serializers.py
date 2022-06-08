from rest_framework import serializers

class UserProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True, required=False)
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False)
    gender = serializers.CharField(max_length=20)
    date_of_birth = serializers.DateField()
    identity_num = serializers.CharField(max_length=15)
    mobile_number = serializers.CharField(max_length=10)
    country = serializers.CharField(max_length=50)
    address = serializers.CharField(max_length=100)
    province_info = serializers.CharField(max_length=50)
    district_info = serializers.CharField(max_length=50)
    ward_info = serializers.CharField(max_length=50)

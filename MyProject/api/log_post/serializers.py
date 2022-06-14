from rest_framework import serializers


class LogPostSerializer(serializers.Serializer):
    # id = serializers.IntegerField()
    user_id = serializers.CharField(max_length=20)
    object_id_post = serializers.CharField(max_length=50)
    province_search = serializers.CharField(max_length=200)
    district_search = serializers.CharField(max_length=200)
    price_search = serializers.FloatField(default=0)
    squad_search = serializers.CharField(max_length=100)




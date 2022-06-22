from rest_framework import serializers


class LogSearchSerializer(serializers.Serializer):
    # id = serializers.IntegerField()
    user_id = serializers.CharField(max_length=20)
    real_estate_type = serializers.CharField(max_length=200)
    province_search = serializers.IntegerField()
    district_search = serializers.IntegerField()
    price_search = serializers.FloatField(default=0)
    squad_search = serializers.CharField(max_length=100)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

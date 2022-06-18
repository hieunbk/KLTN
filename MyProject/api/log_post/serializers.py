from rest_framework import serializers

class LogPostSerializer(serializers.Serializer):
    # id = serializers.IntegerField()
    user_id = serializers.CharField(max_length=20)
    object_id_post = serializers.CharField(max_length=50)
    province_info = serializers.IntegerField()
    district_info = serializers.IntegerField()
    price_info = serializers.FloatField(default=0)
    squad_info = serializers.FloatField(default=0)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


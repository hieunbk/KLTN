from core.models import LogPost
from rest_framework import viewsets
from .serializers import LogPostSerializer
from rest_framework.response import Response
from rest_framework import status
import orjson


class LogPostViewSet(viewsets.ViewSet):
    def list(self, request):
        log_search = LogPost.objects.all()
        serializer = LogPostSerializer(log_search, many=True)
        return Response(serializer.data)


    def create(self, request):
        data = orjson.loads(request.body)
        user_id = data.get('user_id')
        if not user_id:
            return Response("Not user id")
        object_id_post = data.get("object_id_post")
        real_estate_type = data.get('real_estate_type')
        province_info = data.get('province_info')
        district_info = data.get('district_info')
        price_info = data.get('price_info')
        squad_info = data.get('squad_info')

        new_log = LogPost.objects.create(
            user_id=user_id,
            object_id_post=object_id_post,
            real_estate_type=real_estate_type,
            province_info=province_info,
            district_info=district_info,
            price_info=price_info,
            squad_info=squad_info
        )
        if not new_log:
            return Response("Errol", status=status.HTTP_400_BAD_REQUEST)
        return Response("Create successful", status=status.HTTP_201_CREATED)
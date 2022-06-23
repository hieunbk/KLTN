import orjson
from core.models import LogSearch
from rest_framework import viewsets
from .serializers import LogSearchSerializer
from rest_framework.response import Response
from rest_framework import status
from ..base.api_view import CustomAPIView


class LogSearchViewSet(viewsets.ViewSet):
    def list(self, request):
        user_id = self.request.query_params.get('user_id', None)
        log_search = LogSearch.objects.all()
        if user_id:
            log_search = log_search.filter(user_id=user_id)
        serializer = LogSearchSerializer(log_search, many=True)
        return Response(serializer.data)

    def create(self, request):
        if not request.body:
            return Response("Data invalid", status=status.HTTP_204_NO_CONTENT)

        data = orjson.loads(request.body)

        user_id = data.get('user_id')
        if not user_id:
            return Response("Not user id", status=status.HTTP_400_BAD_REQUEST)
        real_estate_type = data.get('real_estate_type')
        province_search = data.get('province_search')
        district_search = data.get('district_search')
        price_search = data.get('price_search')
        squad_search = data.get('squad_search')

        new_log = LogSearch.objects.create(
            user_id=user_id,
            real_estate_type=real_estate_type,
            province_search=province_search,
            district_search=district_search,
            price_search=price_search,
            squad_search=squad_search
        )
        if not new_log:
            return Response("Errol", status=status.HTTP_400_BAD_REQUEST)
        return Response("Create successful", status=status.HTTP_201_CREATED)

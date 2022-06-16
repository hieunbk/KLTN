import orjson
from core.models import LogSearch, LogPost, UserProfile
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, F, Sum, Avg


class RecommendPostViewSet(viewsets.ViewSet):
    def get_list_post(self, request):
        if not request.body:
            return Response("Data invalid", status=status.HTTP_204_NO_CONTENT)
        data = orjson.loads(request.body)
        user_id = data.get("user_id")

        if not user_id:
            return Response("Not user id", status=status.HTTP_400_BAD_REQUEST)

        user_search = LogSearch.objects.filter(user_id=user_id)
        user_post = LogPost.objects.filter(user_id=user_id)

        if user_post is None and user_search is None:
            return Response("New user", status=status.HTTP_204_NO_CONTENT)

        list_log_search = LogSearch.objects.filter(user_id=user_id).values('province_search').\
            annotate(count_province=Count('id')).order_by('-count_province')[:3]

        price_search_avg = LogSearch.objects.aggregate(Avg('price_search'))
        squad_search_avg = LogSearch.objects.aggregate(Avg('squad_search'))

        list_log_post = LogPost.objects.filter(user_id=user_id).values('province_post').\
            annotate(count_province=Count('id')).order_by('-count_province')[:3]

        return Response(list_log_search)
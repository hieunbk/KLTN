from builtins import print, property

import orjson
from core.models import LogSearch, LogPost, UserProfile
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, F, Sum, Avg


class RecommendPostViewSet(viewsets.ViewSet):
    def get_list_post(self, request, user_id):
        if not user_id:
            return Response("Not user id", status=status.HTTP_400_BAD_REQUEST)

        user = UserProfile.objects.filter(id=user_id).first()
        if not user:
            return Response("User id invalid", status=status.HTTP_400_BAD_REQUEST)
        user_province = user.province_info
        user_district = user.district_info

        user_search = LogSearch.objects.filter(user_id=user_id)
        if not user_search:
            if user_province and user_district:
                data_result = {
                    "user_id": user_id,
                    "province": user_province,
                    "district": user_district,
                }
                return Response(data_result, status=status.HTTP_200_OK)
            else:
                Response("No information. Update your profile", status=status.HTTP_400_BAD_REQUEST)

        user_post = LogPost.objects.filter(user_id=user_id)

        # if user_post is None and user_search is None:
        #     return Response("New user", status=status.HTTP_204_NO_CONTENT)

        list_province_search = LogSearch.objects.filter(user_id=user_id).values('province_search'). \
                                   annotate(count_province=Count('id')).order_by('-count_province')[:3]

        list_province_post = LogPost.objects.filter(user_id=user_id).values('province_info'). \
                                 annotate(count_province=Count('id')).order_by('-count_province')[:3]

        list_province = []
        list_district_province = []

        for province_search in list_province_search:
            for province_post in list_province_post:
                if province_search["province_search"] == province_post["province_info"]:
                    total = province_search["count_province"] + province_post["count_province"]
                    list_province.append([province_search["province_search"], total])

        for province in list_province:
            list_district_search = LogSearch.objects.filter(user_id=user_id, province_search=province[0]).values(
                'district_search'). \
                                       annotate(count_district=Count('id')).order_by('-count_district')[:3]

            list_district_post = LogPost.objects.filter(user_id=user_id, province_info=province[0]).values(
                'district_info'). \
                                     annotate(count_district=Count('id')).order_by('-count_district')[:3]

            for district_search in list_district_search:
                for district_post in list_district_post:
                    if district_search["district_search"] == district_post["district_info"]:
                        total_district = district_search["count_district"] + district_post["count_district"]
                        list_district_province.append([province[0], district_search["district_search"], total_district])

        max_count = 0
        max_index = 0
        for idx, address in enumerate(list_district_province):
            if address[2] >= max_count:
                max_count = address[2]
                max_index = idx
        province_result = list_district_province[max_index][0]
        district_result = list_district_province[max_index][1]

        price_search_avg = LogSearch.objects.aggregate(Avg('price_search'))
        squad_search_avg = LogSearch.objects.aggregate(Avg('squad_search'))
        
        price_post_avg = LogPost.objects.aggregate(Avg('price_info'))
        squad_post_avg = LogPost.objects.aggregate(Avg('squad_info'))
        
        price_result = (price_search_avg["price_search__avg"] + price_post_avg["price_info__avg"]) / 2
        squad_result = (squad_post_avg["squad_info__avg"] + squad_search_avg["squad_search__avg"]) / 2
        
        data_result = {
            "user_id": user_id,
            "province": province_result,
            "district": district_result,
            "price": price_result,
            "squad": squad_result
        }

        return Response(data_result, status=status.HTTP_200_OK)

import orjson
from core.models import LogSearch, LogPost, UserProfile
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, F, Sum, Avg
from ..utils.squad_price import SELLER_TYPE, LESSOR_TYPE


class RecommendPostViewSet(viewsets.ViewSet):
    def get_list_post(self, request, user_id):
        if not user_id:
            return Response("Not user id", status=status.HTTP_400_BAD_REQUEST)

        real_estate_type = self.request.query_params.get('real_estate_type', None)

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

        data_record = None
        if real_estate_type == SELLER_TYPE:
            data_record = LogSearch.objects.filter(user_id=user_id, real_estate_type=SELLER_TYPE)
        elif real_estate_type == LESSOR_TYPE:
            data_record = LogSearch.objects.filter(user_id=user_id, real_estate_type=LESSOR_TYPE)

        max_province_search = data_record.filter(user_id=user_id).values('province_search') \
            .annotate(count_province=Count('id')).order_by('-count_province')
        province_result = max_province_search[0]["province_search"] if max_province_search else None

        max_district_search = data_record.filter(user_id=user_id, province_search=province_result).values(
            'district_search').annotate(count_district=Count('id')).order_by('-count_district')
        district_result = max_district_search[0]["district_search"] if max_district_search else None

        max_price_search = data_record.filter(user_id=user_id).values('price_search') \
            .annotate(count_price=Count('id')).order_by('-count_price')
        price_result = int(max_price_search[0]["price_search"]) if max_price_search else None

        max_squad_search = data_record.filter(user_id=user_id, price_search=price_result).values('squad_search') \
            .annotate(count_squad=Count('id')).order_by('-count_squad') if price_result is not None \
            else data_record.filter(user_id=user_id).values('squad_search') \
            .annotate(count_squad=Count('id')).order_by('-count_squad')
        squad_result = max_squad_search[0]["squad_search"] if max_squad_search else None

        data_result = {
            "user_id": user_id,
            "real_estate_type": real_estate_type,
            "province": province_result,
            "district": district_result,
            "price": price_result,
            "squad": squad_result
        }
        return Response(data_result, status=status.HTTP_200_OK)

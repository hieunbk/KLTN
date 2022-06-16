from django.urls import path, include
from .views import RecommendPostViewSet

urlpatterns = [
    path('get-recommend-post', RecommendPostViewSet.as_view({'post': 'get_list_post'})),
]

from django.urls import path, include
from .views import RecommendPostViewSet

urlpatterns = [
    path('get-recommend-post/<int:user_id>', RecommendPostViewSet.as_view({'get': 'get_list_post'})),
]

from django.urls import path, include
from .views import LogSearchViewSet

urlpatterns = [
    path('get-log-search', LogSearchViewSet.as_view({'get': 'list'})),
    path('add-log-search', LogSearchViewSet.as_view({'post': 'create'})),
]

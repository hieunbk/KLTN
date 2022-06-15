from django.urls import path, include
from .views import LogPostViewSet

urlpatterns = [
    path('get-log-post', LogPostViewSet.as_view({'get': 'list'})),
    path('add-log-post', LogPostViewSet.as_view({'post': 'create'})),
]

from django.urls import path, include

from .login import UserLoginViewSet
from .views import UserViewSet

urlpatterns = [
    path('get-all-user', UserViewSet.as_view({'get': 'list'})),
    path('create', UserViewSet.as_view({'post': 'create'})),
    path('update', UserViewSet.as_view({'post': 'update'})),
    path('login', UserLoginViewSet.as_view({'post': 'post'})),
]

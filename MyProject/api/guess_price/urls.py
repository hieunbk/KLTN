from django.urls import path, include
from .views import GuessPrice

urlpatterns = [
    path('get-guess-price', GuessPrice.as_view({'post': 'get_guess_price'})),
]

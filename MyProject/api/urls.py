from django.urls import path, include

# app_name = 'core'
urlpatterns = [
    path('guess-price/', include("api.guess_price.urls")),
]
from django.urls import path, include

# app_name = 'core'
urlpatterns = [
    path('guess-price/', include("api.guess_price.urls")),
    path('user/', include("api.user.urls")),
    path('log-search/', include("api.log_search.urls")),
    # path('log_post/', include("api.log_post.urls")),
]
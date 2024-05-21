from django.urls import path, include
from . import views
    # path('members/spotify_callback', views.tokenn, name="getdatoken"),
urlpatterns = [
    path('', views.landing, name="login"),
    path('spotify_callback/', views.tokenn, name="getdatoken"),
    path('home/', views.home, name="homepage"),    
]
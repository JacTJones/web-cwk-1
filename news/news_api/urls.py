# from django.conf.urls import url
from django.urls import path, include
from .views import (
    loginApiView,
    registerApiView,
    logoutApiView,
    storyApiView,
    deleteStoryApiView,
)

# from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("login", loginApiView),
    path("register", registerApiView),
    path("logout", logoutApiView),
    path("stories", storyApiView),
    path("stories/<int:key>", deleteStoryApiView),
]

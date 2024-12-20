from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import MeetingViewSet, UserViewSet, ObtainTokenView
from rest_framework_simplejwt import views as jwt_views

router = DefaultRouter()
router.register(r"meetings", MeetingViewSet, basename="meeting")
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("token/", ObtainTokenView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
] + router.urls


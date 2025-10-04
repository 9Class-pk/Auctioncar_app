from .views import (UserProfileListAPIView, BrandViewSet, ModelCarViewSet,
                    CarListAPIView, CarImageViewSet, AuctionViewSet,
                    BidAPIView, FeedbackAPIView, CarDetailAPIView,
                    UserProfileDetailAPIView, RegisterView, LogoutView)
from rest_framework_simplejwt.views import(
        TokenObtainPairView,
    TokenRefreshView,TokenBlacklistView)

from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter

router = SimpleRouter()

router.register('brand', BrandViewSet)
router.register('model', ModelCarViewSet)
router.register('car-image', CarImageViewSet)
router.register('auction', AuctionViewSet)


urlpatterns = [
path('', include(router.urls)),
    path('cars/', CarListAPIView.as_view(), name='cars_list'),
    path('cars/<int:pk>/', CarDetailAPIView.as_view(), name='cars_detail'),
    path('bids/', BidAPIView.as_view(), name='bid_create'),
    path('feedbacks/', FeedbackAPIView.as_view(), name='feedback_create'),
    path('users/', UserProfileListAPIView.as_view(), name='user_list'),
    path('users/<int:pk>/', UserProfileDetailAPIView.as_view(), name='user_detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

]
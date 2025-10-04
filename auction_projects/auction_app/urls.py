from .views import (UserProfileViewSet, BrandViewSet, ModelCarViewSet,
                    CarViewSet, CarImageViewSet, AuctionViewSet,
                    BidViewSet, FeedbackViewSet)

from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register('user', UserProfileViewSet)
router.register('brand', BrandViewSet)
router.register('model', ModelCarViewSet)
router.register('car', CarViewSet)
router.register('car-image', CarImageViewSet)
router.register('auction', AuctionViewSet)
router.register('bid', BidViewSet)
router.register('feedback', FeedbackViewSet)


urlpatterns = [
path('', include(router.urls)),
]
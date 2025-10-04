from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from .filters import CarFilter
from .permission import IsSeller, IsBuyer, IsAdmin, IsOwner, IsSellerOwner, IsSellerOrAdmin
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import(
        TokenObtainPairView, TokenRefreshView)



class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class ModelCarViewSet(viewsets.ModelViewSet):
    queryset = ModelCar.objects.all()
    serializer_class = ModelCarSerializer


class CarListAPIView(generics.ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['model_car_name']
    ordering_fields = ['price', 'year']
    ordering = ["-created_at"]
    filterset_class = CarFilter
    permission_classes = [AllowAny]


class CarDetailAPIView(generics.RetrieveAPIView):
    queryset = Car.objects.all()
    serializer_class = CarDetailSerializer
    permission_classes = [AllowAny]


class CarCreateAPIView(generics.CreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsSellerOrAdmin]


class CarImageViewSet(viewsets.ModelViewSet):
    queryset = CarImage.objects.all()
    serializer_class = CarImageSerializer
    permission_classes = [IsSellerOrAdmin]


class AuctionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsSeller()]
        return [AllowAny()]


class BidAPIView(generics.CreateAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [IsBuyer]


class FeedbackAPIView(generics.CreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsBuyer]


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            "user": serializer.data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]


    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)





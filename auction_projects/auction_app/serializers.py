from .models import (UserProfile, Brand, ModelCar, Car,
                     CarImage, Auction, Bid, Feedback)
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES)

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'password_confirm',
                  'first_name', 'last_name', 'role')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = UserProfile.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user = UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")

        user = authenticate(username=user.username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")

        refresh = RefreshToken.for_user(user)
        attrs['access'] = str(refresh.access_token)
        attrs['refresh'] = str(refresh)
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields =  ['id', 'brand_name']


class ModelCarSerializer(serializers.ModelSerializer):

    class Meta:
        model = ModelCar
        fields =  ['id', 'brand', 'model_car_name']


class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ['image']


class CarListSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    model = ModelCarSerializer(read_only=True, many=True)
    images = CarImageSerializer(many=True, read_only=True)

    class Meta:
        model = Car
        fields = ['id', 'images', 'brand', 'model', 'year', 'fuel_type', 'transmission', 'mileage', 'price']


class CarDetailSerializer(serializers.ModelSerializer):
    brand = serializers.CharField(source='model_car.brand.brand_name', read_only=True)
    model = serializers.CharField(source='model_car.model_car_name', read_only=True)
    images = CarImageSerializer(many=True, read_only=True)
    seller = serializers.StringRelatedField()

    class Meta:
        model = Car
        fields =  ['images', 'brand', 'model', 'year', 'fuel_type', 'transmission',
                  'mileage', 'price', 'description', 'seller']


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'


class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = ['id', 'car', 'start_price', 'min_price', 'start_time', 'end_time', 'status']


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ['id', 'auction', 'buyer', 'amount', 'created_at']


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'seller', 'buyer', 'rating', 'comment', 'created_at']
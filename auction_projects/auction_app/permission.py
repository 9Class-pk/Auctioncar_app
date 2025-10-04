from rest_framework.permissions import BasePermission



class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"


class IsSeller(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "seller"


class IsBuyer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "buyer"


class IsSellerOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsSellerOrAdmin(BasePermission):
     def has_object_permission(self, request, view, obj):
        return request.user.role == "admin" or obj.owner == request.user
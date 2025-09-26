from rest_framework.permissions import BasePermission , SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.methode in SAFE_METHODS:
            return True
        return obj.user == request.user
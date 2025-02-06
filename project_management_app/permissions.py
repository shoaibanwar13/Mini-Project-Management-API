from rest_framework.permissions import BasePermission

class IsAdminPermissionOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role=="admin"
class IsMemberOrAdminOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        return request.user.role=="admin" or (request.user.role=="member" and request.method in ['GET','PATCH'])
         
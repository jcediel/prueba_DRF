from rest_framework import permissions


class IsStaffOrBasic(permissions.BasePermission):
    """
    Permite a staff ver y manipular todo, y a usuarios basic solo sus propios préstamos.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.role == "staff":
            return True
        return obj.member == request.user


class IsStaffOrSelfbasic(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == "staff":
            return True
        return obj.id == request.user.id

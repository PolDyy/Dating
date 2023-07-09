from rest_framework.permissions import BasePermission


class IsLikeYourself(BasePermission):
    def has_permission(self, request, view):
        return request.user.id != view.kwargs.get('id')


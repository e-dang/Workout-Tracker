from rest_framework import permissions


class IsOwner(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        pk = view.kwargs.get('pk', None)

        if pk is None:
            return super().has_permission(request, view)

        return super().has_permission(request, view) and str(request.user.pk) == pk

    def has_object_permission(self, request, view, obj):
        try:
            return obj.owner == request.user
        except AttributeError:
            return obj == request.user


class IsAdmin(permissions.IsAdminUser):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff

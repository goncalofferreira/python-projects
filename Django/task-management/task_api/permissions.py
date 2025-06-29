from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Só o dono da tarefa pode editá-la.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

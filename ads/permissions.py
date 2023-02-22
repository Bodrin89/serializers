from rest_framework.permissions import BasePermission

ROLE = ["moderator", "admin"]

class CheckAuthorPermission(BasePermission):

    message = "You are not the author"
    def has_object_permission(self, request, view, obj):
        if obj.author == request.user or request.user.role in ROLE:
            return True
        return False




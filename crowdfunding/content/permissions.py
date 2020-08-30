from rest_framework import permissions
#App Level Permissions are set to require authorisation.
#Is Owner or Read Only to be used for Forms/profile.
#Otherwise Users can not update/change items once created for content.


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
        


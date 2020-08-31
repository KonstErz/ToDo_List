from rest_framework.permissions import BasePermission


class GetAccessCompany(BasePermission):

    def has_permission(self, request, view):
        return bool(request.session.get('company_id'))

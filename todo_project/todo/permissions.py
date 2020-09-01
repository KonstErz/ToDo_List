from rest_framework.permissions import BasePermission


class GetAccessCompany(BasePermission):
    """
    Checking the permission to access the company,
    whether there is a company ID in the session.
    """

    def has_permission(self, request, view):
        return bool(request.session.get('company_id'))

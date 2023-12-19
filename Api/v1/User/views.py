from rest_framework import viewsets
from core.Utils.Api.permissions import IsSuperuserPermission
from .serializers import UserSerializer
from core.User.models import User


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = (IsSuperuserPermission,)

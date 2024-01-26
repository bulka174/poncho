from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from account.models import Vendor
from account.permissions import IsAccountOwner, IsAccountOwnerOrAdmin, IsHead, IsHeadOrAdmin
from account.serializers import UserSerializer, UserListSerializer, UserProfileSerializer, \
    VendorSerializer, VendorListSerializer, VendorProfileSerializer, UserRegisterSerializer


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action in ('update', 'partial_update'):
            return [IsAccountOwner()]
        elif self.action == 'destroy':
            return [IsAccountOwnerOrAdmin()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegisterSerializer
        elif self.action == 'list':
            return UserListSerializer
        elif self.action in ('update', 'partial_update', 'retrieve'):
            return UserProfileSerializer
        return UserSerializer


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def get_permissions(self):
        if self.action in ('update', 'partial_update'):
            return [IsHead()]
        elif self.action == 'destroy':
            return [IsHeadOrAdmin()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.action == 'list':
            return VendorListSerializer
        if self.action == 'retrieve':
            return VendorProfileSerializer
        return VendorSerializer

    def perform_create(self, serializer):
        serializer.save(head=self.request.user)
        vendor_instance = serializer.instance
        vendor_instance.members.add(self.request.user)

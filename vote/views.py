from django.shortcuts import render
from rest_framework import viewsets
from .permissions import ReadOnlyOrAthorPerm as ReadOnlyOrAuthorPerm
from . models import (
        Category, Nomination, Preference, Vote)
from .serializers import (
        CategorySerializer, NominationSerializer,
        PreferenceSerializer, VoteSerializer)
# Create your views here

class CategoryViewSet(viewsets.ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    permission_classes=[ReadOnlyOrAuthorPerm]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)


class NominationViewSet(viewsets.ModelViewSet):
    queryset=Nomination.objects.all()
    serializer_class=NominationSerializer
    permission_classes=[ReadOnlyOrAuthorPerm]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)


class PreferenceViewSet(viewsets.ModelViewSet):
    queryset=Preference.objects.all()
    serializer_class=PreferenceSerializer
    permission_classes=[ReadOnlyOrAuthorPerm]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)


class VoteViewSet(viewsets.ModelViewSet):
    queryset=Vote.objects.all()
    serializer_class=VoteSerializer
    permission_classes=[ReadOnlyOrAuthorPerm]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)



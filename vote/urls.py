from rest_framework.routers import DefaultRouter
from .views import (CategoryViewSet,
    NominationViewSet, PreferenceViewSet, VoteViewSet
)

router=DefaultRouter()

router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"nominations", NominationViewSet, basename="nominations")
router.register(r"preference", PreferenceViewSet, basename="preferences")
router.register(r"votes", VoteViewSet, basename="votes")

urlpatterns=router.urls

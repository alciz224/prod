from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . views import AlbumViewSet, ArtistViewSet, LikeToggleView, PostViewSet, TrackViewSet, CommentViewSet, EventViewSet

router=DefaultRouter()

router.register(r"posts", PostViewSet, basename="posts")
router.register(r"events", EventViewSet, basename="events")
router.register(r"comments", CommentViewSet, basename="comments")
router.register(r"likes", LikeToggleView, basename="likes")
router.register(r'artists', ArtistViewSet, basename="artist")
router.register(r'albums', AlbumViewSet, basename="albums")
router.register(r"tracks", TrackViewSet, basename="tracks")

urlpatterns=router.urls


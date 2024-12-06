
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from . models import Album, Post, Event, Reaction, Comment, Reaction, Artist, Track
from . serializers import ArtistSerializer, CommentSerializer, EventSerializer, LikeSerializer, PostSerializer, AlbumSerializer, TrackSerializer
from . permissions import ReadOnlyOrAthorPerm

#--------POST VIEWS---------
class PostViewSet(viewsets.ModelViewSet):
    queryset=Post.objects.all()
    serializer_class=PostSerializer
    permission_classes=[ReadOnlyOrAthorPerm]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)


class EventViewSet(viewsets.ModelViewSet):
    serializer_class=EventSerializer
    queryset=Event.objects.all()
    permission_classes=[ReadOnlyOrAthorPerm]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class=CommentSerializer
    permission_classes=[ReadOnlyOrAthorPerm]
    queryset=Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)

# --------LIKE VIEWS SECTION-----------
class LikeToggleView(viewsets.ModelViewSet):
    serializer_class=LikeSerializer
    queryset=Reaction.objects.all()
    permission_classes = [ReadOnlyOrAthorPerm]

    def create(self, request, *args, **kwargs):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=request.user
        content_type=serializer.validated_data["content_type"]
        object_id=serializer.validated_data["object_id"]

        like, created=Reaction.objects.get_or_create(
            user=user,
            content_type=content_type,
            object_id=object_id
        )

        if not created:
            like.delete()
            return Response({"detail":"Like removed successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

#-----------ARTIST VIEWS --------
class ArtistViewSet(viewsets.ModelViewSet):
    serializer_class=ArtistSerializer
    queryset=Artist.objects.all()
    permission_classes=[ReadOnlyOrAthorPerm]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)

class AlbumViewSet(viewsets.ModelViewSet):
    serializer_class=AlbumSerializer
    queryset=Album.objects.all()
    permission_classes=[ReadOnlyOrAthorPerm]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)

class TrackViewSet(viewsets.ModelViewSet):
    serializer_class=TrackSerializer
    queryset=Track.objects.all()
    permission_classes=[ReadOnlyOrAthorPerm]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)




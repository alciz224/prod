from typing import Required
from django.db.models.expressions import fields
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from rest_framework.compat import apply_markdown
from rest_framework.validators import ValidationError
from .models import (
    Artist,
    Album,
    Track,
    Comment,
    Reaction,
    SocialMedia,
    StreamingPlatform,
    ArtistLink,
    AlbumTrackLink,
    Event,
    EventAssociatedImage,
    Post,
)


class ArtistSerializer(serializers.ModelSerializer):
    user=serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Artist
        fields = '__all__'


class AlbumSerializer(serializers.ModelSerializer):
    user=serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Album
        fields = '__all__'


class TrackSerializer(serializers.ModelSerializer):
    user=serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Track
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    comments=serializers.SerializerMethodField()
    likes=serializers.SerializerMethodField()
    user=serializers.ReadOnlyField(source='user.username')
    #    content_type=serializers.ModelField(source='content_type.model', model_field='content_type__model')  
    class Meta:
        model = Comment
        fields = ["id", "text", "content_type", "object_id", "parent", "user","comments", "user", "likes"]
        #['id', 'text', 'content_type', 'created_at', 'user', 'object_id', 'content_object', 'comments', 'likes']

    def get_comments(self, obj):
        child_comments=obj.comments.count()
        return child_comments

    def get_likes(self, obj):
        comment_likes=obj.likes.count()
        return comment_likes


class LikeSerializer(serializers.ModelSerializer):
    user=serializers.ReadOnlyField(source='user.username')
    content_type=serializers.PrimaryKeyRelatedField(queryset=ContentType.objects.filter(model__in=["post","event","comment"]))
    class Meta:
        model=Reaction
        fields="__all__"


class SocialMediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = SocialMedia
        fields = '__all__'


class StreamingPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreamingPlatform
        fields = '__all__'


class ArtistLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistLink
        fields = '__all__'


class AlbumTrackLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumTrackLink
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    user=serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Event
        fields = '__all__'


class EventAssociatedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventAssociatedImage
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    user=serializers.ReadOnlyField(source='user.username')
    comments=serializers.SerializerMethodField()
    likes=serializers.SerializerMethodField()
    user=serializers.ReadOnlyField(source='user.id')
    class Meta:
        model = Post
        fields = ("id", "title", "content", "user", "photo", "created_at", "comments", "likes")

    def get_comments(self, obj):

        main_comments = obj.comments.count()
    
        return main_comments

    def get_likes(self, obj):
        total_likes= obj.likes.count()
        return total_likes


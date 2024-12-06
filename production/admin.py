from django.contrib import admin
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
    Post)


# Register your models here.
admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Track)
admin.site.register(Comment)
admin.site.register(Reaction)
admin.site.register(SocialMedia)
admin.site.register(StreamingPlatform)
admin.site.register(ArtistLink)
admin.site.register(AlbumTrackLink)
admin.site.register(Event)
admin.site.register(EventAssociatedImage)
admin.site.register(Post)

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.auth.models import User
from django.db.transaction import commit
from django.utils.translation import gettext_lazy as _


class Artist(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo=models.ImageField(upload_to='artist/images', null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Album(models.Model):
    title = models.CharField(max_length=255)
    artist = models.ManyToManyField(Artist, related_name='albums')
    cover = models.ImageField(upload_to='album_covers/')
    release_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Track(models.Model):
    title = models.CharField(max_length=255)
    album = models.ForeignKey(
        Album, on_delete=models.CASCADE, related_name='tracks', null=True, blank=True)
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name='tracks')
    feat = models.ManyToManyField(
        Artist, related_name='featured_on', blank=True)
    audio_file = models.FileField(upload_to='tracks/')
    duration = models.DurationField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Link(models.Model):
    name = models.CharField(max_length=255, unique=True)
    icon_image = models.ImageField(upload_to='icons/', blank=True, null=True)

    class Meta:
        abstract = True


class SocialMedia(Link):
    pass


class StreamingPlatform(Link):
    pass


class ArtistLink(models.Model):
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name='artist_links')
    social_media = models.ForeignKey(SocialMedia, on_delete=models.CASCADE)
    link = models.URLField()

    class Meta:
        unique_together=["artist", "social_media"]

    def __str__(self):
        return f"{self.artist.name} - {self.social_media.name}"


class AlbumTrackLink(models.Model):
    album = models.ForeignKey(
        Album, on_delete=models.CASCADE, null=True, blank=True)
    track = models.ForeignKey(
        Track, on_delete=models.CASCADE, null=True, blank=True)
    streaming_platform = models.ForeignKey(
        StreamingPlatform, on_delete=models.CASCADE)
    link = models.URLField()

    def clean(self):
        if self.album and self.track:
            raise ValidationError(
                "Only one of album or track can be selected.")
        if not self.album and not self.track:
            raise ValidationError("Either album or track must be selected.")

    def __str__(self):
        return f"Link for {'album' if self.album else 'track'} on {self.streaming_platform.name}"


class Post(models.Model):
    title = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("Titre")
    )
    content = models.TextField(
        verbose_name=_("Contenu")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo=models.ImageField(upload_to="post", null=True, blank=True)
    likes=GenericRelation("Reaction")
    comments=GenericRelation("Comment")


    def __str__(self):
        return self.title


class Event(models.Model):
    class EventType(models.TextChoices):
        CONCERT = "CONCERT", _("Concert")

        FESTIVAL = "FESTIVAL", _("Festival")

        ALBUM_OR_SINGLE_RELEASE = "ALBUM_OR_SINGLE_RELEASE", _("Sortie d'album ou d'un single")
        
        AWARD = "AWARD", _("Cérémonie de récompence")
    name = models.CharField(max_length=255)
    description = models.TextField(
        blank=True, null=True)
    category = models.CharField(
        max_length=255, 
        choices=EventType.choices, 
        null=False, blank=False)
    start_date = models.DateTimeField(
        verbose_name=_("Début de l'évènement"))
    end_date = models.DateTimeField(
        verbose_name=_("Fin de l'évènement")
    )
    place = models.CharField(
        max_length=255,
        verbose_name=_("Lieu de l'évènement")
    )
    ticket_link = models.URLField(
        blank=True, null=True,
        verbose_name=_("Lien pour le ticket")
    )
    whatsapp_info = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name=_("Numero WhatsApp pour plus d'info")
    )
    is_ongoing = models.BooleanField(
        default=False,
        verbose_name=_("Est-ce un évènement à venir?")
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    photo=models.ImageField(upload_to="event", null=True, blank=True)
    likes=GenericRelation("Reaction")

    def __str__(self):
        return self.name



class EventAssociatedImage(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='associated_images')
    image = models.ImageField(upload_to='event_associated_images/', null=True, blank=True)
    name = models.CharField(max_length=255, blank=True,
                            null=True)  # For branding purposes

    def __str__(self):
        return f"Image for {self.event.name}"


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    text = models.TextField()
    content_type= models.ForeignKey(
        ContentType, on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    content_object=GenericForeignKey(
        "content_type", "object_id")
    parent=models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name="replies")
    created_at = models.DateTimeField(auto_now_add=True)
    likes=GenericRelation("Reaction")
    comments=GenericRelation("Comment")





    def __str__(self):
        if self.parent:
            return f"@{self.user} replied a comment: {self.text[0:10]}..."
        
        if self.content_type:
            return f"@{self.user} commented {self.content_type.model}: {self.text[0:10]}{'...' if len(self.text) > 10 else None}"
        return f"Comment object with id {self.id}"



    @property
    def main_comment(self):
        return self.parent if self.parent else self


class Reaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    created_at = models.DateTimeField(auto_now_add=True)


#    class Meta:
#        unique_together=["user","content_type","object_id"]



    def __str__(self):
        return f"Liked by {self.user.username}"


# Create your models here.

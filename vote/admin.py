from django.contrib import admin
from .models import (
    Award,
    Category,
    Nomination,
    Preference,
    Vote,
)

# Register your models here.
admin.site.register(Category)
admin.site.register(Nomination)
admin.site.register(Preference)
admin.site.register(Vote)
admin.site.register(Award)
# Register your models here.

from django.shortcuts import render
from django.http import HttpResponse
from production.models import Reaction

def home(request):
    reactions=Reaction.objects.first()
    print(type(reactions.content_type))
    if request.htmx:
        return HttpResponse('Htmx Request')

    return render(request, 'base.html')

from django.shortcuts import render
from django.template import RequestContext

def index(request):
    if request.user != "AnonymousUser":
        return render(request, "templates_website/index.html")
    else:
        return render(request, "templates_website/index.html")


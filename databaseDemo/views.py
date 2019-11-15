from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello! Welcome to databaseDemo for methylation-sequencing project.")

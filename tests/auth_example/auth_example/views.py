from django.http import HttpResponse


def permission_denied_handler(request):
    return HttpResponse("you have no permissions!")

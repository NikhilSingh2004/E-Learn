from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def PageNotFound(request : HttpRequest, anything : str) -> HttpResponse:
    return HttpResponse('Page Not Found!')
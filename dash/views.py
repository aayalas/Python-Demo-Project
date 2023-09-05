from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

# Create your views here.
def index(request):
    return render( request, 'dash/index.html' )
    permission_classes = [IsAuthenticated]
       


def settings(request):
    return render( request, 'settings.html' )
    permission_classes = [IsAuthenticated]
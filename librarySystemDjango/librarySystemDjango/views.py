from django.shortcuts import render

def home(request):
    return render(request, 'librarySystemDjango/home.html')

def about(request):
    return render(request, 'librarySystemDjango/about.html')
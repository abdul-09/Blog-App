from django.shortcuts import redirect, render

def home_view(request):
    return redirect('blog/')

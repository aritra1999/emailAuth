from django.shortcuts import render


def home_view(request):
    context = {
        'title': 'Home'
    }
    return render(request, 'dashboard/home.html', context)

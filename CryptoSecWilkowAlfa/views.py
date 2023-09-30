# simpleapp/views.py
from django.shortcuts import render, redirect
from .models import Name
from .forms import NameForm


def index(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            # form.save()
            return redirect('index')
    else:
        form = NameForm()

    names = Name.objects.all()

    return render(request, 'index.html', {'form': form, 'names': names})
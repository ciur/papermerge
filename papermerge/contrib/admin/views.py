from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def browse(request):
    return render(request, "admin/index.html")

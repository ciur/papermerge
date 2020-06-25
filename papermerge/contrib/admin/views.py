from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def browse(self):
    return render("admin/browse.html")

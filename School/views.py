from django.contrib import messages
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def home(request):
    return render(request, "School/home.html")


def about(request):
    return render(request, "School/about.html")


def faq(request):
    return render(request, "School/faq.html")


def contact(request):
    return render(request, "School/contact.html")

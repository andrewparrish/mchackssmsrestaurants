# Create your views here.
from django.shortcuts import render_to_response, redirect, render

def test(request):
	return render(request, 'main/main.html')
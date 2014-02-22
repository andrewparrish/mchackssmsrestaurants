# Create your views here.
from django.shortcuts import render_to_response, redirect, render
from django.http import HttpResponseRedirect, HttpResponse

import json

def test(request):
	return render(request, 'main/main.html')


def search(request):
	q = request.GET.get('q', '')
	crossone = request.GET.get('crossone', '')
	crosstwo = request.GET.get('crosstwo', '')
	response = {}
	response['q'] = q
	response['crossone'] = crossone
	response['crosstwo'] = crosstwo

	return HttpResponse(json.dumps(response), content_type="application/json")
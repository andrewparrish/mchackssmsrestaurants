# Create your views here.
from django.shortcuts import render_to_response, redirect, render
from django.http import HttpResponseRedirect, HttpResponse
import urllib2
import urllib

import json

def test(request):
	return render(request, 'main/index2.html')


def search(request):
	q = request.GET.get('q', '')
	crossone = request.GET.get('crossone', '')
	crosstwo = request.GET.get('crosstwo', '')
	response = {}
	response['q'] = q
	response['crossone'] = crossone
	response['crosstwo'] = crosstwo

	url = 'https://maps.googleapis.com/maps/api/geocode/json?'
	params = urllib.urlencode({
		'address' : 'president kennedy ave and rue city councillors st',
		'sensor' : 'false'
		})
	j = urllib2.urlopen(url+params)
 	jsonparse = json.load(j)

	return HttpResponse(json.dumps(jsonparse), content_type="application/json")
# Create your views here.
from django.shortcuts import render_to_response, redirect, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext

import urllib2
import urllib

import json
import re

def foodchoose(food):
	match = re.search(r'(\w+)\s+near\s+(\w+\s+)', food.lower())
	matchtwo = re.search(r'(\w+)\s+(\w+\s+)', food.lower())
	if match:
		return match
	elif matchtwo and matchtwo.group(1) is not 'near':
		return match
	else:
		return 'false'

def gmaps(where):
	url = 'https://maps.googleapis.com/maps/api/geocode/json?'
	params = urllib.urlencode({
		'address' : ''+where,
		'sensor' : 'false'
		})
	j = urllib2.urlopen(url+params)
	jsonparse = json.load(j)
	return jsonparse

def places(latitude, longitude, food):
	url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
	params = urllib.urlencode({
		'location' : str(latitude)+','+str(longitude),
		'keyword' : food,
		'sensor' : 'false'
		})
	j = urllib2.urlopen(url+params)
	jsonparse = json.load(j)
	return jsonparse

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
	jsonparse = gmaps(crossone, crosstwo)

	return HttpResponse(json.dumps(jsonparse), content_type="application/json")

def preferences(request):
	if request.method == 'POST':
		food = request.POST.get('food', '')
		where = request.POST.get('where')
		
		foodarr = foodchoose(food)
		jsonstuff = gmaps(where)
		jsonstr = json.dumps(jsonstuff)
		if jsonstuff['status'] == 'OK':
			print 'okay'
			results = jsonstuff['results']
			mapping =results[0]
			location = mapping['geometry']
			latlong = location['location']
			latitude = latlong['lat']
			longitude = latlong['lng']
			print foodarr
			if foodarr is 'false':
				foodinput = 'food'
			else:
				foodinput = foodarr.group(0)

			placelist = places(latitude, longitude, foodinput)
			
			return HttpResponse(json.dumps(placelist), content_type="application/json")
		else:
			redirect('/preferences')


		if foodarr is 'false' or crossone is '' or crosstwo is '':
			redirect('/preferences')
	return render_to_response('preferences.html',{},context_instance=RequestContext(request))

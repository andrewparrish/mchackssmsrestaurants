# Create your views here.
from django.shortcuts import render_to_response, redirect, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext

import urllib2
import urllib

import json
import re
from datetime import *

from place import *

def gmaps(where):
	url = 'https://maps.googleapis.com/maps/api/geocode/json?'
	params = urllib.urlencode({
		'address' : ''+where,
		'sensor' : 'false',
		})
	j = urllib2.urlopen(url+params)
	jsonparse = json.load(j)
	return jsonparse

def places(latitude, longitude, food):
	url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
	params = urllib.urlencode({
		'key' : 'AIzaSyAiWF1P0ha-Kxz9ahNz14at5FVKeUb1oiE',
		'location' : str(latitude)+','+str(longitude),
		'keyword' : food,
		'sensor' : 'false',
		'rankby' : 'distance'
		})
	j = urllib2.urlopen(url+params)
	jsonparse = json.load(j)
	return jsonparse

def placelisting(jsonin):
	places = []
	for place in jsonin:
		geometry = place['geometry']
		latlong = geometry['location']
		newplace = make_foodplace(place.get('rating', 0.0) , place['name'], place.get('price_level', 0), latlong['lat'], latlong['lng'], place.get('vicinity', ''))
		places.append(newplace)
	return places

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

def home(request):
	return render(request, 'main/index2.html')

def directionsto(latitude, longitude, destination):
	url = 'https://maps.googleapis.com/maps/api/directions/json?'
	params = urllib.urlencode({
		'key' : 'AIzaSyAiWF1P0ha-Kxz9ahNz14at5FVKeUb1oiE',
		'origin' : str(latitude)+str(',')+str(longitude),
		'destination' : str(destination.latitude)+str(',')+str(destination.longitude),
		'sensor' : 'false',
		'mode' : 'transit',
		'departure_time' : str(int(datetime.now().strftime("%s")) * 1000)
		})
	j = urllib2.urlopen(url+params)
	jsonparse = json.load(j)
	if jsonparse['status'] == 'ZERO_RESULTS':
		params = urllib.urlencode({
		'key' : 'AIzaSyAiWF1P0ha-Kxz9ahNz14at5FVKeUb1oiE',
		'origin' : str(latitude)+str(',')+str(longitude),
		'destination' : str(destination.latitude)+str(',')+str(destination.longitude),
		'sensor' : 'false',
		'mode' : 'walking'
		})
		j = urllib2.urlopen(url+params)
		jsonparse = json.load(j)
	return jsonparse

def gotoplace(request):
	if request.method == 'POST':
		food = request.POST.get('food', 'food')
		where = request.POST.get('where')
		
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

			placelist = places(latitude, longitude, food)
			if placelist['status'] == 'OK':
				placelistsimple = placelisting(placelist['results'])
				print placelistsimple[0].name
				print directionsto(latitude, longitude, placelistsimple[0])
				redirect('/')
			else:
				redirect('/preferences')
		else:
			redirect('/preferences')
	return render_to_response('preferences.html',{},context_instance=RequestContext(request))

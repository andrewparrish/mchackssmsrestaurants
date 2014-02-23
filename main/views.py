# Create your views here.
from django.shortcuts import render_to_response, redirect, render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext

import urllib2
import urllib

import json
import re
from datetime import *

from place import *

from main.models import Directions

def gmaps(where):
	url = 'https://maps.googleapis.com/maps/api/geocode/json?'
	params = urllib.urlencode({
		'address' : ''+where,
		'sensor' : 'false',
		})
	j = urllib2.urlopen(url+params)
	jsonparse = json.load(j)
	return jsonparse

def places(latitude, longitude, keyword):
	url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
	params = urllib.urlencode({
		'key' : 'AIzaSyAiWF1P0ha-Kxz9ahNz14at5FVKeUb1oiE',
		'location' : str(latitude)+','+str(longitude),
		'keyword' : keyword,
		'sensor' : 'false',
		'radius' : 16093
		})
	j = urllib2.urlopen(url+params)
	jsonparse = json.load(j)
	return jsonparse

def placelisting(jsonin):
	places = []
	for place in jsonin:
		geometry = place['geometry']
		latlong = geometry['location']
		newplace = make_place(place.get('rating', 0.0) , place['name'], place.get('price_level', 0), latlong['lat'], latlong['lng'], place.get('vicinity', ''))
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
		'departure_time' : str(int(datetime.now().strftime("%s")))
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

def directionslistcomplete(keyword, where):
	directionlist = []
	jsonstuff = gmaps(where)
	jsonstr = json.dumps(jsonstuff)
	if jsonstuff['status'] == 'OK':
		results = jsonstuff['results']
		mapping =results[0]
		location = mapping['geometry']
		latlong = location['location']
		latitude = latlong['lat']
		longitude = latlong['lng']

		placelist = places(latitude, longitude, keyword)
		if placelist['status'] == 'OK':
			placelistsimple = placelisting(placelist['results'])
			direct = directionsto(latitude, longitude, placelistsimple[0])
			legs = direct['routes'][0]['legs']
			for leg in legs:
				steps = leg['steps']
				for step in steps:
					if step['travel_mode'] == unicode('WALKING'):
						directionlist.append(str(step['html_instructions']))
					elif step['travel_mode'] == unicode('TRANSIT'):
						directionlist.append(str('Take '+step['transit_details']['line']['name']+' to '+step['transit_details']['arrival_stop']['name']))
			return directionlist
		else:
			return directionlist
	else:
		return directionlist

def direction(request):
	directions = request.session['directions']
	splitted = directions.split('/')
	print splitted
	context = {'directions': splitted}
	return render(request, 'gotoplace.html', context)

def gotoplace(request):
	if request.method == 'POST':
		keyword = request.POST.get('keyword', '')
		where = request.POST.get('where')
		context = directionslistcomplete(keyword, where)
		arr = []
		for c in context:
			cd = c.encode('utf8')
			arr.append(cd)
		stri = '/'.join(arr)
		request.session['directions'] = stri
		return redirect('/directions')
	else:
		redirect('/preferences')
	return render_to_response('preferences.html',{},context_instance=RequestContext(request))



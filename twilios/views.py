# Create your views here.
# Okay.

from django.shortcuts import render_to_response, redirect, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from main.views import *
from django.shortcuts import render_to_response, redirect, render, get_object_or_404

from main.models import Directions
import re
from twilio import twiml

import subprocess

def science(request):
	msg = twiml.Response()
	msg.message("Science!")
	h = HttpResponse(str(msg), content_type="text/xml")
	return h

def science2(request):
	resp = twiml.Response()
	resp.message(str(request.GET['Body']))
	h = HttpResponse(str(resp), content_type="text/xml")
	return h

def whynot(request):
	body = request.GET['Body']
	sender = request.GET['From']

	num = Directions.objects.filter(phone=sender[1:]).count()
	if num is 0:
		user = Directions(phone=sender[1:])
		user.save()
		return _primary(body, sender[1:])
	else:
		user = Directions.objects.get(phone=sender[1:])
		grp = re.match(r'^(\d)$', body)
		if grp is not None:
			return _fourth(grp.group(0), sender, user)
		else:
			if user.location is unicode(''):
				user.location = body
				user.save()
				return _secondary(body, sender)
			else:
				user.directions = body
				user.save()
				return _tertiary(body, sender, user)
		

def _primary(text, sender):
	print "_primary"
	msg = twiml.Response()
	msg.message("Text where you are. (cross street 1, cross street 2, city)")
	h = HttpResponse(str(msg), content_type="text/xml")
	return h

#address recieved text options
def _secondary(text, sender):
	msg = twiml.Response()
	msg.message("Now Send Us Where You Want to Go in one word like \'Chinese food\'")
	h = HttpResponse(str(msg), content_type="text/xml")
	return h

def _tertiary(text, sender, user):
	msg = twiml.Response()
	msg.message = ("Text us the number you want to go to!\n")
	jsonstuff = gmaps(str(user.location))
	jsonstr = json.dumps(jsonstuff)
	if jsonstuff['status'] == 'OK':
		results = jsonstuff['results']
		mapping =results[0]
		location = mapping['geometry']
		latlong = location['location']
		latitude = latlong['lat']
		longitude = latlong['lng']

		placelist = places(latitude, longitude, str(user.directions))
		if placelist['status'] == 'OK':
			placelistsimple = placelisting(placelist['results'])
			for place in placelistsimple:
				_indmessage(place.name.encode('utf8'))
	h = HttpResponse(str(msg), content_type="text/xml")
	return h

def _indmessage(message):
	msg = twiml.Response()
	msg.message(message)
	h = HttpResponse(str(msg), content_type="text/xml")
	return h

#number recieved
def _fourth(text, sender, user):
	msg= twiml.Response()
	jsonstuff = gmaps(str(user.location))
	jsonstr = json.dumps(jsonstuff)
	if jsonstuff['status'] == 'OK':
		results = jsonstuff['results']
		mapping =results[0]
		location = mapping['geometry']
		latlong = location['location']
		latitude = latlong['lat']
		longitude = latlong['lng']

		placelist = places(latitude, longitude, str(user.directions))
		if placelist['status'] == 'OK':
			placelistsimple = placelisting(placelist['results'])
			directs = directionslistcomplete(str(placelistsimple[int(text)-1].name), str(user.location))
			for direct in directs:
				_indmessage(str(direct))
	user.delete()
	h = HttpResponse(str(msg), content_type="text/xml")

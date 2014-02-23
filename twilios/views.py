# Create your views here.
# Okay.

from django.shortcuts import render_to_response, redirect, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from main import views
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
	ls = subprocess.check_output('ls')
	ls = ls.split('\n')

	print ls
	num = Directions.objects.filter(phone=sender[1:]).count()
	if num is 0:
		user = Directions(phone=sender[1:])
		user.save()
		return _primary(body, sender[1:])
	else:
		user = Directions.objects.get(phone=sender[1:])
		grp = re.match(r'^(\d)$', body)
		if grp is not '':
			return _fourth(grp.group(0), sender, user)
		else:
			if user.location is '':
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
	msg.message = ("Now Send Us Where You Want to Go in one word like \'Chinese food\'")
	h = HttpResponse(str(msg), content_type="text/xml")
	return h

def _tertiary(text, sender, user):
	msg = twiml.Response()
	msg.message = ("Text us the number you want to go to!\n")
	jsonstuff = gmaps(user.location)
	jsonstr = json.dumps(jsonstuff)
	if jsonstuff['status'] == 'OK':
		results = jsonstuff['results']
		mapping =results[0]
		location = mapping['geometry']
		latlong = location['location']
		latitude = latlong['lat']
		longitude = latlong['lng']

		placelist = places(latitude, longitude, user.directions)
		if placelist['status'] == 'OK':
			placelistsimple = placelisting(placelist['results'])
			for place in placelistsimple:
				msg.message+=str(place)+'\n'
	h = HttpResponse(str(msg), content_type="text/xml")
	return h

#number recieved
def _fourth(text, sender, user):
	msg= twiml.Response()
	jsonstuff = gmaps(user.location)
	jsonstr = json.dumps(jsonstuff)
	if jsonstuff['status'] == 'OK':
		results = jsonstuff['results']
		mapping =results[0]
		location = mapping['geometry']
		latlong = location['location']
		latitude = latlong['lat']
		longitude = latlong['lng']

		placelist = places(latitude, longitude, user.directions)
		if placelist['status'] == 'OK':
			placelistsimple = placelisting(placelist['results'])
			directs = directionsto(latitude, longitude, placelistsimple[int(text)])
			for direct in directs:
				msg.message+=str(direct)+'\n'
	user.delete()g
	h = HttpResponse(str(msg), content_type="text/xml")

# Create your views here.
# Okay.

from django.shortcuts import render_to_response, redirect, render_to_response
from django.http import HttpResponseRedirect, HttpResponse

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

	if (sender[1:] + '.txt') in ls:
		return _secondary(body, sender[1:])
	else:
		return _primary(body, sender[1:])

def _primary(text, sender):
	with open(sender + '.txt', 'w') as nooooo:
		nooooo.write(text)
		print "_primary"
		msg = twiml.Response()
		msg.message("Ask a question of the Helix")
		h = HttpResponse(str(msg), content_type="text/xml")
		return h

def _secondary(text, sender):
	with open(sender + '.txt', 'r') as whyyy:
		s = whyyy.read()

		msg = twiml.Response()
		msg.message("The Helix says: " + _process_request(text) + 
			"\n\nAnd YOU says: "+s+"\nDonphan never forgets.")
		h = HttpResponse(str(msg), content_type="text/xml")
		print "_secondary"
		subprocess.call(['rm', sender + '.txt'])

		return h

def _process_request(text):
	if (text[0] >= "a" and text[0] < "g") or(text[0] >= "A" and text[0] < "G"):
	   return "No way, son."
	if (text[0] >= "g" and text[0] < "n") or(text[0] >= "G" and text[0] < "N"):
	   return "For science!"
	if (text[0] >= "n" and text[0] < "u") or(text[0] >= "N" and text[0] < "U"):
	   return "Try again later."
	if (text[0] >= "u" and text[0] < "z") or(text[0] >= "U" and text[0] < "Z"):
	   return "Most certainly."
	else: 
		return "NO U"

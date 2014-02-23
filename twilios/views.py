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
	ls = subprocess.check_output('ls').split('\n')

	if sender.lstrip("+") in ls:
		return _secondary(body, sender.lstrip("+"))
	else:
		return _primary(body, sender.lstrip("+"))

def _primary(text, sender):
	with open(sender + '.txt', 'w') as nooooo:
		nooooo.write(text)

		msg = twiml.Response()
		msg.message("Choose 1-5")
		h = HttpResponse(str(msg), content_type="text/xml")
		return h

def _secondary(text, sender):
	with open(sender + '.txt', 'r') as whyyy:
		s = whyyy.read()

		msg = twiml.Response()
		msg.message(text + ": " + s)
		h = HttpResponse(str(msg), content_type="text/xml")
		
		subprocess.call('rm', sender + '.txt')

		return h
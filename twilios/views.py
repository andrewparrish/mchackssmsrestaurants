# Create your views here.
# Okay.

from django.shortcuts import render_to_response, redirect, render_to_response
from django.http import HttpResponseRedirect, HttpResponse

from twilio import twiml

def science(request):
	msg = twiml.Response()
	msg.message("Science!")
	h = HttpResponse(str(msg), content_type="text/xml")
	return h

def science2(request, msg):
	resp = twiml.Response()
	resp.message(str(msg))
	h = HttpResponse(str(resp), content_type="text/xml")
	return h

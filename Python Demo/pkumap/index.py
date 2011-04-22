from django.http import HttpResponse
from django.template import Template
from django.shortcuts import render_to_response

def index(request):
	return render_to_response("mapview/index2.html")
	
def index2(request):
	return render_to_response("mapview/index2.html")

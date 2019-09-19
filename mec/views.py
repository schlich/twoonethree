from django.shortcuts import render
from django.views.generic.base import TemplateView

import mec.dash_apps

# Create your views here.
class MecIndex(TemplateView):
	
	template_name = "mec/index.html"
import math
from django.shortcuts import render
import re
import os
from pathlib import Path
from django.contrib import messages
from django.utils.timezone import datetime
from django.shortcuts import redirect
from noise_detection.forms import AudioAnalysisForm
from noise_detection_api.models import AudioAnalysis
from django.views.generic import ListView

# Create your views here.

class ResultListView(ListView):
    """Renders the history page, with a list of result of the analysis."""
    model = AudioAnalysis

    def get_context_data(self, **kwargs):
        context = super(ResultListView, self).get_context_data(**kwargs)
        return context

def about(request):
    return render(request, "noise_detection/about.html")

def home(request):
    return render(request, "noise_detection/home.html")
    
    

def result(request, record):
    return render(request, "noise_detection/result.html")
        
        
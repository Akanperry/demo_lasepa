from django import forms
from noise_detection_api.models import AudioAnalysis

class AudioAnalysisForm(forms.ModelForm):
    class Meta:
        model = AudioAnalysis
        fields = ("video_evidence",)   # NOTE: the trailing comma is required
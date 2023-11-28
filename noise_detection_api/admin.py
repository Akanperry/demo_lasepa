from django.contrib import admin
from noise_detection_api.models import AudioAnalysis

# Register your models here.
class AudioAnalysisAdmin(admin.ModelAdmin):
    pass

admin.site.register(AudioAnalysis, AudioAnalysisAdmin)

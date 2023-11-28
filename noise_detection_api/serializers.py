from rest_framework import serializers
from noise_detection_api.models import AudioAnalysis

class AudioAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioAnalysis
        fields = ["id", "title", "audio_file", "audio_file_size", "audio_file_duration", "audio_file_type", "noise_density", "category", "user_ip_address", "gps_location", "video_evidence", "mel_graph", "user", "log_date"]
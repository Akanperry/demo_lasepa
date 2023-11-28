from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from noise_detection_api.resource import validator as validate
from django.contrib.auth.models import User

# Create your models here.

class AudioAnalysis(models.Model):
    title = models.CharField(max_length=1000)
    audio_file = models.FileField(upload_to='audio_files/', validators=[validate.check_extension, validate.check_mime_type, validate.check_file_size], verbose_name="Select Audio FIle", blank=True)
    audio_file_size = models.FloatField(default=0.00)
    audio_file_duration = models.CharField(max_length=300, default="")
    audio_file_type = models.CharField(max_length=300, blank=True)
    noise_density = models.FloatField(default=0.00)
    category = models.CharField(max_length=300, blank=True)
    user_ip_address = models.GenericIPAddressField(protocol='both', unpack_ipv4=True, null=True)
    gps_location = models.TextField(blank=True)
    log_date = models.DateTimeField("date logged")
    mel_graph = models.FileField(upload_to='graph_files/', validators=[validate.check_image_extension, validate.check_file_size], verbose_name="Select Graph Image", blank=True)
    video_evidence = models.FileField(upload_to='video_files/', validators=[validate.check_video_extension, validate.check_file_size], verbose_name="Select Video FIle", error_messages={"required": "Please select an Video file for evidence"})
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)
    updated_at = models.DateTimeField("date logged", null=True)

    class Meta:
        verbose_name = "Analysis Record"
        verbose_name_plural = "Analysis Records"
        ordering = ["-log_date"]

    def __str__(self):
        """Returns a string representation of a message."""
        date = timezone.localtime(self.log_date)
        return f"'{self.title} - {date.strftime('%A, %d %B, %Y at %X')}"
import math, re, os
from pathlib import Path
from django.contrib import messages
from django.utils.timezone import datetime
from noise_detection_api.models import AudioAnalysis
from noise_detection_api.resource.audio_scrapper import AudioScrapper
from noise_detection_api.resource.location_detector import LocationDetector
from noise_detection_api.resource.detector_algorithm import NosieLevelAlgorithm as nla
from django.core.exceptions import RequestAborted

def classify_density(noise_density):
    noise_density = float(noise_density)
    if(noise_density<=40.00):
        category = "Faint"
    elif(noise_density>40.00 and noise_density<=60.00):
        category = "Moderate"
    elif(noise_density>60.00 and noise_density<=70.00):
        category = "Loud"
    elif(noise_density>70.00 and noise_density<=100.00):
        category = "Very Loud"
    elif(noise_density>100.00):
        category = "Extremely Loud"
    return category

def do_analysis(record_id, user_id):
    result = AudioAnalysis.objects.get(id=record_id)
    if result:
        file_path = result.video_evidence.path
        result.audio_file = AudioScrapper.scrape_audio(file_path)
        result.save()
        
        file_path = result.audio_file.path
        
        filesize = os.path.getsize(file_path)
        filesize = format(filesize/(1024*1024), ".2f")
        name, extension = os.path.splitext(file_path)
        duration = nla.get_duration_librosa(file_path)
        duration = str(math.floor(duration/60))+":"+str(int(duration%60))
        lat, lon, ip = LocationDetector.get_user_location()
        if lat is not None:
            location = LocationDetector.get_location(float(lat), float(lon))
            audio_noise_density = nla.calculate_noise_density(file_path)
            audio_noise_density = format(audio_noise_density, ".2f")
            audio_category = classify_density(audio_noise_density)

            result.audio_file_size = filesize
            result.audio_file_duration = duration
            result.audio_file_type = extension
            result.user_ip_address = ip
            result.gps_location = location
            result.noise_density = audio_noise_density
            result.category = audio_category
            result.updated_at = datetime.now()
            result.mel_graph = nla.plot_mel_spectogram(nla, file_path)

            result.save()

            return {
                'title': result.title,
                'audio_file': result.audio_file,
                'audio_file_size': filesize,
                'audio_file_duration': duration,
                'audio_file_type': extension,
                'noise_density': audio_noise_density,
                'category': audio_category,
                'user_ip_address': ip,
                'gps_location': location,
                'log_date': result.log_date,
                'video_evidence': result.video_evidence,
                'mel_graph': result.mel_graph,
                'user': user_id
            }
        else:
            raise RequestAborted("Unable to do analysis. Pleack your internet and try again.")
    else:
        raise RequestAborted("Unable to do analysis. Database activity failed.")
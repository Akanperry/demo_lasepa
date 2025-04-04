# Generated by Django 4.2.7 on 2023-11-28 12:08

from django.db import migrations, models
import noise_detection_api.resource.validator


class Migration(migrations.Migration):

    dependencies = [
        ('noise_detection_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='audioanalysis',
            options={'ordering': ['-log_date'], 'verbose_name': 'Analysis Record', 'verbose_name_plural': 'Analysis Records'},
        ),
        migrations.AlterField(
            model_name='audioanalysis',
            name='audio_file',
            field=models.FileField(blank=True, error_messages={'required': 'Please select an audio file to analyse'}, upload_to='audio_files/', validators=[noise_detection_api.resource.validator.check_extension, noise_detection_api.resource.validator.check_mime_type, noise_detection_api.resource.validator.check_file_size], verbose_name='Select Audio FIle'),
        ),
    ]

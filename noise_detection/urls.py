from django.urls import path
from noise_detection import views
from noise_detection_api.models import AudioAnalysis

result_list_view = views.ResultListView.as_view(
    queryset=AudioAnalysis.objects.order_by("log_date"),
    context_object_name="result_list",
    template_name="noise_detection/history.html",
)



urlpatterns = [
    path("", views.home, name="home"),
    path("result/", views.result, name='result'),
    path("history/", result_list_view, name="history"),
    path("about/", views.about, name="about"),
]
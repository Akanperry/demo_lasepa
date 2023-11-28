from django.urls import path
from rest_framework.schemas import get_schema_view
from .views import (
    RecordingsListView,
    CreateRecordingView,
    RecordingDetailView,
)

urlpatterns = [
    path('records/', RecordingsListView.as_view()),
    path('records/<int:record_id>', RecordingDetailView.as_view()),
    path('create-record/', CreateRecordingView.as_view()),

    # ...
    # Use the `get_schema_view()` helper to add a `SchemaView` to project URLs.
    #   * `title` and `description` parameters are passed to `SchemaGenerator`.
    #   * Provide view name for use with `reverse()`.
    path('', get_schema_view(
        title="Lasepa Demo API",
        description="API for all lasepa demo functionalities.",
        version="1.0.0"
    ), name='schemas'),
    # ...
]
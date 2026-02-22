from django.urls import path
from .views import WorkerSearchView

urlpatterns = [
    path('search/', WorkerSearchView.as_view(), name='worker-search'),
]
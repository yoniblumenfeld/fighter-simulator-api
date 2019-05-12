from django.urls import include,path
from . import views

urlpatterns = [
    path('simulate/',views.SimulatorAPIView.as_view())
]
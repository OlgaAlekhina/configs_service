from django.urls import path

from .views import GetConfigView, ConfigsView

urlpatterns = [
    path('configs/<str:config_type>/', GetConfigView.as_view(), name='get_config'),
    path('configs/', ConfigsView.as_view(), name='configs'),
]
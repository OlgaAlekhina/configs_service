from django.urls import path

from .views import ConfigTypeView, ConfigsView

urlpatterns = [
    path('configs/<str:config_type>/', ConfigTypeView.as_view(), name='get_config'),
    path('configs/', ConfigsView.as_view(), name='configs'),
]
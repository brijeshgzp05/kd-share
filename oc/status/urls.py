from django.conf.urls import url 
from .views import StatusView
from django.contrib.auth.decorators import login_required
# app_name = status

urlpatterns = [
	url(r'^status/$', login_required(StatusView.as_view()), name="status"),
]
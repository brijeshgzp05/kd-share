from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import ChatView, SaveView, UnseenView

urlpatterns = [
	url(r'^(?P<id>\d+)/$',ChatView, name="chat"),	
	url(r'^$',SaveView, name="save"),
	url(r'^messages$',login_required(UnseenView.as_view()), name="unseen"),
]

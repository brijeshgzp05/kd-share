from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import AddView, ReqView, DelReqView, AccReqView, FriendsView

urlpatterns = [
	url(r'^add/$', login_required(AddView.as_view()), name="add"),
	url(r'^view-requests/$', login_required(ReqView.as_view()), name="view"),
	url(r'^d/(?P<pk>\d+)/$', login_required(DelReqView.as_view()), name="del"),
	url(r'^a/(?P<pk>\d+)/$', login_required(AccReqView.as_view()), name="acc"),
	url(r'^$', login_required(FriendsView.as_view()), name="friends"),
]
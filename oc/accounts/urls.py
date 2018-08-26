from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import UnfriendView, RegisterFormView, LoginFormView, LogoutFormView, ChangePicView, VerifyCodeView, ProfileView, PseudoPro, OnlinePeopleView, ForgotPasswordView
# app_name = 'accounts'

urlpatterns = [

		url(r'^register/$', RegisterFormView.as_view(), name="register"),
		url(r'^login/$', LoginFormView.as_view(), name="login"),
		url(r'^logout/$', login_required(LogoutFormView.as_view()), name="logout"),
		url(r'^(?P<pk>\d+)/$', login_required(ProfileView.as_view()), name="profile"),
		url(r'^friends/(?P<username>[\w.@+-]+)/$', PseudoPro, name="pseudopro"),
		url(r'^chat/$', login_required(OnlinePeopleView.as_view()), name="online"),
		url(r'^security/email-checkup/$', ForgotPasswordView.as_view(), name="security"),
		url(r'^security/verify-code/$', VerifyCodeView.as_view(), name="code"),
		url(r'^unfriend/(?P<id>\d+)/$', UnfriendView, name="unfriend"),
		url(r'^change-profile-picture/$', login_required(ChangePicView.as_view()), name="change-profile-pic"),

]
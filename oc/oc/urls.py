from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^chats/', include('message.urls', namespace='message')),
    url(r'^friends/', include('friend.urls', namespace='friend')),
    url(r'^', include('home.urls', namespace='home')),
    url(r'^status/',include('status.urls', namespace="status")),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

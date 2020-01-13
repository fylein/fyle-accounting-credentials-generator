from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^connect/?$', views.connect, name='connect'),
    url(r'^validate_code/?$', views.validate_code, name='validate_code'),
    url(r'^send_email/?$', views.send_email, name='send_email'),
    url(r'^get_tokens/?$', views.get_tokens, name='get_tokens')
]

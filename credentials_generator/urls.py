from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^connect/?$', views.connect, name='connect'),
    url(r'^code_validator/?$', views.code_validator, name='code_validator'),
    url(r'^sendmail/?$', views.sendmail, name='sendmail'),
    url(r'^get_tokens/?$', views.get_tokens, name='get_tokens')
]

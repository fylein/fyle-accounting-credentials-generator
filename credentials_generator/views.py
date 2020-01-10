import json
import urllib

import requests
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.conf import settings

from django.core.mail import BadHeaderError, EmailMultiAlternatives
from django.http import HttpResponse

from credentials_generator.utilities import (
    getSecretKey,
    stringToBase64
)

accounting_system = ''


def index(request):
    """
    Home View
    """
    return render(request, 'index.html')


def connect(request):
    """
    create OAuth2 connection
    """
    global accounting_system
    accounting_system = request.POST.get('accounting_system', False)
    if accounting_system == 'qbo':
        CLIENT_ID = settings.QBO_CLIENT_ID
        SCOPES = settings.QBO_SCOPE
        url = settings.QBO_AUTH_ENDPOINT
        params = {'scope': SCOPES, 'redirect_uri': settings.REDIRECT_URI,
                  'response_type': 'code', 'state': get_CSRF_token(request), 'client_id': CLIENT_ID}
        url += '?' + urllib.parse.urlencode(params)
        return redirect(url)
    if accounting_system == 'xero':
        CLIENT_ID = settings.XERO_CLIENT_ID
        SCOPES = settings.XERO_SCOPE
        url = settings.XERO_AUTH_ENDPOINT
        params = {'scope': SCOPES, 'redirect_uri': settings.REDIRECT_URI,
                  'response_type': 'code', 'state': get_CSRF_token(request), 'client_id': CLIENT_ID}
        url += '?' + urllib.parse.urlencode(params)
        return redirect(url)


def code_validator(request):
    """
    Validate authorization code
    """
    state = request.GET.get('state', None)
    error = request.GET.get('error', None)
    if error == 'access_denied':
        return redirect('credentials_generator:index')
    if state is None:
        return HttpResponseBadRequest()
    elif state != get_CSRF_token(request):  # validate against CSRF attacks
        return HttpResponse('unauthorized, Make sure you have logged in to QuickBooks or Xero', status=401)
    auth_code = request.GET.get('code', None)
    client_id = request.GET.get('client_id', None)
    c = {
        'auth_code': auth_code,
        'client_id': client_id,
    }

    if auth_code is None:
        return HttpResponseBadRequest()

    else:
        return render(request, 'connected.html', context=c)


def get_tokens(request):
    """
    Get Tokens
    """
    if accounting_system == 'qbo':
        code = request.POST.get("auth_code", "")
        token_endpoint = 'https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer'
        CLIENT_ID = settings.QBO_CLIENT_ID
        CLIENT_SECRET = settings.QBO_CLIENT_SECRET
        auth_header = 'Basic ' + stringToBase64(CLIENT_ID + ':' + CLIENT_SECRET)
        headers = {'Accept': 'application/json', 'content-type': 'application/x-www-form-urlencoded',
                   'Authorization': auth_header}
        payload = {
            "grant_type": "authorization_code",
            "code": code,
            'redirect_uri': settings.REDIRECT_URI,
        }
        r = requests.post(token_endpoint, data=payload, headers=headers)
        json_data = json.loads(r.text)
        return render(request, 'tokens.html', context=json_data)

    if accounting_system == 'xero':
        code = request.POST.get("auth_code", "")
        token_endpoint = 'https://identity.xero.com/connect/token'
        CLIENT_ID = settings.XERO_CLIENT_ID
        CLIENT_SECRET = settings.XERO_CLIENT_SECRET
        auth_header = 'Basic ' + stringToBase64(CLIENT_ID + ':' + CLIENT_SECRET)
        headers = {'Accept': 'application/json', 'content-type': 'application/x-www-form-urlencoded',
                   'Authorization': auth_header}
        payload = {
            "grant_type": "authorization_code",
            "code": code,
            'redirect_uri': settings.REDIRECT_URI,
        }
        r = requests.post(token_endpoint, data=payload, headers=headers)
        json_data = json.loads(r.text)
        return render(request, 'tokens.html', context=json_data)


def sendmail(request):
    """
    Send Email
    """
    access_token = request.POST.get("access_token", "")
    refresh_token = request.POST.get("refresh_token", "")
    org_name = request.POST.get("org_name", "")
    from_email = 'sravan.kumar@fyle.in'
    to_email = ['n150264@rguktn.ac.in']
    subject = f"{accounting_system.upper()} OAuth2 Credentials Received from {org_name.upper()}"
    text_content = 'This is an important message.'
    html_content = '<b>' + org_name + '</b>' + '<p> OAuth2 credentials received' + '</p>' + '<b> RefreshToken : </b>' + '<p>' + refresh_token + '</p>' + '<br/>' + '<b> AccessToken : </b>' + '<p>' + access_token
    if subject and text_content and html_content and from_email:
        try:
            msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return render(request, 'success.html')
    else:
        return HttpResponse('Some unexpected error has occurred , please start the OAuth2 Flow again')


def get_CSRF_token(request):
    """
    Used to generate CSRF_token
    """
    token = request.session.get('csrfToken', None)
    if token is None:
        token = getSecretKey()
        request.session['csrfToken'] = token
    return token

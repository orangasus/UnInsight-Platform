from base64 import urlsafe_b64decode
from email.message import EmailMessage
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode
from django.shortcuts import redirect, get_object_or_404
from django.utils.encoding import force_str
from users.models import ExtendedUser
from django.contrib.auth.models import User
from .token_gen import token_generator
from .custom_responses import *

def check_login_status(request):
    value = request.session.get('user.id', 'default_value')
    if value == 'default_value':
        return False
    return True
    #insert this if in any needed function where the user must be logged in to access
    #if not check_login_status(request):
        #return Response(GET_SESSION_ERROR_RESPONSE("not logged in"), status=status.HTTP_401_UNAUTHORIZED)


def send_confirmation_email(request, ex_user):
    # domain = get_current_site(request).domain
    mail_subject = 'Account Activation'
    message = render_to_string('confirmation_template.html',
                               {
                                   "user": ex_user.user,
                                   "domain": 'uni.styro.dev',
                                   # char/digit -> byte representation (8bit for each char) -> encode64 (6bit for each char) (url-safe) representation
                                   "uid": generate_uidb64(ex_user.pk),
                                   "token": token_generator.make_token(ex_user)
                               })
    to_email = ex_user.user.email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()
    return HttpResponse('Confirmation email sent!')

def generate_uidb64(id):
    init_res = urlsafe_base64_encode(force_bytes(id))
    # check that res length is a multiple of 4
    res = init_res + '=' * ((4 - len(init_res) % 4) % 4)
    return res

def activate_account(request, uidb64, token):
    uid = force_str(urlsafe_b64decode(uidb64))
    ex_user = ExtendedUser.objects.get(pk=uid)

    if token_generator.check_token(ex_user, token):
        ex_user.user.is_active = True
        ex_user.user.save()
        return Response(ACCOUNT_ACTIVATED_RESPONSE("logged in"), status=status.HTTP_200_OK)
    else:
        return Response(ACTIVATION_FAILED_RESPONSE("not logged in"), status=status.HTTP_401_UNAUTHORIZED)
    
def send_password_reset_email(request, ex_user):
    mail_subject = 'Resetting Password'
    message = render_to_string('password_reset.html',
                               {
                                   "user": ex_user,
                                   "domain": 'uni.styro.dev',
                                   # char/digit -> byte representation (8bit for each char) -> encode64 (6bit for each char) (url-safe) representation
                                   "uid": generate_uidb64(ex_user.pk),
                                   "token": token_generator.make_token(ex_user)
                               })
    to_email = ex_user.user.email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()
    return HttpResponse('Password email sent!')

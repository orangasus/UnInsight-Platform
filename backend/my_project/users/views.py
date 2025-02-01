import logging
from base64 import urlsafe_b64decode
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User, Group
from django.db import IntegrityError
from django.http import HttpResponse
from django.utils.encoding import force_str
from django.http import JsonResponse
from emails.token_gen import token_generator
from emails.views import send_confirmation_email, send_password_reset_email
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .custom_responses import USER_DELETED_RESPONSE, USER_DELETED_ERROR, USER_UPDATE_ERROR, USER_NOT_FOUND_RESPONSE, \
    USER_LOGGED_IN_RESPONSE, AUTH_ERROR, \
    SERVER_ERROR_RESPONSE, USERNAME_TAKEN_RESPONSE, USER_SIGNUP_RESPONSE, USER_SIGNUP_ERROR, \
    RESET_PASSWORD_REQUEST_ERROR, RESET_PASSWORD_REQUEST_RESPONSE, RESET_PASSWORD_CHECK_TOKEN_RESPONSE, \
    RESET_PASSWORD_CHECK_TOKEN_ERROR, PASSWORD_CHANGED, PASSWORD_CHANGED_ERROR, LOGOUT_SUCCESS_RESPONSE, \
    LOGOUT_ERROR_RESPONSE, GET_SESSION_ERROR_RESPONSE,EMAIL_TAKEN_RESPONSE
from .custom_serializers import ExtendedUserSerializer
from .models import ExtendedUser

# Set up logging
logger = logging.getLogger(__name__)


def check_login_status(request):
    value = request.session.get('user.id', 'default_value')
    if value == 'default_value':
        return False
    return True
    # insert this if in any needed function where the user must be logged in to access
    # if not check_login_status(request):
    # return Response(GET_SESSION_ERROR_RESPONSE("not logged in"), status=status.HTTP_401_UNAUTHORIZED)
    # add this if needed in a class request = self.request


# Helper function to assign user to a group programmatically
def assign_user_to_group(username, group_name):
    try:
        user = User.objects.get(username=username)
        group = Group.objects.get(name=group_name)
        user.groups.add(group)
        logger.info(f"User {username} added to group {group_name}")
    except User.DoesNotExist:
        logger.error(f"User {username} does not exist")
    except Group.DoesNotExist:
        logger.error(f"Group {group_name} does not exist")


# Helper function to check if user is an admin
def is_admin(user):
    return user.is_staff or user.is_superuser


@api_view(['GET'])
def get_all_users(request):
    user = request.user
    if not is_admin(user):
      return Response(GET_SESSION_ERROR_RESPONSE("not logged in"), status=status.HTTP_401_UNAUTHORIZED)
    ex_users = ExtendedUser.objects.all()
    serializer = ExtendedUserSerializer(ex_users, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])

def delete_user_by_id(request, ex_user_id):
    user = request.user
    if not is_admin(user):
      return Response(GET_SESSION_ERROR_RESPONSE("not logged in"), status=status.HTTP_401_UNAUTHORIZED)
    try:
        user_to_delete = ExtendedUser.objects.get(id=ex_user_id)
        user_to_delete.delete()
        return Response(USER_DELETED_RESPONSE, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response(USER_DELETED_ERROR(e), status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def update_user_by_id(request, ex_user_id):
    user = request.user
    if not is_admin(user):
      return Response(GET_SESSION_ERROR_RESPONSE("not logged in"), status=status.HTTP_401_UNAUTHORIZED)
    try:
        user_to_update = ExtendedUser.objects.get(id=ex_user_id)
        serializer = ExtendedUserSerializer(user_to_update, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(USER_UPDATE_ERROR(e), status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_user_by_id(request, ex_user_id):
    user = request.user
    if not is_admin(user):
      return Response(GET_SESSION_ERROR_RESPONSE("not logged in"), status=status.HTTP_401_UNAUTHORIZED)
    try:
        user_to_get = ExtendedUser.objects.get(id=ex_user_id)
        serializer = ExtendedUserSerializer(user_to_get)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(USER_NOT_FOUND_RESPONSE(e), status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def login_user(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        ex_user = ExtendedUser.objects.get(user=user)
        if user:
            request.session["user.id"] = ex_user.id
            return Response(USER_LOGGED_IN_RESPONSE, status=status.HTTP_200_OK)
        return Response(AUTH_ERROR, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(SERVER_ERROR_RESPONSE(e), status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def signup_user(request):
    # Log the request data
    logger.debug(f"Request data: {request.data}")

    # Ensure request.data is a dictionary
    if not isinstance(request.data, dict):
        return Response({"detail": "Invalid data format"}, status=status.HTTP_400_BAD_REQUEST)

    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    # Check if the username is provided and not empty
    if not username or username.strip() == "":
        logger.error("Username is missing or empty")
        return Response({"status": "error", "message": "The given username must be set", "code": "USER_SIGNUP_ERROR"},
                        status=status.HTTP_400_BAD_REQUEST)

    if check_if_username_exists(username):
        return Response(USERNAME_TAKEN_RESPONSE, status=status.HTTP_400_BAD_REQUEST)

    # Uncomment this line if you want to check for email uniqueness
    if check_if_email_exists(email):
        return Response(EMAIL_TAKEN_RESPONSE, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.create_user(username=username, password=password, email=email)
        user.is_active = False
        user.save()
        ex_user = ExtendedUser.objects.create(user=user, public_username='npc')
        ex_user.save()
        ex_user.generate_public_name()
        send_confirmation_email(request._request, ex_user)
        return Response(USER_SIGNUP_RESPONSE, status=status.HTTP_201_CREATED)
    except IntegrityError:
        logger.error("Integrity error, possibly due to a duplicate entry")
        return Response({"detail": "Integrity error, possibly due to a duplicate entry"},
                        status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return Response(USER_SIGNUP_ERROR(e), status=status.HTTP_400_BAD_REQUEST)


def check_if_username_exists(username):
    return User.objects.filter(username=username).exists()


def check_if_email_exists(email):
    return User.objects.filter(email=email).exists()


@api_view(['GET'])
def reset_password_request(request):
    try:
        email = request.GET.get('email')
        print(email)
        user = User.objects.filter(email=email).first()
        ex_user = ExtendedUser.objects.get(user=user)
        send_password_reset_email(request, ex_user)
        return Response(RESET_PASSWORD_REQUEST_RESPONSE, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(RESET_PASSWORD_REQUEST_ERROR(e), status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_password_reset(request):
    try:
        uidb64 = request.data.get('uidb64')
        token = request.data.get('token')

        uid = force_str(urlsafe_b64decode(uidb64))
        ex_user = ExtendedUser.objects.get(pk=uid)

        if token_generator.check_token(ex_user, token):
            reset_user_password(request, uid)
            return Response(RESET_PASSWORD_CHECK_TOKEN_RESPONSE(True), status=status.HTTP_202_ACCEPTED)
        return Response(RESET_PASSWORD_CHECK_TOKEN_RESPONSE(False), status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(RESET_PASSWORD_CHECK_TOKEN_ERROR(e), status=status.HTTP_400_BAD_REQUEST)


def reset_user_password(request, ex_user_id):
    try:
        ex_user = ExtendedUser.objects.get(id=ex_user_id)
        new_password = request.data.get('new_password')
        ex_user.user.set_password(new_password)
        ex_user.save()
        return Response(PASSWORD_CHANGED, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(PASSWORD_CHANGED_ERROR(e), status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout_user(request):
    try:
        logout(request)
        delete_session(request)
        return Response(LOGOUT_SUCCESS_RESPONSE, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(LOGOUT_ERROR_RESPONSE(e), status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def set_session(request):
    user = request.user
    if not is_admin(user):
      return Response(GET_SESSION_ERROR_RESPONSE("not logged in"), status=status.HTTP_401_UNAUTHORIZED)
    request.session['key'] = 'value'
    return HttpResponse('Session data set')


@api_view(['GET'])
def get_session(request):
    value = request.session.get('user.id', 'default_value')
    if value == 'default_value':
        return JsonResponse({"code": 200, "message": "Invalid"})
    return JsonResponse({"code": 200, "message": "Valid", "session_data": value})

@api_view(['Delete'])
def delete_session(request):
    user = request.user
    if not is_admin(user):
      return Response(GET_SESSION_ERROR_RESPONSE("not logged in"), status=status.HTTP_401_UNAUTHORIZED)
    try:
        del request.session['user.id']
    except KeyError:
        pass
    return HttpResponse('Session data cleared')

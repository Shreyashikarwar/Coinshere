import sys
import os
from django.http import HttpResponse,JsonResponse
from rest_framework.authtoken.models import Token

from admin_user.models import *

def authenticate_token(view_func):
    def wrapper_func(request, *args, **kwargs):
        response = {}
        if 'Authorization' in request.headers and request.headers['Authorization'] != "" :
            api_token = request.headers['Authorization']
          
            if Token.objects.filter(key=api_token).exists():
                return view_func(request, *args, **kwargs)
            else:
                response['message'] = "Invalid Authorization token"
                
                return JsonResponse(response,status=401)  # when getting 401 status then user will logout or Invalid token
        else:
            response['message'] = "Authorization token is missing"
            return JsonResponse(response,status=404)
    return wrapper_func




def organization_authenticate_token(view_func):
    def wrapper_func(request, *args, **kwargs):
        response = {}
        if 'Authorization' in request.headers and request.headers['Authorization'] != "" :
            api_token = request.headers['Authorization']
          
            if OrganizationToken.objects.filter(token=api_token).exists():
                return view_func(request, *args, **kwargs)
            else:
                response['message'] = "Invalid Authorization token"
                
                return JsonResponse(response,status=401)  # when getting 401 status then user will logout or Invalid token
        else:
            response['message'] = "Authorization token is missing"
            return JsonResponse(response,status=404)
    return wrapper_func

    
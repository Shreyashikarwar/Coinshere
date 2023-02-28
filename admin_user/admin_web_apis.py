
from enum import unique
from multiprocessing import context
import profile
from urllib import response
from django.shortcuts import render
from genericpath import exists
import re
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated

from django.contrib.auth.models import User

from rest_framework.response import Response
from datetime import datetime,date
from utils.helpers import *

from django.conf import settings
from rest_framework.authtoken.models import Token
# Status and Response 
from rest_framework import status

from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED
)
from rest_framework.response import Response
# Models and Serializers Import Data
from .models import *
from line_manager_app.models import Team
from django.contrib.auth.hashers import make_password, check_password

from accounts.models import *

from .serializers import CompanySiteSerializers,LeaderShipTaskSerializers,LearningMaterialSerializers,OtherLinkSerializers,GameNameSerializers
from django.contrib.auth import logout
from decorators.decorators import *
from django.conf import settings

# Create Your Views Here 


# web view from terms & condition Section 

def term(request):
    template = "email/terms.html"
    context = {

    }
    return render(request, template , context)
# AUthentication  Section                             



# Login 
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def admin_login(request):
    email = request.data.get('email')
    password = request.data.get('password') 
    context = {}


    if email is None or email == '':
        return Response({'message': 'Email field is required', 'response_code':400}, status=HTTP_400_BAD_REQUEST)

    if password is None or password == '':
        return Response({'message': 'Password field is required', 'response_code':400}, status=HTTP_400_BAD_REQUEST)
    
    organization = Organiztaion.objects.filter(email=email).first()

    if not organization:
        return Response({'message': "Your email is not correct", 'response_code':400}, status=HTTP_400_BAD_REQUEST)

 
    if check_password(organization.password,password):
        return Response({'message': "You password is not correct", 'response_code': 400}, status=HTTP_400_BAD_REQUEST)
    
    if check_password(password,organization.password):

        token,_=OrganizationToken.objects.get_or_create(token=generate_token(),organization=organization)

        context['token']                  = token.token
        context['org_id']                 = organization.id 
        context['org_name']               = organization.organization_name
        context['unique_code_data']       = organization.unique_code
        context['mobile_number']          = organization.mobile_number
        context['email']                  = organization.email
        context['message']    = 'Login Successful '
        context['response_code'] = 200
        return Response(context, status=HTTP_200_OK)
    else:   
        context['message']    = 'You password is not correct'
        context['response_code'] = 400
        return Response(context, status=HTTP_400_BAD_REQUEST)
        

# Logout Section 
@csrf_exempt
@api_view(["POST"])
def admin_logout(request):
    if request.data.get('org_id') == '' or request.data.get('org_id') is None:  
        return Response({'message': 'Please provide a org_id', 'response_code': 400}, status=HTTP_400_BAD_REQUEST) 
    
    org_id = request.data.get('org_id')
    user_instance = OrganizationToken.objects.filter(organization__id=org_id)
    context = {}

    if user_instance:
        user_instance.delete()
        context['message']       = (f" User Logged Out successfully for user id {org_id}.")
        context['response']      = 200
        return Response(context,status.HTTP_200_OK)
    else:
        context['message']       = (f" { org_id } is Invalid  User Id.")
        context['response']      = 400
        return Response(context,status.HTTP_400_BAD_REQUEST)


#Get ALl Data from Organization 
@csrf_exempt
@api_view(['GET'])
def organization_employee_data_list(request):

    if request.data.get('org_id') == '' or request.data.get('org_id') is None:  
        return Response({'message': 'Please provide a org_id', 'response_code': 400}, status=HTTP_400_BAD_REQUEST) 
    
    org_id = request.data.get('org_id')

    user_instance = OrganizationToken.objects.filter(organization__id=org_id).first()


    unique_code=request.data.get('unique_code')
    context ={}
    if unique_code:
        organization_employee_data=UserProfile.objects.filter(unique_code=unique_code).values()
        if organization_employee_data:
            context['organization_employee_data']  = organization_employee_data
            context['message']                     = f"Employee Data Successfully Geting for unique_code {unique_code}"
            context['resposne_code']               =  200
            return Response(context,status=status.HTTP_200_OK)
        else:
            context['message']                     =  f"Data Not Get for unique_code  {unique_code}"
            context['resposne_code']               =  400
            return Response(context,status=status.HTTP_400_BAD_REQUEST)
    else:
        context['message']                     = 'Please Provide unique_code in Params '
        context['resposne_code']               =  400
        return Response(context,status=status.HTTP_400_BAD_REQUEST)


# Get All Employee Data With Filter
@csrf_exempt
@api_view(['POST'])
def employee_data_list_baselocation(request):
    unique_code=request.data.get('unique_code')
    if unique_code == '' or unique_code is  None:  
        return Response({'message': 'Please provide a valid Unique_code ', 'response_code':400},status=status.HTTP_400_BAD_REQUEST) 

    base_location        =  request.data.get('base_location')
    team_id              =  request.data.get('team_id')
    pending_for_approval =  request.data.get('pending_for_approval') # 0
    existing_active      =  request.data.get('existing_active')   # 1
    employee_data=UserProfile.objects.filter(unique_code=unique_code)
    context ={}
    if base_location:
        employee_data = employee_data.filter(base_location=base_location)
    if team_id:
        employee_data = employee_data.filter(team_id=team_id)
    if pending_for_approval:
        employee_data = employee_data.filter(is_verified_by_admin=pending_for_approval)
    if existing_active:
        employee_data = employee_data.filter(is_verified_by_admin=existing_active)
    employees = []
    for employee in employee_data:
        data = {}
        data['first_name']         = employee.user.first_name
        data['last_name']          = employee.user.last_name
        data['organization_code']  = employee.organization_code
        data['mobile_no']          = employee.mobile_no
        data['email']              = employee.user.email
        data['team_name']          = Team.objects.values_list('team_name',flat=True).filter(id=employee.team_id).first() 
        data['date_of_action']     = employee.created_at
        employees.append(data)
    context['employee_data']  = employees
    context['message']        = f"Data received successfully"
    context['resposne_code']  =  200
    return Response(context,status=status.HTTP_200_OK)
            


# City List Data
@csrf_exempt
@api_view(['GET'])
def employee_city_list(request):
    organization_city_data=OrganizationCity.objects.all().values()
    context={}
    if organization_city_data:
        context['organization_city_data']  = organization_city_data
        context['response_code']           = 200
        context['message']                 = 'Employee City Data List'
        return Response(context,status=status.HTTP_200_OK)
    else:
        context['response_code']           = 400
        context['message']                 = 'Data Not Found'
        return Response(context,status=status.HTTP_400_BAD_REQUEST)

  



# Team List Data 
@csrf_exempt
@api_view(['GET'])
def team_list_data(request):
    org_id_data=request.query_params.get('org_id')
    
    if org_id_data == '' or org_id_data is  None:  
        return Response({'message': 'Please provide a valid org_id_data ', 'response_code':400},status=status.HTTP_400_BAD_REQUEST) 
    team_list_data=Team.objects.filter(organization__id=org_id_data).values()

    context = {}
    if team_list_data:
        context['team_list_data'] = team_list_data
        context['message']        = f"Data get Successfully for {org_id_data}"
        context['response_code']  = 200
        return Response(context,status=status.HTTP_200_OK)
    else:
        context['message']        = f"Data not Get for {org_id_data}"
        context['response_code']  = 400
        return Response(context,status=status.HTTP_400_BAD_REQUEST)
        




# How to Create or sent Data on Two Diffrent  Model on Same Model 
@csrf_exempt
@api_view(["POST"])
# @permission_classes((AllowAny,))
def organization_employee(request):
    context = {}    

    
    # Get Role Id Data
    role_id=request.data.get('role_id')
    # Get First Name
    first_name=request.data.get('first_name')

    # Last name
    last_name=request.data.get('last_name')
    # New Password
    new_password=request.data.get('new_password')
    # Confirm Password
    confirm_password=request.data.get('confirm_password')
    # Unique Code
    unique_code=request.data.get('unique_code')
    # email
    email_data=request.data.get('email')
    # Mobile Number
    mobile=request.data.get('mobile')
    # Base Location 
    location=request.data.get('location')
    # Organization Name
    organization_name=request.data.get('organization_name')

    designation=request.data.get('designation')
    team_id=request.data.get('team_id')




    if role_id =='' or role_id is  None:
        return Response({'message':'Please Provide a Valid role_id','response_code':400},status=status.HTTP_400_BAD_REQUEST)
    if first_name=='' or first_name is None:
        return Response({'message':'Please Provoide first_name','response_code':400},status=status.HTTP_400_BAD_REQUEST) 
    if last_name =='' or last_name is None:
        return Response({'message':'Please Provide last_name','response_code':400},status=status.HTTP_400_BAD_REQUEST)
    if new_password=='' or new_password is None:
        return Response({'message':'Please Provide new_password','response_code':400},status=status.HTTP_400_BAD_REQUEST)
    if confirm_password =='' or confirm_password is None:
        return Response({'message':'Please Provide confirm_password','response_code':400},status=status.HTTP_400_BAD_REQUEST)

    # matching Password Data          --------------------    
    if confirm_password != new_password:
        return Response({'message':'New Password and Old Password not Matched','response_code':400},status=status.HTTP_400_BAD_REQUEST)
        
    if unique_code =='' or unique_code is None:
        return Response({'message':'Please Provide unique_code','response_code':400},status=status.HTTP_400_BAD_REQUEST)
    # Unique Code Check from user      --------------------
    if not Organiztaion.objects.filter(unique_code=unique_code).exists():
        return Response({'message':'Please Provide a valid unique Code','response_code':400},status=status.HTTP_400_BAD_REQUEST)


    if email_data == ' ' or email_data is None:
        return Response({'messsage':'Please Provide email','response_code':400},status=status.HTTP_400_BAD_REQUEST)
    # Email Validation Check form user  --------------------
    if User.objects.filter(email=email_data).exists():
        return Response({'message':'Email is already exists','response_code':400},status=status.HTTP_400_BAD_REQUEST)


    if mobile == ' ' or mobile is None:
        return Response({'message':'Please Provide Mobile no','response_code':400},status=status.HTTP_400_BAD_REQUEST)
    # Mobile No Check Validation ---------------------------
    if UserProfile.objects.filter(mobile_no=mobile).exists():
        return Response({'message':'Mobile Number already exists','response_code':400},status=status.HTTP_400_BAD_REQUEST)

    if location =='' or location is None:
        return Response({'message':'Please Provide Location','response_coed':400},status=status.HTTP_400_BAD_REQUEST)

    if organization_name =='' or organization_name is None:
        return Response({'message':'Please provide Organozation Name','response_code':400},status=status.HTTP_400_BAD_REQUEST)
    org_obj = Organiztaion.objects.filter(unique_code=request.data.get("unique_code")).first()

    if designation =='' or designation is None:
            return Response({'message':'Please provide designation Name','response_code':400},status=status.HTTP_400_BAD_REQUEST)
        
    if team_id =='' or team_id is None:
            return Response({'message':'Please provide team_id ','response_code':400},status=status.HTTP_400_BAD_REQUEST)
        


    user = User.objects.create(username=generate_random_number(),first_name=first_name,
    last_name=last_name,email=email_data,password=  make_password(request.data.get("new_password")))
    role = Role.objects.filter(id=role_id).first()
    if user:
        user_profile = UserProfile.objects.create(base_location=org_obj.address,company_name=org_obj.organization_name,organization_code=org_obj.organization_code,user=user,mobile_no=mobile,unique_code=unique_code,role=role,designation=designation,team_id=team_id)
        user_profile.member_since = user_profile.created_at
        user_profile.save()

    context['message']                  = f"Employee succesfully Created for {organization_name}"
    context['response_code']            = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)
 



# ##############################################



# # How to Create or sent Data on Two Diffrent  Model on Same Model 
# @csrf_exempt
# @api_view(["POST"])
# @organization_authenticate_token
# # @permission_classes((AllowAny,))
# def admin_signup(request):
    
#     # Get Role Id Data
#     role_id=request.data.get('role_id')
#     # Get First Name
#     first_name=request.data.get('first_name')
#     # Last name
#     last_name=request.data.get('last_name')
#     # New Password
#     new_password=request.data.get('new_password')
#     # Confirm Password
#     confirm_password=request.data.get('confirm_password')
#     # Unique Code
#     unique_code=request.data.get('unique_code')
#     # email
#     # Mobile Number
#     mobile=request.data.get('mobile')
#     # Base Location 
#     location=request.data.get('location')
#     # Organization Name
#     organization_name=request.data.get('organization_name')
#     email=request.data.get('email')


#     if role_id =='' or role_id is  None:
#         return Response({'message':'Please Provide a Valid role_id','response_code':400},status=status.HTTP_400_BAD_REQUEST)
#     if first_name=='' or first_name is None:
#         return Response({'message':'Please Provoide first_name','response_code':400},status=status.HTTP_400_BAD_REQUEST) 
#     if last_name =='' or last_name is None:
#         return Response({'message':'Please Provide last_name','response_code':400},status=status.HTTP_400_BAD_REQUEST)
#     if new_password=='' or new_password is None:
#         return Response({'message':'Please Provide new_password','response_code':400},status=status.HTTP_400_BAD_REQUEST)
#     if confirm_password =='' or confirm_password is None:
#         return Response({'message':'Please Provide confirm_password','response_code':400},status=status.HTTP_400_BAD_REQUEST)

#     # matching Password Data          --------------------    
#     if confirm_password != new_password:
#         return Response({'message':'New Password and Confirm Password not Matched','response_code':400},status=status.HTTP_400_BAD_REQUEST)
        
#     if unique_code =='' or unique_code is None:
#         return Response({'message':'Please Provide unique_code','response_code':400},status=status.HTTP_400_BAD_REQUEST)
#     # Unique Code Check from user      --------------------
#     if not Organiztaion.objects.filter(unique_code=unique_code).exists():
#         return Response({'message':'Please Provide a valid unique Code','response_code':400},status=status.HTTP_400_BAD_REQUEST)


#     if email == ' ' or email is None:
#         return Response({'messsage':'Please Provide email','response_code':400},status=status.HTTP_400_BAD_REQUEST)
#     # Email Validation Check form user  --------------------
#     if User.objects.filter(email=email).exists():
#         return Response({'message':'Email is already exists','response_code':400},status=status.HTTP_400_BAD_REQUEST)

#     if mobile == ' ' or mobile is None:
#         return Response({'message':'Please Provide Mobile no','response_code':400},status=status.HTTP_400_BAD_REQUEST)
#     # Mobile No Check Validation ---------------------------
#     if UserProfile.objects.filter(mobile_no=mobile).exists():
#         return Response({'message':'Mobile Number already exists','response_code':400},status=status.HTTP_400_BAD_REQUEST)

#     if location =='' or location is None:
#         return Response({'message':'Please Provide Location','response_coed':400},status=status.HTTP_400_BAD_REQUEST)

#     if organization_name =='' or organization_name is None:
#         return Response({'message':'Please provide Organization Name','response_code':400},status=status.HTTP_400_BAD_REQUEST)
#     org_obj = Organiztaion.objects.filter(unique_code=request.data.get("unique_code")).first()

#     print(org_obj.address)
#     print(org_obj.organization_name)
#     print(org_obj.organization_code)
#     print(mobile)
#     print(unique_code)

# #     if int(role_id) == 1:
# #         # Customer 
# #         user = User.objects.create(username=generate_random_number(),first_name=first_name,
# #             last_name=last_name,email=email,password=  make_password(request.data.get("new_password")))
# #         role = Role.objects.filter(id=role_id).first()
# #         if user:
# #             user_profile = UserProfile.objects.create(base_location=org_obj.address,company_name=org_obj.organization_name,organization_code=org_obj.organization_code,user=user,mobile_no=request.data.get('mobile_no'),unique_code=request.data.get('unique_code'),role=role)
# #             user_profile.member_since = user_profile.created_at
# #             user_profile.save()
# #     else:
# #         # Manager
# #         user = User.objects.create(username=generate_random_number(),first_name=request.data.get('first_name'),
# #             last_name=request.data.get('last_name'),email=request.data.get('email'),password=make_password(request.data.get("new_password")))
# #         role = Role.objects.filter(id=role_id).first()
# #         if user:
# #             user_profile = UserProfile.objects.create(base_location=org_obj.address,company_name=org_obj.organization_name,organization_code=org_obj.organization_code,user=user,mobile_no=request.data.get('mobile_no'),unique_code=request.data.get('unique_code'),role=role)
# #             user_profile.member_since = user_profile.created_at
# #             user_profile.save()


#     context = {}    
#     context['message']                  = ""
#     context['response_code']            = HTTP_200_OK
#     return Response(context, status=HTTP_200_OK)
 




# Manager Concern Section 
@csrf_exempt
@api_view(["POST"])
@organization_authenticate_token
def manage_concern_list(request):
    unique_code=request.data.get('unique_code')
    if unique_code ==' ' or unique_code is None:
        return Response({'message':'Please Provide unique_code','response_code':400},status=status.HTTP_400_BAD_REQUEST)
    
    if not Organiztaion.objects.filter(unique_code=unique_code).exists():
        return Response({'message':'Please Provide a valid unique Code','response_code':400},status=status.HTTP_400_BAD_REQUEST)

    concern_data_list=[]

    # get customer & manager raise concern data with filter with unique code
    customer_concern_list=CustomerRaiseConcern.objects.filter(user_profile__unique_code=unique_code)
    manager_concern_list=ManagerRaiseConcern.objects.filter(user_profile__unique_code=unique_code)

    
    #looping customer & manager section
    for customer_concern in customer_concern_list:
        data = {}
        data['ticket_id']       = 'ticket#'+str(customer_concern.id)
        data['email']           = customer_concern.user_profile.user.email
        data['comment']         = customer_concern.comment
        data['team']            = Team.objects.filter(id=customer_concern.user_profile.team_id).values_list('team_name', flat=True)[0] 
        data['manager']         = Manager.objects.filter(id=customer_concern.user_profile.manager_id).values_list('manager_name', flat=True)[0] 
        data['location']        = customer_concern.user_profile.base_location
        data['status']          = customer_concern.status
        data['concern_type']    = customer_concern.concern_category.name
        
        if User.objects.filter(id=customer_concern.action_owner_id).exists(): 
           user_obj= User.objects.get(id=customer_concern.action_owner_id)
           action_owner_name = user_obj.first_name +" "+user_obj.last_name 
        else:  
           org_obj= Organiztaion.objects.get(id=customer_concern.action_owner_id)
           action_owner_name = org_obj.organization_name

        data['action_owner_name'] = action_owner_name
        concern_data_list.append(data)


    for manager_concern in manager_concern_list:
        data = {}
        data['ticket_id']       = 'ticket#'+str(manager_concern.id)
        data['email']           = manager_concern.user_profile.user.email
        data['comment']         = manager_concern.comment
        data['team']            = Team.objects.filter(id=manager_concern.user_profile.team_id).values_list('team_name', flat=True)[0] 
        data['location']        = manager_concern.user_profile.base_location
        data['manager']         = '----' 
        data['status']          = manager_concern.status
        data['concern_type']    = manager_concern.concern_category.name

        if User.objects.filter(id=manager_concern.action_owner_id).exists(): 
           user_obj= User.objects.get(id=manager_concern.action_owner_id)
           action_owner_name = user_obj.first_name +" "+user_obj.last_name 
        else:  
           org_obj= Organiztaion.objects.get(id=manager_concern.action_owner_id)
           action_owner_name = org_obj.organization_name
           data['action_owner_name'] = action_owner_name

        concern_data_list.append(data)
    context = {}    
    context['message']                  = f"succcesfully geting data from unique code {unique_code}"
    context['response_code']            = HTTP_200_OK
    context['concern_list_data']    = concern_data_list
    
    return Response(context, status=HTTP_200_OK)
 



# User Profile List Section 
@csrf_exempt
@api_view(["POST"])
@organization_authenticate_token
def user_profile_list(request):

    unique_code=request.data.get('unique_code')
    if unique_code == ' ' or unique_code is None:
        return Response({'message':'Please Provide unique_code','response_code':400},status=status.HTTP_400_BAD_REQUEST)
    
    if not Organiztaion.objects.filter(unique_code=unique_code).exists():
        return Response({'message':'Please Provide a valid unique Code','response_code':400},status=status.HTTP_400_BAD_REQUEST)

    # Create List 
    user_profile_list_data=[]

    # Get User & User Profile Data
    user_profile_list=UserProfile.objects.filter(unique_code=unique_code)

    #Create For Loop
    for user_profile in  user_profile_list:

        # Crteate empty dict
        data={}
        data['first_name'] =  user_profile.user.first_name   
        data['last_name']  =  user_profile.user.last_name
        data['org_code']   =  user_profile.organization_code
        data['mobile']     =  user_profile.mobile_no
        data['email']      =  user_profile.user.email
        data['active']     =  user_profile.is_active
        data['team']       =  Team.objects.values_list('team_name', flat=True).filter(id=user_profile.team_id).first()
        data['manager']    =  Manager.objects.values_list('manager_name', flat=True).filter(id=user_profile.manager_id).first()
        data['location']   =  user_profile.base_location
        data['date']       =  user_profile.created_at.date()
        user_profile_list_data.append(data)        

    context={}
    context['message']                  = f"succcesfully geting data from unique code {unique_code}"
    context['user_profile_list']   = user_profile_list_data
    context['response_code']       = 200
    return Response(context)


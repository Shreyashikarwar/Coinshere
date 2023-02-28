from asyncio import tasks
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from django.contrib.auth.models import User
from uritemplate import partial
from .models import *
from django.contrib.auth.hashers import make_password, check_password

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from utils.helpers import *
from rest_framework.authtoken.models import Token



from rest_framework import serializers, status
from rest_framework.response import Response 

from decorators.decorators import *
from admin_user.models import *
from utils.helpers import *

#Import  Serializers
from .models import UserProfile
from .serializers import UserProfileListSerializer,UserProfileUpdateSerializer

from line_manager_app.models import *

from datetime import datetime
from django.conf import settings

from django.template.loader import render_to_string

from django.core.mail import EmailMultiAlternatives


# Create your views here.



@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def signup(request):
    role_id         = request.data.get('role_id')
    # organization_id = request.data.get('organization_id')

   
    if request.data.get("first_name") == '' or request.data.get("first_name") is None:
        return Response({'message': 'Please provide first name', 'response_code':201}, status=HTTP_200_OK)     

    if request.data.get("last_name") == '' or request.data.get("last_name") is None:
        return Response({'message': 'Please provide last name', 'response_code': 201}, status=HTTP_200_OK)     

    if request.data.get("new_password") is None or request.data.get("new_password") is None:
        return Response({'message': 'Please provide new password', 'response_code':201}, status=HTTP_200_OK)
    # newpas=request.data.get("new_password")
    # confirm_pass=request.data.get("confirm_password")

    if request.data.get("confirm_password") == '' or request.data.get("confirm_password") is None:  
        return Response({'message': 'Please provide confirm password', 'response_code':201}, status=HTTP_200_OK) 

    if request.data.get("confirm_password") != request.data.get("new_password"):  
        return Response({'message': 'New password and confirm password did not match.', 'response_code':201}, status=HTTP_200_OK) 


    if request.data.get("unique_code") == '' or request.data.get("unique_code") is None:  
        return Response({'message': 'Please provide unique code', 'response_code':201}, status=HTTP_200_OK) 

    if request.data.get("email") == '' or request.data.get("email") is None:   
        return Response({'message': 'Please provide email', 'response_code': 201}, status=HTTP_200_OK) 

    if request.data.get("mobile_no") == '' or request.data.get("mobile_no") is None:   
        return Response({'message': 'Please provide mobile_no', 'response_code':201}, status=HTTP_200_OK) 


    if User.objects.filter(email=request.data.get('email')).exists():
        return Response({'message': 'Email is already exists', 'response_code':201}, status=HTTP_200_OK) 

    if UserProfile.objects.filter(mobile_no=request.data.get('mobile_no')).exists():
        return Response({'message': 'Mobile no is already exists', 'response_code':201}, status=HTTP_200_OK) 
     
    if not Organiztaion.objects.filter(unique_code=request.data.get("unique_code")).exists():
        return Response({'message': 'Please provide valid unique code', 'response_code':201}, status=HTTP_200_OK) 

    organization_employee = OrganizationEmployeeData.objects.filter(organization__unique_code=request.data.get("unique_code"),email=request.data.get("email")).first()

    if not organization_employee:
        return Response({'message': 'You are not an employee in any organization', 'response_code':201}, status=HTTP_200_OK) 

    if request.data.get("firebase_token") == '' or request.data.get("firebase_token") is None:
        return Response({'message': 'Please provide firebase token field', 'response_code':201}, status=HTTP_200_OK) 


    firebase_token =request.data.get('firebase_token')



    org_obj = Organiztaion.objects.filter(unique_code=request.data.get("unique_code")).first()

 
    if int(role_id) == 1:
        # Customer 
        user = User.objects.create(username=generate_random_number(),first_name=request.data.get('first_name'),
            last_name=request.data.get('last_name'),email=request.data.get('email'),password=make_password(request.data.get("new_password")))
              
        role = Role.objects.filter(id=role_id).first()
        
        if user:
            user_profile = UserProfile.objects.create(base_location=org_obj.address,company_name=org_obj.organization_name,organization_code=org_obj.organization_code,user=user,mobile_no=request.data.get('mobile_no'),unique_code=request.data.get('unique_code'),role=role,team_id=organization_employee.team.id,manager_id=organization_employee.manager.id,gender=organization_employee.gender,default_language=organization_employee.language,designation=organization_employee.designation)
            user_profile.member_since = user_profile.created_at
            user_profile.save()

            userFirebaseToken = firebase_token

            message_title = "Your profile has been created"
            message_body = "Your Profile is under company admin review and for verificationn then you can login"
            notification_image = ""

            if userFirebaseToken is not None and userFirebaseToken != "" :
                registration_ids = []
                registration_ids.append(userFirebaseToken)
                data_message = {}
                data_message['id'] = 1
                data_message['status'] = 'notification'
                data_message['click_action'] = 'login_page'

                data_message['image'] = notification_image

                send_android_notification(message_title,message_body,data_message,registration_ids)
                
                heading="Your profile has been created successfully"

                notification_msg="Your Profile is under company admin review and for verification then you can login"

                save_notification(user_profile.manager_id,user_profile.id,heading,notification_msg)

    else:
        # Manager
        user = User.objects.create(username=generate_random_number(),first_name=request.data.get('first_name'),
            last_name=request.data.get('last_name'),email=request.data.get('email'),password=make_password(request.data.get("new_password")))
        
        role = Role.objects.filter(id=role_id).first()

        if user:
            user_profile = UserProfile.objects.create(base_location=org_obj.address,company_name=org_obj.organization_name,organization_code=org_obj.organization_code,user=user,mobile_no=request.data.get('mobile_no'),unique_code=request.data.get('unique_code'),role=role,team_id=organization_employee.team.id,manager_id=organization_employee.manager.id,gender=organization_employee.gender,default_language=organization_employee.language,designation=organization_employee.designation)
            user_profile.member_since = user_profile.created_at
            user_profile.save()

            userFirebaseToken = firebase_token

            message_title = "Your profile has been created"
            message_body = "Your Profile is under company admin review and for verificationn then you can login"
            notification_image = ""

            if userFirebaseToken is not None and userFirebaseToken != "" :
                registration_ids = []
                registration_ids.append(userFirebaseToken)
                data_message = {}
                data_message['id'] = 1
                data_message['status'] = 'notification'
                data_message['click_action'] = 'login_page'

                data_message['image'] = notification_image

                send_android_notification(message_title,message_body,data_message,registration_ids)
                
                heading="Your profile has been created succcessfully"

                notification_msg="Your Profile is under company admin review and for verification then you can login"

                save_notification(user_profile.id,user_profile.id,heading,notification_msg)

    context = {}    
    context['message']                  = "User profile has been created successfully"
    context['response_code']            = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)



@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    role_id         = request.data.get('role_id')

    if request.data.get("email") == '' or request.data.get("email") is None:  
        return Response({'message': 'Please provide email', 'response_code':201}, status=HTTP_200_OK) 
    
    if request.data.get("password") == '' or request.data.get("password") is None:
        return Response({'message': 'Please provide password', 'response_code':201}, status=HTTP_200_OK)     
    
    user_profile=UserProfile.objects.filter(user__email=request.data.get('email')).first()
    
    if not user_profile:
        return Response({'message': 'Email is not exists', 'response_code': 201}, status=HTTP_200_OK) 

    user_profile=UserProfile.objects.filter(user__email=request.data.get('email'),is_verified_by_admin=True).first()
    

    if not user_profile:
        return Response({'message': 'Your profile is not verified by the Admin.Kindly wait after some time.', 'response_code':201}, status=HTTP_200_OK) 

    user_profile_role=UserProfile.objects.filter(user__email=request.data.get('email'),is_verified_by_admin=True).first()
    

    if role_id!=user_profile_role.role.id:
        return Response({'message': 'You are not authorized with this role.', 'response_code':201}, status=HTTP_200_OK) 


    # if request.data.get("firebase_token") == '' or request.data.get("firebase_token") is None:
    #     return Response({'message': 'Please provide firebase token field', 'response_code':201}, status=HTTP_200_OK) 

    # if request.data.get("device_id") == '' or request.data.get("device_id") is None:
    #     return Response({'message': 'Please provide device id', 'response_code':201}, status=HTTP_200_OK) 


    firebase_token =request.data.get('firebase_token')
    
    # body = "Awesome!You are connected with Twilio"

    # to_mobile_no = request.data.get('to_mobile_no') 
    
    # print("to mobile no===>",to_mobile_no)

    # broadcast_message_on_whatsapp(body,to_mobile_no)
    
    if check_password(request.data.get("password"), user_profile.user.password):
        user_profile=user_profile

        if request.data.get("device_id") != '' or request.data.get("device_id") is not None:
            user_profile.device_id = request.data.get("device_id")
            user_profile.save()
        
      
        current_date = datetime.now().date()


        if not user_profile.is_signup:
        
            user_activity_count = ActivityLog.objects.filter(user_id=user_profile.id,module="Login",sub_module="Login",created_at__icontains=current_date).count()
            
        
            if not user_activity_count:
               
                points = RewardPointsStimulator.objects.filter(status=4).first()

                if MyRewardPoint.objects.filter(user_profile__id=user_profile.id).exists():
                    my_reward = MyRewardPoint.objects.filter(user_profile__id=user_profile.id).last()

                    point_balance = my_reward.point_balance + int(points.multiplier)

                    my_reward = MyRewardPoint.objects.create(
                        manager_id=0,              
                        user_profile=user_profile,
                        earned_point=int(points.multiplier),
                        point_balance=point_balance
                    )
                else:
                    my_reward = MyRewardPoint.objects.create(
                        manager_id=0,              
                        user_profile=user_profile,
                        earned_point=int(points.multiplier),
                        point_balance=int(points.multiplier)
                    )    
        

        if user_profile.is_signup == 1:
 
            user_profile.is_signup = 0
            user_profile.save()

            points = RewardPointsStimulator.objects.filter(status=1).first()

            my_reward = MyRewardPoint.objects.create(
                manager_id=0,              
                user_profile=user_profile,
                earned_point=int(points.multiplier),
                point_balance=int(points.multiplier)
            )
        
        user_profile.is_active = 1
        user_profile.save()
    else:
        return Response({'message': 'Invalid Credentials', 'response_code':201}, status=HTTP_200_OK)
    
    data = {}
    

    if role_id==1:
        if role_id==user_profile.role.id:

            data['id']                      =   user_profile.id
            data['unique_code']             =   user_profile.unique_code
            data['first_name']              =   user_profile.user.first_name
            data['last_name']               =   user_profile.user.last_name
            data['email']                   =   user_profile.user.email
            data['mobile_no']               =   user_profile.mobile_no
            data['role_id']                 =   user_profile.role.id
            data['role_name']               =   user_profile.role.role_name
            data['company_name']            =   user_profile.company_name
            data['organization_code']       =   user_profile.organization_code
            data['gender']                  =   user_profile.gender
            data['designation']             =   user_profile.designation
            data['base_location']           =   user_profile.base_location
            data['team_id']                 =   user_profile.team_id
            
            if Team.objects.values_list('team_name',flat=True).filter(id=user_profile.team_id).first():
                data['team_name']               =   Team.objects.values_list('team_name',flat=True).filter(id=user_profile.team_id).first()
            else:
                data['team_name']               =   None


            if Manager.objects.filter(id=user_profile.manager_id).exists():
                manager = Manager.objects.values_list('manager_name',flat=True).filter(id=user_profile.team_id).first()
    
                data['manager_id']              =   user_profile.manager_id
                data['manager_name']            =   manager

            else:
                data['manager_id']              =   None
                data['manager_name']            =   None
          
            data['default_language']        =   user_profile.default_language
            data['member_since']            =   user_profile.created_at.strftime("%d %B, %Y")

            if user_profile.last_active_on:
                data['last_active_on']          =   user_profile.last_active_on.strftime("%d/%m/%Y %I:%M:%S")
            else:
                data['last_active_on']          =   "-"

            data['is_verified_by_admin']    =   user_profile.is_verified_by_admin
            data['firebase_token']          =   request.data.get('firebase_token')
            data['created_at']              =   user_profile.created_at
            data['updated_at']              =   user_profile.updated_at
            data['is_active']               =   user_profile.is_active
            data['device_id']               =   user_profile.device_id 

            avatar_image = AvatarImage.objects.values().filter(id=user_profile.avatar_image_id).first()

            if avatar_image:
                data['avatar_image']        = settings.BASE_URL +"media/"+ avatar_image['image']
            else:
                data['avatar_image']        = ""

            data['organization']            =   Organiztaion.objects.values().filter(unique_code=user_profile.unique_code).first() 
            
            token,_=Token.objects.get_or_create(user=user_profile.user)

            data['token']                   =   token.key
            
            if firebase_token:
                UserProfile.objects.filter(user__email=request.data.get('email')).update(firebase_token=firebase_token)    
        else:
            return Response({'message': 'Your role is Invalid.', 'response_code':201}, status=HTTP_200_OK) 


    else:
        if role_id==user_profile.role.id:
            data['id']                      =   user_profile.id
            data['unique_code']             =   user_profile.unique_code 
            data['first_name']              =   user_profile.user.first_name
            data['last_name']               =   user_profile.user.last_name
            data['email']                   =   user_profile.user.email
            data['mobile_no']               =   user_profile.mobile_no
            data['role_id']                 =   user_profile.role.id
            data['role_name']               =   user_profile.role.role_name
            data['company_name']            =   user_profile.company_name
            data['organization_code']       =   user_profile.organization_code
            data['gender']                  =   user_profile.gender
            data['designation']             =   user_profile.designation
            data['base_location']           =   user_profile.base_location
            data['team_id']                 =   user_profile.team_id

            if Team.objects.values_list('team_name',flat=True).filter(id=user_profile.team_id).first():
                data['team_name']               =   Team.objects.values_list('team_name',flat=True).filter(id=user_profile.team_id).first()
            else:
                data['team_name']               =   None

            data['manager_name']            =  user_profile.user.first_name + " "+user_profile.user.last_name  

            data['default_language']        =   user_profile.default_language
            data['member_since']            =   user_profile.created_at.strftime("%d %B, %Y")
            if user_profile.last_active_on:
                data['last_active_on']          =   user_profile.last_active_on.strftime("%d/%m/%Y %I:%M:%S")
            else:
                data['last_active_on']          =   "-"    
            data['is_verified_by_admin']    =   user_profile.is_verified_by_admin
            data['firebase_token']          =   request.data.get('firebase_token')
            data['created_at']              =   user_profile.created_at
            data['updated_at']              =   user_profile.updated_at
            data['is_active']               =   user_profile.is_active
            data['device_id']               =   user_profile.device_id
            
            avatar_image = AvatarImage.objects.values().filter(id=user_profile.avatar_image_id).first()
            
            if avatar_image:
                data['avatar_image']        = settings.BASE_URL + avatar_image['image']
            else:
                data['avatar_image']        = ""

            data['organization']            =   Organiztaion.objects.values().filter(unique_code=user_profile.unique_code).first() 
            
            token,_=Token.objects.get_or_create(user=user_profile.user)

            data['token']                   =   token.key
            
            if firebase_token:
                UserProfile.objects.filter(user__email=request.data.get('email')).update(firebase_token=firebase_token)    
        else:
            return Response({'message': 'Your role is Invalid.', 'response_code':201}, status=HTTP_200_OK) 
     

    user_name   = user_profile.user.first_name+' '+user_profile.user.last_name

    heading     = user_name+' has been logged In'
    
    activity    = user_name+' has been logged In on '+datetime.now().strftime('%d/%m/%Y | %I:%M %p') 
    
    save_activity('Login', 'Login', heading, activity, user_profile.id, user_name, 'login.png', '1', 'app.png') # '1' means app // '2' means web
   

    context = {}
    context['user_data']                = data
    context['response_code']            = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)



@csrf_exempt
@api_view(["POST"])
def UserProfileList(request):
    
    context = {}
    context['message']       = 'Profile has been received successfully'
    
    context['response_code'] = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)



@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def role_lists(request):
    role = Role.objects.all().values()
    context = {}
    context['role']          = role
    context['message']       = 'Role data has been received successfully'
    context['response_code'] = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)




# Deo Abhi ------------

@csrf_exempt
@api_view(["GET"])
@authenticate_token
def user_profile_list(request,pk):
    userprofile_serializer = UserProfileListSerializer(UserProfile.objects.get(pk=pk))
    return Response(data = {'msg':'success','data':userprofile_serializer.data,},status=status.HTTP_200_OK)  
    




# UserProfile Update -------------
@csrf_exempt
@api_view(['PUT'])
@authenticate_token
def user_profile_update(request,pk):
    user_profile            = UserProfile.objects.get(pk=pk)
    user                    = User.objects.filter(id=user_profile.user.id).first()
    user.first_name         = request.data.get('first_name')
    user.last_name          = request.data.get('last_name')
    user.save()
    
     
    # user_profile_serializer = UserProfileUpdateSerializer(user_profile,data=request.data,partial=True)
    
    # if user_profile_serializer.is_valid():
  
    #     user_profile_serializer.save()
    
    
    if not user_profile.is_updated:

        points = RewardPointsStimulator.objects.filter(status=2).first()

        if MyRewardPoint.objects.filter(user_profile__id=user_profile.id).exists():

            my_reward = MyRewardPoint.objects.filter(user_profile__id=user_profile.id).last()

            point_balance = my_reward.point_balance + int(points.multiplier)

            my_reward = MyRewardPoint.objects.create(
                manager_id=0,              
                user_profile=user_profile,
                earned_point=int(points.multiplier),
                point_balance=point_balance
            )
        else:
            my_reward = MyRewardPoint.objects.create(
                manager_id=0,              
                user_profile=user_profile,
                earned_point=int(points.multiplier),
                point_balance=int(points.multiplier)
            )
    
        user_profile.is_updated = 1
        user_profile.save()
 
        # serializer_data = UserProfileListSerializer(user_profile)

        # data = user_profile_serializer.data

        # if data['team_id']:
        #     data['team_name']               =   Team.objects.values_list('team_name',flat=True).filter(id=data['team_id']).first()
        # else:
        #     data['team_name']               =   None

        # if data['manager_id']:         
        #     data['manager_name']            =   Manager.objects.values_list('manager_name',flat=True).filter(id=data['manager_id']).first()
        # else:
        #     data['manager_name']            =   None

    return Response(data= {'msg':'Data saved Successfully','status':True,'response_code':200}, status=status.HTTP_200_OK)
    # else:
    #     return Response(data={'msg':'Data not Saved','response_code':201},status=status.HTTP_201_CREATED)




# Update Avatar Image -------------
@csrf_exempt
@api_view(['POST'])
@authenticate_token
def update_avatar_image(request):
    if request.data.get("user_profile_id") == '' or request.data.get("user_profile_id") is None:  
        return Response({'message': 'Please provide user profile id', 'response_code':201}, status=HTTP_200_OK) 
    if request.data.get("avatar_image_id") == '' or request.data.get("avatar_image_id") is None:  
        return Response({'message': 'Please provide avatar image id', 'response_code':201}, status=HTTP_200_OK) 
    

    user_profile_id = request.data.get('user_profile_id')
    avatar_image_id = request.data.get('avatar_image_id')

    avatar_image = AvatarImage.objects.values().filter(id=request.data.get('avatar_image_id')).first() 

    avatar_image['image'] = settings.BASE_URL+"media/"+avatar_image['image']
    try:
        user_profile  = UserProfile.objects.get(id=user_profile_id)
    except Exception as e:
        Response(data= {'msg':str(e),'response_code':404}, status=HTTP_404_NOT_FOUND)

    if not user_profile.avatar_image_id:
        points = RewardPointsStimulator.objects.filter(status=3).first()
 
        if MyRewardPoint.objects.filter(user_profile__id=user_profile.id).exists():

            my_reward = MyRewardPoint.objects.filter(user_profile__id=user_profile.id).last()

            point_balance = my_reward.point_balance + int(points.multiplier)

            my_reward = MyRewardPoint.objects.create(
                manager_id=0,              
                user_profile=user_profile,
                earned_point=int(points.multiplier),
                point_balance=point_balance
            )
        else:
            my_reward = MyRewardPoint.objects.create(
                manager_id=0,              
                user_profile=user_profile,
                earned_point=int(points.multiplier),
                point_balance=int(points.multiplier)
            )
    

        user_profile.avatar_image_id=avatar_image_id
        user_profile.save() 

    return Response(data= {'msg':'Data saved Successfully','data':avatar_image,'response_code':200}, status=status.HTTP_200_OK)
   


@csrf_exempt
@api_view(["POST"])
@authenticate_token
def user_logout(request):
    user_profile_id = request.data.get('user_profile_id')
    user_profile = UserProfile.objects.filter(id=user_profile_id).first()
    
    if user_profile:

        user_profile.is_active = 0
        user_profile.save()
        
        user_instance= Token.objects.filter(user__id=user_profile.user.id)
        user_instance.delete()

        current_date_time = datetime.now()
        
        user_profile.last_active_on=current_date_time
        
        user_profile.save()

        UserProfile.objects.filter(id=user_profile_id).update(firebase_token=None)
        
        UserProfile.objects.filter(id=user_profile_id).update(device_id=None)
        
        return Response({"message":"User Logged Out successfully"})
    else:
        pass


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def show_msg_user_already_login(request):
    
    email = request.data.get('email')

    device_id = request.data.get('device_id')
    
    role_id = request.data.get('role_id')

    password        = request.data.get('password') 

    user_profile = UserProfile.objects.filter(user__email=email).first()

    if int(role_id)!=user_profile.role.id:
        return Response({'message': 'You are not authorized with this role.', 'response_code':202}, status=HTTP_200_OK) 

    
    if not check_password(request.data.get("password"), user_profile.user.password):
        return Response({'message': 'Invalid Credentials', 'response_code':202}, status=HTTP_200_OK)

    if not user_profile:
        if not user_profile:   
            return Response({'message': 'Success', 'response_code':200}, status=HTTP_200_OK)
        elif not user_profile.device_id:
            return Response({'message': 'Success', 'response_code':200}, status=HTTP_200_OK)
    else:
        if user_profile.device_id:   
            if user_profile.device_id!=device_id:
                return Response({'message': 'You are logged in with another device.', 'response_code':201}, status=HTTP_200_OK) 
            else:
                return Response({'message': 'Success', 'response_code':200}, status=HTTP_200_OK) 
        else:
            return Response({'message': 'Success', 'response_code':200}, status=HTTP_200_OK) 

@csrf_exempt
@api_view(["POST"])
@authenticate_token
def user_login_check(request):
    
    user_profile_id = request.data.get('user_profile_id')

    device_id = request.data.get('device_id')
    
    user_profile = UserProfile.objects.filter(id=user_profile_id).first()
    
    if user_profile.device_id == device_id:
        status_value = 0
    else:
        status_value  = 1

    context = {}
    context['status'] = status    
    return Response({'message': 'Data received successfully.',"status":status_value,'response_code':200},status=HTTP_200_OK) 
            



@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def send_otp(request):

    if request.data.get("user_email") == '' or request.data.get("user_email") is None:  
        return Response({'message': 'Please provide user email', 'response_code':201}, status=HTTP_200_OK) 
    if request.data.get("user_mobile_no") == '' or request.data.get("user_mobile_no") is None:  
        return Response({'message': 'Please provide user mobile no', 'response_code':201}, status=HTTP_200_OK) 

    user_email     = request.data.get('user_email')
    user_mobile_no = request.data.get("user_mobile_no")
    
    user_profile = UserProfile.objects.filter(user__email=user_email,mobile_no=user_mobile_no).first()

    if user_profile:

        otp = generate_otp()
        
        try:
            user_otp = PasswordResetOTP.objects.filter(email=user_email,mobile=user_mobile_no).first()
        except PasswordResetOTP.DoesNotExist:
            user_otp = None
        
        if user_otp:
            PasswordResetOTP.objects.filter(email=user_email,mobile=user_mobile_no).delete()

        user_otp           = PasswordResetOTP()
        user_otp.email     = user_email
        user_otp.mobile    = user_mobile_no
        user_otp.otp       = otp
        user_otp.save()

    
        # send otp on email and mobile no

        context = {}

        context['name']  = user_profile.user.first_name + " " +user_profile.user.last_name
        context['otp']   = otp

        template = 'email/email_otp.html'

        
        subject = "OTP for reset password"

        recipient = user_email
        
        message_email=f"Otp sent successfully to {recipient}."
        send_email(request,template,context,subject,recipient)

        # message = f"Your OTP is: {otp} ."
        # send_sms('Game On',user_mobile_no,message)

        return Response({'message':message_email,'response_code':200},status=HTTP_200_OK) 
    else:
        return Response({'message': 'Your email or mobile no is invalid.','response_code':201},status=HTTP_200_OK) 

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def reset_password(request):


    if request.data.get("user_email") == '' or request.data.get("user_email") is None:  
        return Response({'message': 'Please provide user email', 'response_code':201}, status=HTTP_200_OK) 


    if request.data.get("user_mobile_no") == '' or request.data.get("user_mobile_no") is None:  
        return Response({'message': 'Please provide user mobile no', 'response_code':201}, status=HTTP_200_OK) 

    if request.data.get("otp") == '' or request.data.get("otp") is None:  
        return Response({'message': 'Please provide otp', 'response_code':201}, status=HTTP_200_OK) 

    if request.data.get("password") == '' or request.data.get("password") is None:  
        return Response({'message': 'Please provide password', 'response_code':201}, status=HTTP_200_OK) 

    if request.data.get("cpassword") == '' or request.data.get("cpassword") is None:  
        return Response({'message': 'Please provide confirm password', 'response_code':201}, status=HTTP_200_OK) 

    if request.data.get("firebase_token") == '' or request.data.get("firebase_token") is None:  
        return Response({'message': 'Please provide firebase token', 'response_code':201}, status=HTTP_200_OK) 

    user_email     = request.data.get('user_email')
    user_mobile_no = request.data.get("user_mobile_no")
    otp = request.data.get("otp")

    password = request.data.get("password")
    cpassword = request.data.get("cpassword")
    
  
    try:
        user_otp = PasswordResetOTP.objects.filter(email=user_email,mobile=user_mobile_no).first()
    except PasswordResetOTP.DoesNotExist:
        user_otp = None
    

    if user_otp.otp==otp:
        if password==cpassword:
            user_profile = UserProfile.objects.filter(user__email=user_email).first()
            user         = User.objects.get(email=user_profile.user.email)

            user.password  = make_password(str(request.data.get("password")))
            user.save()
            
            userFirebaseToken = request.data.get("firebase_token")

            message_title = "Your password has been reset successfully"
            message_body = "Your password has been reset now you can login"
            notification_image = ""

            if userFirebaseToken is not None and userFirebaseToken != "" :
                registration_ids = []
                registration_ids.append(userFirebaseToken)
                data_message = {}
                data_message['id'] = 1
                data_message['status'] = 'notification'
                data_message['click_action'] = 'login_page'

                data_message['image'] = notification_image

                send_android_notification(message_title,message_body,data_message,registration_ids)
                
                heading="Your password has been reset successfully"

                notification_msg="Your password has been reset successfully now you can login"

              
                save_notification(None,user_profile.id,heading,notification_msg)

            return Response({'message': 'Password has been changed successfully.','response_code':200},status=HTTP_200_OK) 
        else:
            return Response({'message': 'Password and confirm password is not matched.','response_code':201},status=HTTP_200_OK) 
    else:
        return Response({'message': 'Otp is incorrect.','response_code':201},status=HTTP_200_OK) 






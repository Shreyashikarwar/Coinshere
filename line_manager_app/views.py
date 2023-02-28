from enum import unique
from multiprocessing import context
from re import M
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from django.contrib.auth.models import User

from rest_framework.response import Response
from datetime import datetime,date, timedelta

from yaml import serialize

current_date   = date.today()

from django.db.models import Sum

# Status and Response 
from rest_framework import status
from rest_framework.response import Response

import math

import pandas as pd


# Import Models and Serializers
from .models import *
from .serializers import ManagerRaiseConcernSerializers,ManagerConcernCategorySerializers,ManagerReasonTypeSerializers,ManagerJoshReasonSerializer,ManagerSerializer,TeamCampaignSerializers


from accounts.models import *

from customer_service_app.models import *

from decorators.decorators import *

from utils.helpers import *

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

@csrf_exempt
@api_view(["GET"])
@authenticate_token
def challenge_purpose_list(request):
    challenge_purpose = ChallengePurpose.objects.filter(status=1).values()

    context = {}
    context['challenge_purpose'] = challenge_purpose
    return Response(context, status=HTTP_200_OK)



@csrf_exempt
@api_view(["POST"])
@authenticate_token
def create_challenge(request):
    if request.data.get("user_id") is None or request.data.get("user_id") == '':
        return Response({'message': 'User Id field is required', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)
    if request.data.get("challenge_purpose_id") is None or request.data.get("challenge_purpose_id") == '':
        return Response({'message': 'Challenge Purpose Id field is required', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)
    if request.data.get("challenge_name") is None or request.data.get("challenge_name") == '':
        return Response({'message': 'Challenge Name field is required', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)
    
    if request.data.get("start_time") is None or request.data.get("start_time") == '':
        return Response({'message': 'Start time field is required', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)

    if request.data.get("end_time") is None or request.data.get("end_time") == '':
        return Response({'message': 'End time field is required', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)

    if request.data.get("broadcast_id") is None or request.data.get("broadcast_id") == '': # braodcast_id = 1
        return Response({'message': 'Broadcast Id field is required', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)


    if request.data.get("activity_details") is None or request.data.get("activity_details") == '':
        return Response({'message': 'Activity details field field is required', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)
  
    if request.data.get("bonus_point") is None or request.data.get("bonus_point") == '':
        return Response({'message': 'Bonus point field is required', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)

    if request.data.get("industry_work_type_id") is None or request.data.get("industry_work_type_id") == '':
        return Response({'message': 'Industry work type field is required', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)

    if request.data.get("kpi_name_id") is None or request.data.get("kpi_name_id") == '':
        return Response({'message': 'KPI name id field is required', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)

    if not TeamChallenge.objects.filter(manager__id=request.data.get('user_id'),challenge_name__icontains=request.data.get('challenge_name')).exists():

        try:
            user_profile = UserProfile.objects.get(id=request.data.get('user_id'))        
        except Exception as e:
            return Response({'message':str(e)}, status=HTTP_404_NOT_FOUND)
            
        try:
            challenge_purpose = ChallengePurpose.objects.get(id=request.data.get('challenge_purpose_id'))
        except Exception as e:
            return Response({'message':str(e)}, status=HTTP_404_NOT_FOUND)
                
        team_challenge                   = TeamChallenge()
        team_challenge.manager           = user_profile
        team_challenge.challenge_purpose = challenge_purpose
        team_challenge.challenge_name    = request.data.get('challenge_name')
        
      
        team_challenge.start_time          = request.data.get("start_time")
        team_challenge.end_time            = request.data.get("end_time")
        team_challenge.activity_details    = request.data.get('activity_details') 
        team_challenge.bonus_point         = request.data.get('bonus_point')
        team_challenge.industry_work_type  = request.data.get('industry_work_type_id') 
        team_challenge.kpi_name_id         = request.data.get('kpi_name_id')

        team_challenge.is_broadcasted      = request.data.get("broadcast_id") 
        
        team_challenge.save()

        employee_profile =UserProfile.objects.filter(team_id=user_profile.team_id,is_active=1,role__id=1)
    
        # body = "Hello,Sir!\nHow are you doing?"

        # broadcast_message_on_whatsapp(body)

        manager_name= user_profile.user.first_name +" "+user_profile.user.last_name

        for profile in employee_profile:
            userFirebaseToken = profile.firebase_token

            message_title = "New Challenge"
            message_body = f"Hey, {manager_name} has just set up a new challenge, do you think you can do it ? Accept it and tell us you can do it"
            
            notification_image = ""

            if userFirebaseToken is not None and userFirebaseToken != "" :
                registration_ids = []
                registration_ids.append(userFirebaseToken)
                data_message = {}
                data_message['id'] = 1
                data_message['status'] = 'notification'
                data_message['click_action'] = 'new_challenge'

                data_message['image'] = notification_image

                send_android_notification(message_title,message_body,data_message,registration_ids)
                
                heading="New Challenge"

                notification_msg=f"Hey, {manager_name} has just set up a new challenge, do you think you can do it ? Accept it and tell us you can do it"

                save_notification(profile.id,profile.id,heading,notification_msg,'new_challenge')

    else:
        return Response({'message':"The Challenge has been already created"}, status=HTTP_200_OK)    
         

    context            = {}
    context['message'] = "Team challenge has been broadcasted successfully"
    return Response(context, status=HTTP_200_OK)



@csrf_exempt
@api_view(["POST"])
@authenticate_token
def broadcast_challenge(request):
    if request.data.get("user_id") is None or request.data.get("user_id") == '':
        return Response({'message': 'User Id field is required', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)
    
    if request.data.get("challenge_id") is None or request.data.get("challenge_id") == '':
        return Response({'message': 'Challenge Id field is required', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)

    if request.data.get("broadcast_id") is None or request.data.get("broadcast_id") == '': # braodcast_id = 1
        return Response({'message': 'Broadcast Id field is required', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)
    
    if TeamChallenge.objects.filter(manager__id=request.data.get('user_id'),id=request.data.get('challenge_id'),is_broadcasted=1):
           return Response({'message': 'This challenge has been already broadcasted', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)

    try:       
        team_challenge = TeamChallenge.objects.get(manager__id=request.data.get('user_id'),id=request.data.get('challenge_id'))
    except Exception as e:
        return Response({'message':str(e)}, status=HTTP_404_NOT_FOUND)
    
    manager = UserProfile.objects.filter(id=request.data.get("user_id")).first()

    user_profile =UserProfile.objects.filter(team_id=manager.team_id,is_active=1,role__id=1)
    
    body = "Hello,Sir!\nHow are you doing?"

    broadcast_message_on_whatsapp(body)

    manager_name= manager.user.first_name +" "+manager.user.last_name

    for profile in user_profile:
        userFirebaseToken = profile.firebase_token

        message_title = "New Challenge"
        message_body = f"Hey, {manager_name} has just set up a new challenge, do you think you can do it ? Accept it and tell us you can do it"
        
        notification_image = ""

        if userFirebaseToken is not None and userFirebaseToken != "" :
            registration_ids = []
            registration_ids.append(userFirebaseToken)
            data_message = {}
            data_message['id'] = 1
            data_message['status'] = 'notification'
            data_message['click_action'] = 'new_challenge'

            data_message['image'] = notification_image

            send_android_notification(message_title,message_body,data_message,registration_ids)
            
            heading="New Challenge"

            notification_msg=f"Hey, {manager_name} has just set up a new challenge, do you think you can do it ? Accept it and tell us you can do it"

            save_notification(profile.id,profile.id,heading,notification_msg)



    team_challenge.is_broadcasted = request.data.get("broadcast_id")
    team_challenge.save()      

    context            = {}
    context['message'] = "Challenge has been broadcasted successfully"
    return Response(context, status=HTTP_200_OK)



@csrf_exempt
@api_view(["POST"])
@authenticate_token
def create_campaign(request):
    if request.data.get("user_id") is None or request.data.get("user_id") == '':
        return Response({'message': 'User Id field is required', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)
    if request.data.get("campaign_purpose_id") is None or request.data.get("campaign_purpose_id") == '':
        return Response({'message': 'Campaign Purpose Id field is required', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)
    if request.data.get("campaign_name") is None or request.data.get("campaign_name") == '':
        return Response({'message': 'Campaign Name field is required', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)
    if request.data.get("start_date") is None or request.data.get("start_date") == '':
        return Response({'message': 'Start date field is required', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)
    if request.data.get("end_date") is None or request.data.get("end_date") == '':
        return Response({'message': 'End date field is required', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)

    if request.data.get("broadcast_id") is None or request.data.get("broadcast_id") == '': # braodcast_id = 1
        return Response({'message': 'Broadcast Id field is required', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)

    if request.data.get("criteria_point") is None or request.data.get("criteria_point") == '':
        return Response({'message': 'Criteria point field is required', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)

    if request.data.get("industry_work_type_id") is None or request.data.get("industry_work_type_id") == '':
        return Response({'message': 'Industry work type field is required', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)

    if not TeamCampaign.objects.filter(manager__id=request.data.get('user_id'),campaign_name__icontains=request.data.get('campaign_name')).exists():

        if not request.data.get('criteria_point'):
            return Response({'message': 'Criteria point field data is required', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)

        try:
            user_profile = UserProfile.objects.get(id=request.data.get('user_id'))        
        except Exception as e:
            return Response({'message':str(e)}, status=HTTP_404_NOT_FOUND)
            
        try:
            campaign_purpose = CampaignPurpose.objects.get(id=request.data.get('campaign_purpose_id'))
        except Exception as e:
            return Response({'message':str(e)}, status=HTTP_404_NOT_FOUND)
      

        team_campaign      = TeamCampaign.objects.create(
        manager            = user_profile,
        campaign_purpose   = campaign_purpose,
        campaign_name      = request.data.get("campaign_name"),
        start_date         = request.data.get('start_date'),
        end_date           = request.data.get('end_date'),
        industry_work_type = request.data.get("industry_work_type_id"),
        is_broadcasted     = request.data.get("broadcast_id"),
        end_campaign_date  = datetime.strptime(request.data.get('end_date'),'%Y-%m-%d').date()+timedelta(days=1)
        
        )

        

        
        for data in request.data.get('criteria_point'):

            criteria_obj = CriteriaPoint.objects.create(
                kpi_id= data['kpi_id'], # kpi id
                rule  = data['rule'],   # kpi name
                point = data['point']
            )
            team_campaign.criteria_point.add(criteria_obj)

        
        employee_profile =UserProfile.objects.filter(team_id=user_profile.team_id,is_active=1,role__id=1)

        manager_name= user_profile.user.first_name +" "+user_profile.user.last_name

        for profile in employee_profile:

            team_accept_campaign                      = TeamAcceptCampaignHistory()
            team_accept_campaign.team_campaign        = team_campaign
            team_accept_campaign.customer_accepted_id = profile.id
            team_accept_campaign.is_accepted          = 1
            team_accept_campaign.save()


            userFirebaseToken = profile.firebase_token

            message_title = "New Campaign"
            message_body = f"Hey, {manager_name} has just set up a new campaign, take a look and see what's in store for you"
            
            notification_image = ""

            if userFirebaseToken is not None and userFirebaseToken != "" :
                registration_ids = []
                registration_ids.append(userFirebaseToken)
                data_message = {}
                data_message['id'] = 1
                data_message['status'] = 'notification'
                data_message['click_action'] = 'new_campaign'

                data_message['image'] = notification_image

                send_android_notification(message_title,message_body,data_message,registration_ids)
                
                heading="New Campaign"
                
                notification_msg=f"Hey, {manager_name} has just set up a new campaign, take a look and see what's in store for you"

                save_notification(profile.id,profile.id,heading,notification_msg,'new_campaign')

    
    else:
        return Response({'message':"The Campaign has been already created",'response_code':201}, status=HTTP_200_OK)    


    context = {}
    context['message'] = "Team campaign has been broadcasted successfully"
    context['response_code']= 200
    return Response(context, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@authenticate_token
def broadcast_campaign(request):
    if request.data.get("user_id") is None or request.data.get("user_id") == '':
        return Response({'message': 'User Id field is required', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)
    
    if request.data.get("campaign_id") is None or request.data.get("challenge_id") == '':
        return Response({'message': 'Campaign Id field is required', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)

    if request.data.get("broadcast_id") is None or request.data.get("broadcast_id") == '': # braodcast_id = 1
        return Response({'message': 'Broadcast Id field is required', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)

    if TeamCampaign.objects.filter(manager__id=request.data.get('user_id'),id=request.data.get('campaign_id'),is_broadcasted=1):
        return Response({'message': 'This campaign has been already broadcasted', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)

    try:       
        team_campaign = TeamCampaign.objects.get(manager__id=request.data.get('user_id'),id=request.data.get('campaign_id'))
    except Exception as e:
        return Response({'message':str(e)}, status=HTTP_404_NOT_FOUND)

    manager = UserProfile.objects.filter(id=request.data.get("user_id")).first()

    user_profile =UserProfile.objects.filter(team_id=manager.team_id,is_active=1,role__id=1)

    manager_name= manager.user.first_name +" "+manager.user.last_name

    for profile in user_profile:

        team_accept_campaign                      = TeamAcceptCampaignHistory()
        team_accept_campaign.team_campaign        = team_campaign
        team_accept_campaign.customer_accepted_id = profile.id
        team_accept_campaign.is_accepted          = 1
        team_accept_campaign.save()


        userFirebaseToken = profile.firebase_token

        message_title = "New Campaign"
        message_body = f"Hey, {manager_name} has just set up a new campaign, take a look and see what's in store for you"
        
        notification_image = ""

        if userFirebaseToken is not None and userFirebaseToken != "" :
            registration_ids = []
            registration_ids.append(userFirebaseToken)
            data_message = {}
            data_message['id'] = 1
            data_message['status'] = 'notification'
            data_message['click_action'] = 'new_campaign'

            data_message['image'] = notification_image

            send_android_notification(message_title,message_body,data_message,registration_ids)
            
            heading="New Campaign"
            
            notification_msg=f"Hey, {manager_name} has just set up a new campaign, take a look and see what's in store for you"

            save_notification(profile.id,profile.id,heading,notification_msg)


    team_campaign.is_broadcasted = request.data.get("broadcast_id")
    team_campaign.save()      

    context            = {}
    context['message'] = "Campaign has been broadcasted successfully"
    return Response(context, status=HTTP_200_OK)



@csrf_exempt
@api_view(["GET"])
@authenticate_token
def campaign_purpose_list(request):
    campaign_purpose = CampaignPurpose.objects.filter(status=1).values()

    context = {}
    context['campaign_purpose'] = campaign_purpose
    return Response(context, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@authenticate_token
def review_challenge(request):
    if request.data.get("user_id") is None or request.data.get("user_id") == '':
        return Response({'message': 'User Id field is required', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)

    if request.data.get("team_id") is None or request.data.get("team_id") == '':
        return Response({'message': 'User Id field is required', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)

    current_date=datetime.now().date()
    current_time=datetime.now().strftime('%H:%M:%S')

   
    challenge_data = TeamChallenge.objects.filter(manager__id=request.data.get('user_id')).values()
   
    total_challenges_running = 0

    total_employee = UserProfile.objects.filter(team_id=request.data.get("team_id"),role__id=1).count()
    
    if not total_employee:
        total_employee = 1
    
    if challenge_data:
    
        for data in challenge_data:
            
            print(data['updated_at'].date())

            if data['start_time']<=current_time and current_time<=data['end_time'] and current_date==data['updated_at'].date():

               if data['is_broadcasted']: 
                    total_challenges_running +=1

            data['purpose_name'] =  ChallengePurpose.objects.filter(id=data['challenge_purpose_id']).first().purpose_name
            
            kpi_name = KpiName.objects.filter(id=data['kpi_name_id']).first()

            if kpi_name:
                data['kpi_name'] = kpi_name.name
            else:
                data['kpi_name'] = ""    
            

            team_challenge_count = TeamAcceptChallengeHistory.objects.filter(team_challenge__id=data['id']).count()
               
            data['participation_percent']    = round(team_challenge_count%total_employee,2)
            data['win_percent']              = 0

    context = {}
    context['message']        = "Challenges data has been received successfully"

    context['challenge_data'] = challenge_data

    context['total_challenges_running'] = total_challenges_running
    
    return Response(context, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@authenticate_token
def review_campaign(request):
    if request.data.get("user_id") is None or request.data.get("user_id") == '':
        return Response({'message': 'User Id field is required', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)

    campaign_data = TeamCampaign.objects.filter(manager__id=request.data.get('user_id'))
    
    data = [] 
    
    current_date = datetime.now().date()

    total_campaings_running = 0

    if campaign_data:
        for obj in campaign_data:
            if obj.start_date<=current_date and obj.end_date>=current_date and obj.is_completed_by_manager==0:
                if obj.is_broadcasted:
                    total_campaings_running +=1

            dict = {}
            dict['id']                       = obj.id 
            dict['purpose_name']             = obj.campaign_purpose.purpose_name
            dict['campaign_name']            = obj.campaign_name
            dict['industry_work_type']       = obj.industry_work_type
            dict['customer_accepted_id']     = obj.customer_accepted_id
            dict['start_date']               = obj.start_date
            dict['end_date']                 = obj.end_date
            dict['is_accepted']              = obj.is_accepted
            dict['is_broadcast']             = obj.is_broadcasted
            dict['is_completed_by_customer'] = obj.is_completed_by_customer
            dict['is_completed_by_manager']  = obj.is_completed_by_manager
            
            dict['created_at']               = obj.created_at
            dict['updated_at']               = obj.updated_at 
          
            kpi_data = obj.criteria_point.all().values()
            
            for dataa in kpi_data: 
                kpi_name = KpiName.objects.filter(id=dataa['kpi_id']).first()   
                
                dataa['kpi_name'] = kpi_name.name

            dict['kpi_data']     =  kpi_data
            
            data.append(dict)  

    context = {}
    context['message']        = "Campaigns data has been received successfully"


    context['campaign_data'] = data
    
    context['total_campaigns_running'] = total_campaings_running

    return Response(context, status=HTTP_200_OK)


# Deo Abhinav 


# Manager_concern_category


@csrf_exempt
@api_view(["GET"])
@authenticate_token
def manager_concern_category(request):
    manager_concern_choice = ManagerConcernCategory.objects.filter(status=1).values()
   
    context = {}

    context['manager_concern_category']    = manager_concern_choice
    context['message']       = 'manager_concern_Category data has been received successfully'
    # context['response_code'] = HTTP_200_OK
    return Response(context,status=status.HTTP_200_OK)




# line manager Consern Post
# Deo abhinav 

@csrf_exempt
@api_view(['POST'])
@authenticate_token
def manager_raise_concern_update(request):

    # Get Super User Data
    user_data = UserProfile.objects.filter(id=request.data.get('user_profile')).first()
    # super_id=superusers.id
    manager_serializer=ManagerRaiseConcernSerializers(data=request.data)
    
    unique_code = user_data.unique_code
                
    concern_category=request.data.get('concern_category')

 
    if manager_serializer.is_valid():
        manager_serializer.save()
        data = manager_serializer.data
        manager_raise_concern = ManagerRaiseConcern.objects.filter(id=data['id']).first()

        if int(concern_category)==1:
            admin_user = User.objects.filter(id=1,is_superuser=1).first()

            manager_raise_concern.action_owner_id = admin_user.id
        else:
            unique_code = user_data.unique_code
            
            admin_user = Organiztaion.objects.filter(unique_code=unique_code).first()

            manager_raise_concern.action_owner_id = admin_user.id

        # manager_raise_concern.action_owner_id = super_id
        manager_raise_concern.save()


# For Showning Data in Serializers

        data['action_owner_id'] = admin_user.id
        return Response(data={'msg':'Data Sent Successfully','Data':data,'response_code':200},status=status.HTTP_200_OK)
    else:
        return Response(data={'msg':'Data Not Sent','response_code':201},status=status.HTTP_201_CREATED)
        





# Line Manager Josh Create  -----

# Deo abhinav 
@csrf_exempt
@api_view(['POST'])
@authenticate_token
def manager_josh_create(request):
        manager_josh_create_serializer=ManagerJoshReasonSerializer(data=request.data)
        
        user_id = int(request.data.get('manager'))

        user_profile = UserProfile.objects.filter(id=user_id).first()


        current_date=datetime.now().date()

        if not ManagerJoshReason.objects.filter(manager=user_profile,created_at__icontains=current_date).first():

            if request.data.get('reason_type')=="" or request.data.get('reason_type') is None :
                
                points = RewardPointsStimulator.objects.filter(status=10).first()

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

            

            if manager_josh_create_serializer.is_valid():

                manager_josh_create_serializer.save()
                data = manager_josh_create_serializer.data

                emoji_point = data['emoji_point']
    
                if int(emoji_point)<=3:
                
                    points = RewardPointsStimulator.objects.filter(status=11).first()

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


                    userFirebaseToken = user_profile.firebase_token

                    message_title = "Your Josh"

                    message_body = "Its ok, we all have happy and sad days, but thankfully you have a friend in Game On, tell us why your Josh is low today, click here"
                    
                    notification_image = ""

                    if userFirebaseToken is not None and userFirebaseToken != "" :
                        registration_ids = []
                        registration_ids.append(userFirebaseToken)
                        data_message = {}
                        data_message['id'] = 1
                        data_message['status'] = 'notification'

                        data_message['click_action'] = 'my_josh'

                        data_message['image'] = notification_image

                        send_android_notification(message_title,message_body,data_message,registration_ids)
                        
                        heading="Your Josh"

                        notification_msg="Its ok, we all have happy and sad days, but thankfully you have a friend in Game On, tell us why your Josh is low today, click here"

                        save_notification(user_profile.id,user_profile.id,heading,notification_msg,'my_josh')

                return Response(data={'msg':'Data Sent Succesfully','Data':manager_josh_create_serializer.data,'response_code':200},status=status.HTTP_200_OK)
            return Response(manager_josh_create_serializer.errors, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'msg':'Today,you have created your josh so you can not create your josh again.','response_code':201},status=status.HTTP_200_OK)
             


# Deo abhinav 
@csrf_exempt
@api_view(['GET'])
@authenticate_token
def manager_josh_reason_list(request):
    try:
        user_profile_id = request.query_params.get('user_profile')
    except:
        return Response({'Msg':'Please Provide user_profile_data in params'})

    print(user_profile_id)

    manager_josh_data=ManagerJoshReason.objects.filter(manager__id=user_profile_id)

    manager_josh_data_count=ManagerJoshReason.objects.filter(manager__id=user_profile_id).count()
    
    manager_josh_serializer=ManagerJoshReasonSerializer(manager_josh_data,many=True)
    
    return Response(data={'count':manager_josh_data_count,'msg':'Success','data':manager_josh_serializer.data,'response_code':200},status=status.HTTP_200_OK)



# Customer Josh Data For Today

@csrf_exempt
@api_view(['GET'])
@authenticate_token
def manager_josh_reason_today(request):
    try:
        user_profile_data = request.query_params.get('user_profile')
    except:
        return Response({'Msg':'Please Provide user_profile_data in params'})

    try:
        team_id = request.query_params.get('team_id')
    except:
        return Response({'Msg':'Please Provide team id in params'})

# Get Current Date

    current_date = datetime.now().date()
    # print(current_date_data)

    total_team_mood_count =JoshReason.objects.filter(manager_id=team_id,created_at__icontains=current_date).count()
    
    if not total_team_mood_count:
        total_team_mood_count = 1
    else:   

        total_team_mood_count = total_team_mood_count   

    total_team_mood_sum =JoshReason.objects.filter(manager_id=team_id,created_at__icontains=current_date).aggregate(Sum('emoji_point'))
    
    print(total_team_mood_count,total_team_mood_sum) 

    if not total_team_mood_sum['emoji_point__sum']:
        total_team_mood_sum = 0
    else:
        total_team_mood_sum = total_team_mood_sum['emoji_point__sum']     
     
   

    team_mood  = round(total_team_mood_sum / total_team_mood_count)
    


    end_date = current_date

    start_date = current_date - timedelta(days=4)
    
    moodalytics = []

    while start_date<=end_date:
        data = {}
        josh_reason =ManagerJoshReason.objects.filter(manager__id=user_profile_data,created_at__icontains=start_date).first()

        if josh_reason: 
            data['date']        = start_date
            data['emoji_point'] = josh_reason.emoji_point
        else:
            data['date']        = start_date
            data['emoji_point'] = 0
        
        moodalytics.append(data)

        start_date = start_date +timedelta(days=1)


    manager_josh_data=ManagerJoshReason.objects.filter(manager__id=user_profile_data,created_at__icontains=current_date).first()
    manager_josh_data_count=ManagerJoshReason.objects.filter(manager__id=user_profile_data,created_at__icontains=current_date).count()
    manager_josh_serializer=ManagerJoshReasonSerializer(manager_josh_data)

    return Response(data={'count':manager_josh_data_count,'msg':'Success','data':manager_josh_serializer.data,'team_mood':team_mood,'moodalytics':moodalytics,'response_code':200},status=status.HTTP_200_OK)



@csrf_exempt
@api_view(["GET"])
@authenticate_token
def manager_raise_concern_list(request):

    user_profile_id= request.query_params.get('user_profile')
   
    manager_concern_choice = ManagerRaiseConcern.objects.filter(user_profile=user_profile_id).values()
    
    for manager_concern in manager_concern_choice:
        
        if manager_concern['action_owner_id']==1:
            admin_user = User.objects.filter(id=manager_concern['action_owner_id'],is_superuser=1).first()
            action_owner_name = admin_user.first_name +" "+ admin_user.last_name 
        else:            
            admin_user_org = Organiztaion.objects.filter(id=manager_concern['action_owner_id']).first()
            action_owner_name = admin_user_org.organization_name

        # user_profile = UserProfile.objects.filter(id=data['action_owner_id']).first()
        # user = User.objects.filter(id=manager_concern['action_owner_id']).first()

        manager_concern['action_owner_name'] = action_owner_name

    context = {}
    context['manager_concern_category']    = manager_concern_choice
    context['message']       = 'manager_concern_Category data has been received successfully'
    # context['response_code'] = HTTP_200_OK
    return Response(context,status=status.HTTP_200_OK)







# Josh Reason Type
 
@api_view(['GET'])
@authenticate_token
def manager_josh_reason_type(request):

    try:
        Customer_reason=ManagerReasonType.objects.all()
    except:
        return Response({'Msg':'Data Not Found'})
    
    serializer=ManagerReasonTypeSerializers(Customer_reason,many=True)
    return Response(data={'Manager_reason_type':serializer.data,'response_code':200},status=status.HTTP_200_OK)






@csrf_exempt
@api_view(["POST"])
@authenticate_token
def end_challenge_by_manager(request):
    if request.data.get("user_id") == '' or request.data.get("user_id") is None:  
        return Response({'message': 'Please provide user id', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST) 

    if request.data.get("challenge_id") == '' or request.data.get("challenge_id") is None:  
        return Response({'message': 'Please provide challenge id', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST) 

    if request.data.get("is_completed_by_manager") == '' or request.data.get("is_completed_by_manager") is None:  
        return Response({'message': 'Please provide is completed by manager id', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST) 

    if request.data.get("updated_end_time") == '' or request.data.get("updated_end_time") is None:  
        return Response({'message': 'Please provide updated end time', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST) 

    if request.data.get("end_challenge_time") == '' or request.data.get("end_challenge_time") is None:  
        return Response({'message': 'Please provide end challenge time', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST) 


    team_challenge = TeamChallenge.objects.filter(id=request.data.get("challenge_id")).first()
    team_challenge.is_completed_by_manager = request.data.get("is_completed_by_manager")
    team_challenge.end_time = request.data.get("end_challenge_time")
    team_challenge.end_challenge_time = request.data.get("end_challenge_time") # sent 1 minute increment

    team_challenge.save()
    
    context = {}
    context['message']= 'Challenge has been ended successfully' 
    context['response_code']            = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@authenticate_token
def end_campaign_by_manager(request):
    if request.data.get("user_id") == '' or request.data.get("user_id") is None:  
        return Response({'message': 'Please provide user id', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST) 

    if request.data.get("campaign_id") == '' or request.data.get("campaign_id") is None:  
        return Response({'message': 'Please provide campaign id', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST) 

    if request.data.get("is_completed_by_manager") == '' or request.data.get("is_completed_by_manager") is None:  
        return Response({'message': 'Please provide is completed by manager id', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST) 

    if request.data.get("updated_end_date") == '' or request.data.get("updated_end_date") is None:  
        return Response({'message': 'Please provide updated end date', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST) 

    current_time=datetime.now().strftime('%H:%M:%S')
        
    team_campaign = TeamCampaign.objects.filter(id=request.data.get("campaign_id")).first()
    team_campaign.is_completed_by_manager = request.data.get("is_completed_by_manager")
    team_campaign.end_date = request.data.get("updated_end_date")

    end_datee = datetime.strptime(request.data.get("updated_end_date"),"%Y-%m-%d").date()

    team_campaign.end_campaign_date = end_datee

    team_campaign.end_campaign_time = current_time

    team_campaign.save()
        
    
    context = {}
    context['message']= 'Campaign has been ended successfully' 
    context['response_code']            = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@authenticate_token
def todays_challenge_count(request):
    if request.data.get("manager_id") == '' or request.data.get("manager_id") is None:  
        return Response({'message': 'Please provide manager id', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST) 

    current_date=datetime.now().date()

    team_challenge_count = TeamChallenge.objects.filter(manager__id=request.data.get("manager_id"),updated_at_icontains=current_date,is_broadcasted=1,is_accepted=1,is_completed_by_customer=0).count()
    team_challenge_won_count = TeamChallenge.objects.filter(manager__id=request.data.get("manager_id"),updated_at_icontains=current_date,is_broadcasted=1,is_accepted=1,is_completed_by_customer=1).count()
            
    context = {}
    context['today_customer_accepted']  = team_challenge_count
    context['today_customer_won']       = team_challenge_won_count
    context['message']                  = 'Todays challenge count has been received successfully' 
    context['response_code']            = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)






@csrf_exempt
@api_view(["POST"])
@authenticate_token
def team_lists(request):
    if request.data.get("manager_id") == '' or request.data.get("manager_id") is None:  
        return Response({'message': 'Please provide manager id', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST) 

    if request.data.get("team_id") == '' or request.data.get("team_id") is None:  
        return Response({'message': 'Please provide team id', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST) 

    if request.data.get("unique_code") == '' or request.data.get("unique_code") is None:  
        return Response({'message': 'Please provide unique code', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST) 

 
  
    employees_data = UserProfile.objects.filter(team_id=request.data.get("team_id"),role__id=1)

    organization = Organiztaion.objects.values('id','organization_name','address').filter(unique_code=request.data.get("unique_code")).first()
    if organization:
        try:
            manager_team = Manager.objects.get(team__id=request.data.get("team_id"))
        except Exception as e:
            manager_team = None

        if manager_team:    
            organization['team_name']    = manager_team.team.team_name
        else:
            organization['team_name']    = ""


        user_profile = UserProfile.objects.filter(id=request.data.get("manager_id")).first()    
    
        organization['manager_name'] = user_profile.user.first_name +" "+user_profile.user.last_name
        
        teams_data = []
        if employees_data:
            for employee in employees_data:
                data = {}
                data['id']               = employee.id
                data['employee_name']    = employee.user.first_name +" "+employee.user.last_name
                data['designation']      = employee.designation
                data['email']            = employee.user.email
                data['mobile_no']        = employee.mobile_no
                data['role_id']          = employee.role.id
                data['role_name']        = employee.role.role_name
                if employee.last_active_on:
                    data['last_active_on']   = employee.last_active_on.strftime("%d/%m/%Y %I:%M:%S")
                else:
                    data['last_active_on']   = "-"
                teams_data.append(data)
                organization['teams_data'] = teams_data
        else:
            organization = {}        
             

            
    context = {}
    context['teams_data']               = organization
    context['message']                  = 'Team data has been received successfully' 
    context['response_code']            = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)


# used for listing top 10 employees data

@csrf_exempt
@api_view(["POST"])
@authenticate_token
def team_leaderboard(request):
    if request.data.get("manager_id") == '' or request.data.get("manager_id") is None:  
        return Response({'message': 'Please provide manager id', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST) 
    
    current_date   = date.today()
    
    teams_reward_data = MyRewardPoint.objects.values_list('user_profile__id',flat=True).filter(manager_id=request.data.get("manager_id"))
    employee_sum_data = {}

    team_points_data = []

    for employee_id in set(teams_reward_data):
        single_employee = MyRewardPoint.objects.filter(user_profile__id=employee_id).aggregate(Sum('earned_point'))
        employee_sum_data[employee_id]= single_employee['earned_point__sum']
        
    data = {k: v for k, v in sorted(employee_sum_data.items(), key=lambda employee_sum_data: employee_sum_data[1],reverse=True)[:10]}

    for key,value in data.items():
        user_profile = UserProfile.objects.filter(id=int(key)).first()
          
        team_points_data.append({key:value})
    
    team_data = [] 

    for data in team_points_data:
        dict_data = {}

        key = list(data.keys())[0]
       
        value = list(data.values())[0]

        user_profile = UserProfile.objects.filter(id=int(key)).first()
    
        dict_data['user_profile_id'] = user_profile.id
        dict_data['points']          = value
        dict_data['employee_name']   = user_profile.user.first_name+" "+user_profile.user.last_name
        dict_data["email"]           = user_profile.user.email

        team_data.append(dict_data) 

    context = {}
    context['message']                  = 'Team point data has been received successfully'
    context['data']                     = team_data
    context['response_code']            = HTTP_200_OK   
    return Response(context, status=HTTP_200_OK)




@csrf_exempt
@api_view(["POST"])
@authenticate_token
def team_employee_lists(request):
    if request.data.get("manager_id") == '' or request.data.get("manager_id") is None:  
        return Response({'message': 'Please provide manager id', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST) 

    try:    
        manager_profile = UserProfile.objects.get(id=request.data.get("manager_id"))
    except Exception as e:
        manager_profile = None

    employees = UserProfile.objects.values('id','user__first_name','user__last_name','role__id','role__role_name').filter(team_id=manager_profile.team_id,role__id=1)

    context = {}
    context['employees']                = employees
    context['message']                  = 'Team employees have been received successfully' 
    context['response_code']            = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)


# Pagination
def pagination(page,data):

    # pagination code start
    if page is None or page == "":
        page = 1
    else:
        page=page    

    paginator = Paginator(data, 10)
    try:
        team_points = paginator.page(page)
    except PageNotAnInteger:
        team_points = paginator.page(1)
    except EmptyPage:
        team_points = paginator.page(paginator.num_pages)
        
    if team_points.has_next():
        next_page = retailers.next_page_number()
    else :
        next_page = paginator.num_pages
    if team_points.has_previous():
        previous_page = retailers.previous_page_number()
    else :
        previous_page = 1
    
    page_dict={}

    page_dict['team_points_data']=team_points
    page_dict['total_pages'] = paginator.num_pages
    page_dict['next_page'] = next_page
    page_dict['previous_page'] = previous_page
    # pagination code end
    return page_dict



@csrf_exempt
@api_view(["POST"])
@authenticate_token
def team_leaderboard_filter(request):
    if request.data.get("manager_id") == '' or request.data.get("manager_id") is None:  
        return Response({'message': 'Please provide manager id', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST) 

    if request.data.get("team_id") == '' or request.data.get("team_id") is None:  
        return Response({'message': 'Please provide team id', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST) 

    
    group_all       = request.data.get('group_all')
    select_name_all = request.data.get('select_name_all')
    time_period_all = request.data.get('time_period_all')
    
    context = {}

    current_date   = date.today()
    
    team_points_data = []

    user_profile_ids = UserProfile.objects.filter(team_id=request.data.get("team_id"),role__id=1).values_list('id',flat=True)

    employee_profile = UserProfile.objects.filter(team_id=request.data.get("team_id"),role__id=1)

    end_user_count = UserProfile.objects.filter(team_id=request.data.get("team_id"),role__id=1).count()
    
   
    if group_all=="group_all" and select_name_all=="select_name_all" and time_period_all=="time_period_all":
        # if request.data.get("page_no") == '' or request.data.get("page_no") is None:  
        #     return Response({'message': 'Page no field is required', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST) 

        # page_no = request.data.get("page_no")

        # page_limit  = int(request.data.get("page_no"))*10
        # offset      = int(page_limit)-10
        # page_limit  = 10
 
        # teams_reward_count = MyRewardPoint.objects.values().filter(user_profile__team_id=request.data.get("team_id")).order_by('-id').count()
        
        # teams_reward       = MyRewardPoint.objects.values().filter(user_profile__team_id=request.data.get("team_id")).order_by('-id')
        
     
        for employee in employee_profile:
            if MyRewardPoint.objects.values().filter(user_profile__id=employee.id).exists():

                teams = {}
                teams['first_name'] = employee.user.first_name
                teams['last_name']  = employee.user.last_name
        
                teams_reward        = MyRewardPoint.objects.filter(user_profile__id=employee.id).aggregate(Sum('earned_point'))['earned_point__sum']

                teams['earned_point']     = teams_reward 

                team_points_data.append(teams) 
   
    elif group_all=="group_all" and select_name_all=="select_name_all" and time_period_all=="today":

        # teams_reward = MyRewardPoint.objects.values().filter(user_profile__team_id=request.data.get("team_id"),created_at__icontains=current_date).order_by('-id')
    
        # for data in teams_reward:
        #     user_profile = UserProfile.objects.filter(id=int(data['user_profile_id'])).first()
        #     data['first_name'] = user_profile.user.first_name
        #     data['last_name']  = user_profile.user.last_name  
        #     team_points_data.append(data)

        for employee in employee_profile:
            if MyRewardPoint.objects.values().filter(user_profile__id=employee.id,created_at__icontains=current_date).exists():

                teams = {}
                teams['first_name'] = employee.user.first_name
                teams['last_name']  = employee.user.last_name
        
                teams_reward        = MyRewardPoint.objects.filter(user_profile__id=employee.id,created_at__icontains=current_date).aggregate(Sum('earned_point'))['earned_point__sum']

                teams['earned_point']     = teams_reward 

                team_points_data.append(teams) 


    elif group_all=="group_all" and select_name_all=="select_name_all" and time_period_all=="yesterday":
        yesterday_date = current_date-timedelta(days=1)
        
        # teams_reward = MyRewardPoint.objects.values().filter(user_profile__team_id=request.data.get("team_id"),created_at__icontains=yesterday_date).order_by('-id')
    
        # for data in teams_reward:
        #     user_profile = UserProfile.objects.filter(id=int(data['user_profile_id'])).first()
        #     data['first_name'] = user_profile.user.first_name
        #     data['last_name']  = user_profile.user.last_name  
        #     team_points_data.append(data)

        for employee in employee_profile:
            if MyRewardPoint.objects.values().filter(user_profile__id=employee.id,created_at__icontains=yesterday_date).exists():

                teams = {}
                teams['first_name'] = employee.user.first_name
                teams['last_name']  = employee.user.last_name
        
                teams_reward        = MyRewardPoint.objects.filter(user_profile__id=employee.id,created_at__icontains=yesterday_date).aggregate(Sum('earned_point'))['earned_point__sum']

                teams['earned_point']     = teams_reward 

                team_points_data.append(teams) 


    elif group_all=="group_all" and select_name_all=="select_name_all" and time_period_all=="wtd":
        end_date   = current_date
        start_date = end_date -timedelta(days=7)

        # teams_reward = MyRewardPoint.objects.values().filter(user_profile__team_id=request.data.get("team_id"),created_at__date__range=[start_date,end_date]).order_by('-id')
        
        # for data in teams_reward:
        #     user_profile = UserProfile.objects.filter(id=int(data['user_profile_id'])).first()
        #     data['first_name'] = user_profile.user.first_name
        #     data['last_name']  = user_profile.user.last_name  
        #     team_points_data.append(data)

        for employee in employee_profile:
            if MyRewardPoint.objects.values().filter(user_profile__id=employee.id,created_at__date__range=[start_date,end_date]).exists():

                teams = {}
                teams['first_name'] = employee.user.first_name
                teams['last_name']  = employee.user.last_name
        
                teams_reward        = MyRewardPoint.objects.filter(user_profile__id=employee.id,created_at__date__range=[start_date,end_date]).aggregate(Sum('earned_point'))['earned_point__sum']

                teams['earned_point']     = teams_reward 

                team_points_data.append(teams) 




    elif group_all=="group_all" and select_name_all=="select_name_all" and time_period_all=="mtd":
        month = current_date.month
        year = current_date.year
        
        # teams_reward = MyRewardPoint.objects.values().filter(user_profile__team_id=request.data.get("team_id"),created_at__month=month,created_at__year=year).order_by('-id')
    
        # for data in teams_reward:
        #     user_profile = UserProfile.objects.filter(id=int(data['user_profile_id'])).first()
        #     data['first_name'] = user_profile.user.first_name
        #     data['last_name']  = user_profile.user.last_name  
        #     team_points_data.append(data)

        for employee in employee_profile:
            if MyRewardPoint.objects.values().filter(user_profile__id=employee.id,created_at__month=month,created_at__year=year).exists():

                teams = {}
                teams['first_name'] = employee.user.first_name
                teams['last_name']  = employee.user.last_name
        
                teams_reward        = MyRewardPoint.objects.filter(user_profile__id=employee.id,created_at__month=month,created_at__year=year).aggregate(Sum('earned_point'))['earned_point__sum']

                teams['earned_point']     = teams_reward 

                team_points_data.append(teams) 


    elif group_all=="group_all" and select_name_all=="select_name_all" and time_period_all=="ytd":
        year = current_date.year
        
        # teams_reward = MyRewardPoint.objects.values().filter(user_profile__team_id=request.data.get("team_id"),created_at__year=year).order_by('-id')
    
        # for data in teams_reward:
        #     user_profile = UserProfile.objects.filter(id=int(data['user_profile_id'])).first()
        #     data['first_name'] = user_profile.user.first_name
        #     data['last_name']  = user_profile.user.last_name  
        #     team_points_data.append(data)

        for employee in employee_profile:
            if MyRewardPoint.objects.values().filter(user_profile__id=employee.id,created_at__year=year).exists():

                teams = {}
                teams['first_name'] = employee.user.first_name
                teams['last_name']  = employee.user.last_name
        
                teams_reward        = MyRewardPoint.objects.filter(user_profile__id=employee.id,created_at__year=year).aggregate(Sum('earned_point'))['earned_point__sum']

                teams['earned_point']     = teams_reward 

                team_points_data.append(teams) 
    

    elif group_all=="top_10" and select_name_all=="select_name_all" and time_period_all=="time_period_all":
        teams_reward_data = MyRewardPoint.objects.filter(user_profile__team_id=request.data.get("team_id"))
        employee_sum_data = {}
    
        for employee_id in user_profile_ids:
            single_employee = teams_reward_data.filter(user_profile__id=employee_id).aggregate(Sum('earned_point'))
            employee_sum_data[employee_id]= single_employee['earned_point__sum']
            
        data = {k: v for k, v in sorted(employee_sum_data.items(), key=lambda employee_sum_data: employee_sum_data[1],reverse=True)[:10]}

        for key,value in data.items():
            user_profile = UserProfile.objects.filter(id=int(key)).first()

            team_points_data.append({key:value,'user_profile_id':user_profile.id,'earned_point':value,'employee_name':user_profile.user.first_name+" "+user_profile.user.last_name,'first_name':user_profile.user.first_name,'last_name':user_profile.user.last_name,"email":user_profile.user.email})

    
    elif group_all=="top_10" and select_name_all=="select_name_all" and time_period_all=="today":
        teams_reward_data = MyRewardPoint.objects.filter(user_profile__team_id=request.data.get("team_id"),created_at__icontains=current_date)
        employee_sum_data = {}

        
        for employee_id in user_profile_ids:
            single_employee = teams_reward_data.filter(user_profile__id=employee_id).aggregate(Sum('earned_point'))
            employee_sum_data[employee_id]= single_employee['earned_point__sum']
            
        data = {k: v for k, v in sorted(employee_sum_data.items(), key=lambda employee_sum_data: employee_sum_data[1],reverse=True)[:10]}

        for key,value in data.items():
            user_profile = UserProfile.objects.filter(id=int(key)).first()

            team_points_data.append({key:value,'user_profile_id':user_profile.id,'earned_point':value,'employee_name':user_profile.user.first_name+" "+user_profile.user.last_name,'first_name':user_profile.user.first_name,'last_name':user_profile.user.last_name,"email":user_profile.user.email})
          
    elif group_all=="top_10" and select_name_all=="select_name_all" and time_period_all=="yesterday":
        yesterday_date = current_date-timedelta(days=1)
        teams_reward_data = MyRewardPoint.objects.filter(user_profile__team_id=request.data.get("team_id"),created_at__icontains=yesterday_date)
        employee_sum_data = {}

        for employee_id in user_profile_ids:
            single_employee = teams_reward_data.filter(user_profile__id=employee_id).aggregate(Sum('earned_point'))
            employee_sum_data[employee_id]= single_employee['earned_point__sum']
            
        data = {k: v for k, v in sorted(employee_sum_data.items(), key=lambda employee_sum_data: employee_sum_data[1],reverse=True)[:10]}

        for key,value in data.items():
            user_profile = UserProfile.objects.filter(id=int(key)).first()

            team_points_data.append({key:value,'user_profile_id':user_profile.id,'earned_point':value,'employee_name':user_profile.user.first_name+" "+user_profile.user.last_name,'first_name':user_profile.user.first_name,'last_name':user_profile.user.last_name,"email":user_profile.user.email})
    
    elif group_all=="top_10" and select_name_all=="select_name_all" and time_period_all=="wtd":
        end_date   = current_date
        start_date = end_date -timedelta(days=7)
        
        teams_reward_data = MyRewardPoint.objects.filter(user_profile__team_id=request.data.get("team_id"),created_at__date__range=[start_date,end_date])
        employee_sum_data = {}

        for employee_id in user_profile_ids:
            single_employee = teams_reward_data.filter(user_profile__id=employee_id).aggregate(Sum('earned_point'))
            employee_sum_data[employee_id]= single_employee['earned_point__sum']
            
        data = {k: v for k, v in sorted(employee_sum_data.items(), key=lambda employee_sum_data: employee_sum_data[1],reverse=True)[:10]}

        for key,value in data.items():
            user_profile = UserProfile.objects.filter(id=int(key)).first()

            team_points_data.append({key:value,'user_profile_id':user_profile.id,'earned_point':value,'employee_name':user_profile.user.first_name+" "+user_profile.user.last_name,'first_name':user_profile.user.first_name,'last_name':user_profile.user.last_name,"email":user_profile.user.email})
    
    
    elif group_all=="top_10" and select_name_all=="select_name_all" and time_period_all=="mtd":
        month = current_date.month
        year = current_date.year
        
        teams_reward_data = MyRewardPoint.objects.filter(user_profile__team_id=request.data.get("team_id"),created_at__date__month=month,created_at__date__year=year)
        employee_sum_data = {}

        for employee_id in user_profile_ids:
            single_employee = teams_reward_data.filter(user_profile__id=employee_id).aggregate(Sum('earned_point'))
            employee_sum_data[employee_id]= single_employee['earned_point__sum']
            
        data = {k: v for k, v in sorted(employee_sum_data.items(), key=lambda employee_sum_data: employee_sum_data[1],reverse=True)[:10]}

        for key,value in data.items():
            user_profile = UserProfile.objects.filter(id=int(key)).first()

            team_points_data.append({key:value,'user_profile_id':user_profile.id,'earned_point':value,'employee_name':user_profile.user.first_name+" "+user_profile.user.last_name,'first_name':user_profile.user.first_name,'last_name':user_profile.user.last_name,"email":user_profile.user.email})
    
    elif group_all=="top_10" and select_name_all=="select_name_all" and time_period_all=="ytd":
        year = current_date.year
        
        teams_reward_data = MyRewardPoint.objects.filter(user_profile__team_id=request.data.get("team_id"),created_at__date__year=year)
        employee_sum_data = {}

        for employee_id in user_profile_ids:
            single_employee = teams_reward_data.filter(user_profile__id=employee_id).aggregate(Sum('earned_point'))
            employee_sum_data[employee_id]= single_employee['earned_point__sum']
            
        data = {k: v for k, v in sorted(employee_sum_data.items(), key=lambda employee_sum_data: employee_sum_data[1],reverse=True)[:10]}

        for key,value in data.items():
            user_profile = UserProfile.objects.filter(id=int(key)).first()

            team_points_data.append({key:value,'user_profile_id':user_profile.id,'earned_point':value,'employee_name':user_profile.user.first_name+" "+user_profile.user.last_name,'first_name':user_profile.user.first_name,'last_name':user_profile.user.last_name,"email":user_profile.user.email})
    

    elif group_all=="bottom_10" and select_name_all=="select_name_all" and time_period_all=="time_period_all":
        teams_reward_data = MyRewardPoint.objects.filter(user_profile__team_id=request.data.get("team_id"))
        employee_sum_data = {}

        for employee_id in user_profile_ids:
            single_employee = teams_reward_data.filter(user_profile__id=employee_id).aggregate(Sum('earned_point'))
            employee_sum_data[employee_id]= single_employee['earned_point__sum']
            
        data = {k: v for k, v in sorted(employee_sum_data.items(), key=lambda employee_sum_data: employee_sum_data[1],reverse=False)[:10]}

        user_count = 0
        
        for key,value in data.items():
            user_profile = UserProfile.objects.filter(id=int(key)).first()
            
            user_count +=1

            team_points_data.append({key:value,'user_profile_id':user_profile.id,'earned_point':value,'employee_name':user_profile.user.first_name+" "+user_profile.user.last_name,'first_name':user_profile.user.first_name,'last_name':user_profile.user.last_name,"email":user_profile.user.email})
        
    elif group_all=="bottom_10" and select_name_all=="select_name_all" and time_period_all=="today":
        teams_reward_data = MyRewardPoint.objects.filter(user_profile__team_id=request.data.get("team_id"),created_at__icontains=current_date)
        employee_sum_data = {}

        for employee_id in user_profile_ids:
            single_employee = teams_reward_data.filter(user_profile__id=employee_id).aggregate(Sum('earned_point'))
            employee_sum_data[employee_id]= single_employee['earned_point__sum']
            
        data = {k: v for k, v in sorted(employee_sum_data.items(), key=lambda employee_sum_data: employee_sum_data[1],reverse=False)[:10]}

        for key,value in data.items():
            user_profile = UserProfile.objects.filter(id=int(key)).first()

            team_points_data.append({key:value,'user_profile_id':user_profile.id,'earned_point':value,'employee_name':user_profile.user.first_name+" "+user_profile.user.last_name,'first_name':user_profile.user.first_name,'last_name':user_profile.user.last_name,"email":user_profile.user.email})

    elif group_all=="bottom_10" and select_name_all=="select_name_all" and time_period_all=="yesterday":
        yesterday_date = current_date-timedelta(days=1)

        teams_reward_data = MyRewardPoint.objects.filter(user_profile__team_id=request.data.get("team_id"),created_at__icontains=yesterday_date)
        employee_sum_data = {}

        for employee_id in user_profile_ids:
            single_employee = teams_reward_data.filter(user_profile__id=employee_id).aggregate(Sum('earned_point'))
            employee_sum_data[employee_id]= single_employee['earned_point__sum']
            
        data = {k: v for k, v in sorted(employee_sum_data.items(), key=lambda employee_sum_data: employee_sum_data[1],reverse=False)[:10]}

        for key,value in data.items():
            user_profile = UserProfile.objects.filter(id=int(key)).first()

            team_points_data.append({key:value,'user_profile_id':user_profile.id,'earned_point':value,'employee_name':user_profile.user.first_name+" "+user_profile.user.last_name,'first_name':user_profile.user.first_name,'last_name':user_profile.user.last_name,"email":user_profile.user.email})
    elif group_all=="bottom_10" and select_name_all=="select_name_all" and time_period_all=="wtd":
        end_date   = current_date
        start_date = end_date -timedelta(days=7)
        
        teams_reward_data = MyRewardPoint.objects.filter(user_profile__team_id=request.data.get("team_id"),created_at__date__range=[start_date,end_date])
        employee_sum_data = {}

        for employee_id in user_profile_ids:
            single_employee = teams_reward_data.filter(user_profile__id=employee_id).aggregate(Sum('earned_point'))
            employee_sum_data[employee_id]= single_employee['earned_point__sum']
            
        data = {k: v for k, v in sorted(employee_sum_data.items(), key=lambda employee_sum_data: employee_sum_data[1],reverse=False)[:10]}

        for key,value in data.items():
            user_profile = UserProfile.objects.filter(id=int(key)).first()

            team_points_data.append({key:value,'user_profile_id':user_profile.id,'earned_point':value,'employee_name':user_profile.user.first_name+" "+user_profile.user.last_name,'first_name':user_profile.user.first_name,'last_name':user_profile.user.last_name,"email":user_profile.user.email})
    elif group_all=="bottom_10" and select_name_all=="select_name_all" and time_period_all=="mtd":
        month = current_date.month
        year = current_date.year
        teams_reward_data = MyRewardPoint.objects.filter(user_profile__team_id=request.data.get("team_id"),created_at__month=month,created_at__year=year)
        employee_sum_data = {}

        for employee_id in user_profile_ids:
            single_employee = teams_reward_data.filter(user_profile__id=employee_id).aggregate(Sum('earned_point'))
            employee_sum_data[employee_id]= single_employee['earned_point__sum']
            
        data = {k: v for k, v in sorted(employee_sum_data.items(), key=lambda employee_sum_data: employee_sum_data[1],reverse=False)[:10]}

        for key,value in data.items():
            user_profile = UserProfile.objects.filter(id=int(key)).first()

            team_points_data.append({key:value,'user_profile_id':user_profile.id,'earned_point':value,'employee_name':user_profile.user.first_name+" "+user_profile.user.last_name,'first_name':user_profile.user.first_name,'last_name':user_profile.user.last_name,"email":user_profile.user.email})

    elif group_all=="bottom_10" and select_name_all=="select_name_all" and time_period_all=="ytd":
        year = current_date.year
        teams_reward_data = MyRewardPoint.objects.filter(user_profile__team_id=request.data.get("team_id"),created_at__year=year)
        employee_sum_data = {}

        for employee_id in user_profile_ids:
            single_employee = teams_reward_data.filter(user_profile__id=employee_id).aggregate(Sum('earned_point'))
            employee_sum_data[employee_id]= single_employee['earned_point__sum']
            
        data = {k: v for k, v in sorted(employee_sum_data.items(), key=lambda employee_sum_data: employee_sum_data[1],reverse=False)[:10]}

        for key,value in data.items():
            user_profile = UserProfile.objects.filter(id=int(key)).first()

            team_points_data.append({key:value,'user_profile_id':user_profile.id,'earned_point':value,'employee_name':user_profile.user.first_name+" "+user_profile.user.last_name,'first_name':user_profile.user.first_name,'last_name':user_profile.user.last_name,"email":user_profile.user.email})
    elif select_name_all!="select_name_all" and group_all=="group_all" and time_period_all=="time_period_all":
        
        if MyRewardPoint.objects.values().filter(user_profile__team_id=request.data.get("team_id"),user_profile__id=select_name_all).exists():
                 
            teams_reward       = MyRewardPoint.objects.filter(user_profile__team_id=request.data.get("team_id"),user_profile__id=select_name_all).aggregate(Sum('earned_point'))['earned_point__sum']

            employee_one = UserProfile.objects.filter(id=select_name_all).first()

            data   = {}   
            data['first_name'] = employee_one.user.first_name
            data['last_name']  = employee_one.user.last_name
            data['earned_point'] =  teams_reward
            team_points_data.append(data)

    elif select_name_all!="select_name_all" and group_all=="group_all" and time_period_all=="today":
        # teams_reward       = MyRewardPoint.objects.values().filter(user_profile__team_id=request.data.get("team_id"),user_profile__id=select_name_all,created_at__icontains=current_date).order_by('-id')

        # for data in teams_reward:
        #     user_profile = UserProfile.objects.filter(id=int(data['user_profile_id'])).first()
        #     data['first_name'] = user_profile.user.first_name
        #     data['last_name']  = user_profile.user.last_name  
        #     team_points_data.append(data)


        if MyRewardPoint.objects.values().filter(user_profile__team_id=request.data.get("team_id"),user_profile__id=select_name_all,created_at__icontains=current_date).exists():
                 
            teams_reward       = MyRewardPoint.objects.filter(user_profile__team_id=request.data.get("team_id"),user_profile__id=select_name_all,created_at__icontains=current_date).aggregate(Sum('earned_point'))['earned_point__sum']

            employee_one = UserProfile.objects.filter(id=select_name_all).first()

            data   = {}   
            data['first_name'] = employee_one.user.first_name
            data['last_name']  = employee_one.user.last_name
            data['earned_point'] = teams_reward  
            team_points_data.append(data)    
    elif select_name_all!="select_name_all" and group_all=="group_all" and time_period_all=="yesterday":
        yesterday_date = current_date-timedelta(days=1)
    
        # teams_reward       = MyRewardPoint.objects.values().filter(user_profile__team_id=request.data.get("team_id"),user_profile__id=select_name_all,created_at__icontains=yesterday_date).order_by('-id')

        # for data in teams_reward:
        #     user_profile = UserProfile.objects.filter(id=int(data['user_profile_id'])).first()
        #     data['first_name'] = user_profile.user.first_name
        #     data['last_name']  = user_profile.user.last_name  
        #     team_points_data.append(data)


        if MyRewardPoint.objects.values().filter(user_profile__team_id=request.data.get("team_id"),user_profile__id=select_name_all,created_at__icontains=yesterday_date).exists():
                 
            teams_reward       = MyRewardPoint.objects.filter(user_profile__team_id=request.data.get("team_id"),user_profile__id=select_name_all,created_at__icontains=yesterday_date).aggregate(Sum('earned_point'))['earned_point__sum']

            employee_one = UserProfile.objects.filter(id=select_name_all).first()

            data   = {}   
            data['first_name'] = employee_one.user.first_name
            data['last_name']  = employee_one.user.last_name
            data['earned_point'] = teams_reward   
            team_points_data.append(data)

    elif select_name_all!="select_name_all" and group_all=="group_all" and time_period_all=="wtd":
        end_date   = current_date
        start_date = end_date -timedelta(days=7)

        # teams_reward = MyRewardPoint.objects.values().filter(user_profile__id=select_name_all,user_profile__team_id=request.data.get("team_id"),created_at__date__range=[start_date,end_date]).order_by('-id')
        
        # for data in teams_reward:
        #     user_profile = UserProfile.objects.filter(id=int(data['user_profile_id'])).first()
        #     data['first_name'] = user_profile.user.first_name
        #     data['last_name']  = user_profile.user.last_name  
        #     team_points_data.append(data)

        if MyRewardPoint.objects.values().filter(user_profile__team_id=request.data.get("team_id"),user_profile__id=select_name_all,created_at__date__range=[start_date,end_date]).exists():
                 
            teams_reward       = MyRewardPoint.objects.filter(user_profile__team_id=request.data.get("team_id"),user_profile__id=select_name_all,created_at__date__range=[start_date,end_date]).aggregate(Sum('earned_point'))['earned_point__sum']

            employee_one = UserProfile.objects.filter(id=select_name_all).first()

            data   = {}   
            data['first_name'] = employee_one.user.first_name
            data['last_name']  = employee_one.user.last_name
            data['earned_point'] = teams_reward   
            team_points_data.append(data)

    elif select_name_all!="select_name_all" and group_all=="group_all" and time_period_all=="mtd":
        month = current_date.month
        year = current_date.year
        
        # teams_reward = MyRewardPoint.objects.values().filter(user_profile__id=select_name_all,user_profile__team_id=request.data.get("team_id"),created_at__month=month,created_at__year=year).order_by('-id')
    
        # for data in teams_reward:
        #     user_profile = UserProfile.objects.filter(id=int(data['user_profile_id'])).first()
        #     data['first_name'] = user_profile.user.first_name
        #     data['last_name']  = user_profile.user.last_name  
        #     team_points_data.append(data)

        if MyRewardPoint.objects.values().filter(user_profile__team_id=request.data.get("team_id"),user_profile__id=select_name_all,created_at__month=month,created_at__year=year).exists():
                 
            teams_reward       = MyRewardPoint.objects.filter(user_profile__team_id=request.data.get("team_id"),user_profile__id=select_name_all,created_at__month=month,created_at__year=year).aggregate(Sum('earned_point'))['earned_point__sum']

            employee_one = UserProfile.objects.filter(id=select_name_all).first()

            data   = {}   
            data['first_name'] = employee_one.user.first_name
            data['last_name']  = employee_one.user.last_name
            data['earned_point'] = teams_reward   
            team_points_data.append(data)
    
    elif select_name_all!="select_name_all" and group_all=="group_all" and time_period_all=="ytd":
        year = current_date.year
        
        # teams_reward = MyRewardPoint.objects.values().filter(user_profile__id=select_name_all,user_profile__team_id=request.data.get("team_id"),created_at__year=year).order_by('-id')
    
        # for data in teams_reward:
        #     user_profile = UserProfile.objects.filter(id=int(data['user_profile_id'])).first()
        #     data['first_name'] = user_profile.user.first_name
        #     data['last_name']  = user_profile.user.last_name  
        #     team_points_data.append(data)

        
        if MyRewardPoint.objects.values().filter(user_profile__team_id=request.data.get("team_id"),user_profile__id=select_name_all,created_at__year=year).exists():
                 
            teams_reward       = MyRewardPoint.objects.filter(user_profile__team_id=request.data.get("team_id"),user_profile__id=select_name_all,created_at__year=year).aggregate(Sum('earned_point'))['earned_point__sum']

            employee_one = UserProfile.objects.filter(id=select_name_all).first()

            data   = {}   
            data['first_name'] = employee_one.user.first_name
            data['last_name']  = employee_one.user.last_name
            data['earned_point'] = teams_reward   
            team_points_data.append(data)

  
    context['team_points_data']         = team_points_data

    context['message']                  = 'Team points have been filtered successfully' 
    context['response_code']            = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)





@csrf_exempt
@api_view(["POST"])
@authenticate_token
def team_mood_for_today(request):
    if request.data.get("manager_id") == '' or request.data.get("manager_id") is None:  
        return Response({'message': 'Please provide manager id', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST) 

    if request.data.get("team_id") == '' or request.data.get("team_id") is None:  
        return Response({'message': 'Please provide team id', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST) 

    current_date   = date.today()

    total_team_count  = UserProfile.objects.values().filter(team_id=request.data.get("team_id"),role__id=1).count()

    team_josh_count  = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__icontains=current_date).count()
    
    if not team_josh_count:
        team_josh_count = 1
    else:
        team_josh_count = team_josh_count

    if team_josh_count:
        
        team_josh  = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__icontains=current_date)

        team_josh_sum  = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__icontains=current_date).aggregate(Sum('emoji_point'))['emoji_point__sum']

        # Today average points  
        team_josh_count_one = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__icontains=current_date,emoji_point=1).count()
        
        team_josh_count_one_percent = round((team_josh_count_one *100)/team_josh_count,2)  

        team_josh_count_two = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__icontains=current_date,emoji_point=2).count()
        team_josh_count_two_percent = round((team_josh_count_two * 100)/team_josh_count,2)  

        team_josh_count_three = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__icontains=current_date,emoji_point=3).count()
        team_josh_count_three_percent = round((team_josh_count_three * 100)/team_josh_count,2)  

        team_josh_count_four = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__icontains=current_date,emoji_point=4).count()
        team_josh_count_four_percent = round((team_josh_count_four * 100)/team_josh_count,2)  

        team_josh_count_five = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__icontains=current_date,emoji_point=5).count()
        team_josh_count_five_percent = round((team_josh_count_five * 100)/team_josh_count,2)  


        # Yesterday Average Points
        current_date = date.today()
        yesterday = current_date - timedelta(days=1)

        team_josh_count_one_yesterday = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__icontains=yesterday,emoji_point=1).count()
        team_josh_count_one_percent_yesterday = round((team_josh_count_one_yesterday * 100)/team_josh_count,2)  

        team_josh_count_two_yesterday = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__icontains=yesterday,emoji_point=2).count()
        team_josh_count_two_percent_yesterday = round((team_josh_count_two_yesterday * 100)/team_josh_count,2)  

        team_josh_count_three_yesterday = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__icontains=yesterday,emoji_point=3).count()
        team_josh_count_three_percent_yesterday = round((team_josh_count_three_yesterday * 100)/team_josh_count,2)  

        team_josh_count_four_yesterday = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__icontains=yesterday,emoji_point=4).count()
        team_josh_count_four_percent_yesterday = round((team_josh_count_four_yesterday * 100)/team_josh_count,2)  

        team_josh_count_five_yesterday = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__icontains=yesterday,emoji_point=5).count()
        team_josh_count_five_percent_yesterday = round((team_josh_count_five_yesterday * 100)/team_josh_count,2)  

        # Yesterday KPI Met percent

        team_josh_employees_one_yesterday = JoshReason.objects.filter(manager_id=request.data.get("team_id"),created_at__icontains=yesterday,emoji_point=1).values_list('user_profile__user__email',flat=True)
        
        team_josh_employees_two_yesterday = JoshReason.objects.filter(manager_id=request.data.get("team_id"),created_at__icontains=yesterday,emoji_point=2).values_list('user_profile__user__email',flat=True)

        team_josh_employees_three_yesterday = JoshReason.objects.filter(manager_id=request.data.get("team_id"),created_at__icontains=yesterday,emoji_point=3).values_list('user_profile__user__email',flat=True)

        team_josh_employees_four_yesterday = JoshReason.objects.filter(manager_id=request.data.get("team_id"),created_at__icontains=yesterday,emoji_point=4).values_list('user_profile__user__email',flat=True)

        team_josh_employees_five_yesterday = JoshReason.objects.filter(manager_id=request.data.get("team_id"),created_at__icontains=yesterday,emoji_point=5).values_list('user_profile__user__email',flat=True)

        
        organization_emp_one_performance_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_josh_employees_one_yesterday,permormance_date__icontains=yesterday).aggregate(Sum('kpi_target'))
        organization_emp_one_performance_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_josh_employees_one_yesterday,permormance_date__icontains=yesterday).aggregate(Sum('kpi_actual'))
        
        if organization_emp_one_performance_target['kpi_target__sum']!=None and organization_emp_one_performance_actual['kpi_actual__sum']!=None:
            target = round(organization_emp_one_performance_target['kpi_target__sum'],2)
            actual = round(organization_emp_one_performance_actual['kpi_actual__sum'],2)

            if target<=actual:
                emp_josh_one_percent = (actual/target)*100  
            else:
                emp_josh_one_percent = 0.0
        else:
            emp_josh_one_percent = 0.0

        organization_emp_two_performance_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_josh_employees_two_yesterday,permormance_date__icontains=yesterday).aggregate(Sum('kpi_target'))
        organization_emp_two_performance_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_josh_employees_two_yesterday,permormance_date__icontains=yesterday).aggregate(Sum('kpi_actual'))

        if organization_emp_two_performance_target['kpi_target__sum']!=None and organization_emp_two_performance_actual['kpi_actual__sum']!=None:
            target = round(organization_emp_two_performance_target['kpi_target__sum'],2)
            actual = round(organization_emp_two_performance_actual['kpi_actual__sum'],2)

            if target<=actual:
                emp_josh_two_percent = (actual/target)*100  
            else:
                emp_josh_two_percent = 0.0
        else:
            emp_josh_two_percent = 0.0

        organization_emp_three_performance_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_josh_employees_three_yesterday,permormance_date__icontains=yesterday).aggregate(Sum('kpi_target'))
        organization_emp_three_performance_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_josh_employees_three_yesterday,permormance_date__icontains=yesterday).aggregate(Sum('kpi_actual'))

        if organization_emp_three_performance_target['kpi_target__sum']!=None and organization_emp_three_performance_actual['kpi_actual__sum']!=None:
            target = round(organization_emp_three_performance_target['kpi_target__sum'],2)
            actual = round(organization_emp_three_performance_actual['kpi_actual__sum'],2)

            if target<=actual:
                emp_josh_three_percent = (actual/target)*100  
            else:
                emp_josh_three_percent = 0.0
        else:
            emp_josh_three_percent = 0.0

        organization_emp_four_performance_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_josh_employees_four_yesterday,permormance_date__icontains=yesterday).aggregate(Sum('kpi_target'))
        organization_emp_four_performance_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_josh_employees_four_yesterday,permormance_date__icontains=yesterday).aggregate(Sum('kpi_actual'))

        if organization_emp_four_performance_target['kpi_target__sum']!=None and organization_emp_four_performance_actual['kpi_actual__sum']!=None:
            target = round(organization_emp_four_performance_target['kpi_target__sum'],2)
            actual = round(organization_emp_four_performance_actual['kpi_actual__sum'],2)

            if target<=actual:
                emp_josh_four_percent = (actual/target)*100  
            else:
                emp_josh_four_percent = 0.0
        else:
            emp_josh_four_percent = 0.0

        organization_emp_five_performance_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_josh_employees_five_yesterday,permormance_date__icontains=yesterday).aggregate(Sum('kpi_target'))
        organization_emp_five_performance_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_josh_employees_five_yesterday,permormance_date__icontains=yesterday).aggregate(Sum('kpi_actual'))

        if organization_emp_five_performance_target['kpi_target__sum']!=None and organization_emp_five_performance_actual['kpi_actual__sum']!=None:
            target = round(organization_emp_five_performance_target['kpi_target__sum'],2)
            actual = round(organization_emp_five_performance_actual['kpi_actual__sum'],2)

            if target<=actual:
                emp_josh_five_percent = (actual/target)*100  
            else:
                emp_josh_five_percent = 0.0
        else:
            emp_josh_five_percent = 0.0

        if not team_josh_count:
            team_josh_count = 1

        if not total_team_count:         
           total_team_count = 1

        context = {}
        context['percent_respondent_today'] = round(team_josh_count/total_team_count*100,2)
        context['avg_score_today']          = round(team_josh_sum/team_josh_count,2) 
        context['today_scores']             = {'one':team_josh_count_one_percent,'two':team_josh_count_two_percent,'three':team_josh_count_three_percent,'four':team_josh_count_four_percent,'five':team_josh_count_five_percent}
        context['yesterday_scores']         = {'one':team_josh_count_one_percent_yesterday,'two':team_josh_count_two_percent_yesterday,'three':team_josh_count_three_percent_yesterday,'four':team_josh_count_four_percent_yesterday,'five':team_josh_count_five_percent_yesterday}
        context['yesterday_kpi_met_percent']= {'one':emp_josh_one_percent,'two':emp_josh_two_percent,'three':emp_josh_three_percent,'four':emp_josh_four_percent,'five':emp_josh_five_percent}

        context['message']                  = 'Todays team mood has been received successfully' 
        context['response_code']            = 200
        return Response(context, status=HTTP_200_OK)
    else:
        context = {}
        context['message']                  = 'Todays team mood has not created yet ' 
        context['response_code']            = 201
        return Response(context, status=HTTP_200_OK)



@csrf_exempt
@api_view(["POST"])
@authenticate_token
def team_mood_for_today_filter(request):
    if request.data.get("team_id") == '' or request.data.get("team_id") is None:  
        return Response({'message': 'Please provide team id', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST) 

    if request.data.get("time_period") == '' or request.data.get("time_period") is None:  
        return Response({'message': 'Please provide time period', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST) 

    
    current_date   = date.today()

    time_period = request.data.get("time_period")

    team_employees_email = UserProfile.objects.filter(team_id=request.data.get('team_id'),role__id=1).values_list('user__email',flat=True)
    
    if time_period=="all":
        team_josh_one    = JoshReason.objects.filter(manager_id=request.data.get("team_id"),emoji_point=1).count()
        team_josh_two    = JoshReason.objects.filter(manager_id=request.data.get("team_id"),emoji_point=2).count()
        team_josh_three  = JoshReason.objects.filter(manager_id=request.data.get("team_id"),emoji_point=3).count()

        total_emp_josh_sum = team_josh_one + team_josh_two + team_josh_three
        
        if not total_emp_josh_sum:
            total_emp_josh_sum = 1 

        # pie chart

        team_josh_one_percent   = (team_josh_one*100)/total_emp_josh_sum

        team_josh_two_percent   = (team_josh_two*100)/total_emp_josh_sum

        team_josh_three_percent = (team_josh_three*100)/total_emp_josh_sum


        
        # Team mood for bar chart

        team_josh_count  = JoshReason.objects.values().filter(manager_id=request.data.get("team_id")).count()
        
        if not team_josh_count:
            team_josh_count = 1

        team_josh  = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"))

        team_josh_sum  = JoshReason.objects.values().filter(manager_id=request.data.get("team_id")).aggregate(Sum('emoji_point'))['emoji_point__sum']

        team_josh_count_one = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),emoji_point=1).count()
        team_josh_count_one_percent = round((team_josh_count_one *100)/team_josh_count,2)  

        team_josh_count_two = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),emoji_point=2).count()
        team_josh_count_two_percent = round((team_josh_count_two * 100)/team_josh_count,2)  

        team_josh_count_three = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),emoji_point=3).count()
        team_josh_count_three_percent = round((team_josh_count_three * 100)/team_josh_count,2)  

        team_josh_count_four = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),emoji_point=4).count()
        team_josh_count_four_percent = round((team_josh_count_four * 100)/team_josh_count,2)  

        team_josh_count_five = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),emoji_point=5).count()
        team_josh_count_five_percent = round((team_josh_count_five * 100)/team_josh_count,2)  


        # team kpi data based on josh for  bar chart

        organization_emp_one_performance_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email).aggregate(Sum('kpi_target'))
        organization_emp_one_performance_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email).aggregate(Sum('kpi_actual'))
        
        if organization_emp_one_performance_target['kpi_target__sum']!=None and organization_emp_one_performance_actual['kpi_actual__sum']!=None:
            target = round(organization_emp_one_performance_target['kpi_target__sum'],2)
            actual = round(organization_emp_one_performance_actual['kpi_actual__sum'],2)

            if target<=actual:
                emp_josh_one_percent = (actual/target)*100  
            else:
                emp_josh_one_percent = 0.0
        else:
            emp_josh_one_percent = 0.0

        organization_emp_two_performance_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email).aggregate(Sum('kpi_target'))
        organization_emp_two_performance_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email).aggregate(Sum('kpi_actual'))

        if organization_emp_two_performance_target['kpi_target__sum']!=None and organization_emp_two_performance_actual['kpi_actual__sum']!=None:
            target = round(organization_emp_two_performance_target['kpi_target__sum'],2)
            actual = round(organization_emp_two_performance_actual['kpi_actual__sum'],2)

            if target<=actual:
                emp_josh_two_percent = (actual/target)*100  
            else:
                emp_josh_two_percent = 0.0
        else:
            emp_josh_two_percent = 0.0

        organization_emp_three_performance_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email).aggregate(Sum('kpi_target'))
        organization_emp_three_performance_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email).aggregate(Sum('kpi_actual'))

        if organization_emp_three_performance_target['kpi_target__sum']!=None and organization_emp_three_performance_actual['kpi_actual__sum']!=None:
            target = round(organization_emp_three_performance_target['kpi_target__sum'],2)
            actual = round(organization_emp_three_performance_actual['kpi_actual__sum'],2)

            if target<=actual:
                emp_josh_three_percent = (actual/target)*100  
            else:
                emp_josh_three_percent = 0.0
        else:
            emp_josh_three_percent = 0.0

        organization_emp_four_performance_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email).aggregate(Sum('kpi_target'))
        organization_emp_four_performance_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email).aggregate(Sum('kpi_actual'))

        if organization_emp_four_performance_target['kpi_target__sum']!=None and organization_emp_four_performance_actual['kpi_actual__sum']!=None:
            target = round(organization_emp_four_performance_target['kpi_target__sum'],2)
            actual = round(organization_emp_four_performance_actual['kpi_actual__sum'],2)

            if target<=actual:
                emp_josh_four_percent = (actual/target)*100  
            else:
                emp_josh_four_percent = 0.0
        else:
            emp_josh_four_percent = 0.0

        organization_emp_five_performance_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email).aggregate(Sum('kpi_target'))
        organization_emp_five_performance_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email).aggregate(Sum('kpi_actual'))

        if organization_emp_five_performance_target['kpi_target__sum']!=None and organization_emp_five_performance_actual['kpi_actual__sum']!=None:
            target = round(organization_emp_five_performance_target['kpi_target__sum'],2)
            actual = round(organization_emp_five_performance_actual['kpi_actual__sum'],2)

            if target<=actual:
                emp_josh_five_percent = (actual/target)*100  
            else:
                emp_josh_five_percent = 0.0
        else:
            emp_josh_five_percent = 0.0



    elif time_period=="today":
        team_josh_one    = JoshReason.objects.filter(manager_id=request.data.get("team_id"),created_at__icontains=current_date,emoji_point=1).count()
        team_josh_two    = JoshReason.objects.filter(manager_id=request.data.get("team_id"),created_at__icontains=current_date,emoji_point=2).count()
        team_josh_three  = JoshReason.objects.filter(manager_id=request.data.get("team_id"),created_at__icontains=current_date,emoji_point=3).count()

        total_emp_josh_sum = team_josh_one + team_josh_two + team_josh_three
        
        if not total_emp_josh_sum:
            total_emp_josh_sum = 1

        team_josh_one_percent   = (team_josh_one*100)/total_emp_josh_sum

        team_josh_two_percent   = (team_josh_two*100)/total_emp_josh_sum

        team_josh_three_percent = (team_josh_three*100)/total_emp_josh_sum


        
        # Team mood for pie chart

        team_josh_count  = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__icontains=current_date).count()
        
        if not team_josh_count:
            team_josh_count = 1

        team_josh  = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__icontains=current_date)

        team_josh_sum  = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__icontains=current_date).aggregate(Sum('emoji_point'))['emoji_point__sum']

        team_josh_count_one = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__icontains=current_date,emoji_point=1).count()
        team_josh_count_one_percent = round((team_josh_count_one *100)/team_josh_count,2)  

        team_josh_count_two = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__icontains=current_date,emoji_point=2).count()
        team_josh_count_two_percent = round((team_josh_count_two * 100)/team_josh_count,2)  

        team_josh_count_three = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__icontains=current_date,emoji_point=3).count()
        team_josh_count_three_percent = round((team_josh_count_three * 100)/team_josh_count,2)  

        team_josh_count_four = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__icontains=current_date,emoji_point=4).count()
        team_josh_count_four_percent = round((team_josh_count_four * 100)/team_josh_count,2)  

        team_josh_count_five = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__icontains=current_date,emoji_point=5).count()
        team_josh_count_five_percent = round((team_josh_count_five * 100)/team_josh_count,2)  


        # team kpi data based on josh for  pie chart

        organization_emp_one_performance_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__icontains=current_date).aggregate(Sum('kpi_target'))
        organization_emp_one_performance_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__icontains=current_date).aggregate(Sum('kpi_actual'))
        
        if organization_emp_one_performance_target['kpi_target__sum']!=None and organization_emp_one_performance_actual['kpi_actual__sum']!=None:
            target = round(organization_emp_one_performance_target['kpi_target__sum'],2)
            actual = round(organization_emp_one_performance_actual['kpi_actual__sum'],2)

            if target<=actual:
                emp_josh_one_percent = (actual/target)*100  
            else:
                emp_josh_one_percent = 0.0
        else:
            emp_josh_one_percent = 0.0

        organization_emp_two_performance_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__icontains=current_date).aggregate(Sum('kpi_target'))
        organization_emp_two_performance_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__icontains=current_date).aggregate(Sum('kpi_actual'))

        if organization_emp_two_performance_target['kpi_target__sum']!=None and organization_emp_two_performance_actual['kpi_actual__sum']!=None:
            target = round(organization_emp_two_performance_target['kpi_target__sum'],2)
            actual = round(organization_emp_two_performance_actual['kpi_actual__sum'],2)

            if target<=actual:
                emp_josh_two_percent = (actual/target)*100  
            else:
                emp_josh_two_percent = 0.0
        else:
            emp_josh_two_percent = 0.0

        organization_emp_three_performance_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__icontains=current_date).aggregate(Sum('kpi_target'))
        organization_emp_three_performance_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__icontains=current_date).aggregate(Sum('kpi_actual'))

        if organization_emp_three_performance_target['kpi_target__sum']!=None and organization_emp_three_performance_actual['kpi_actual__sum']!=None:
            target = round(organization_emp_three_performance_target['kpi_target__sum'],2)
            actual = round(organization_emp_three_performance_actual['kpi_actual__sum'],2)

            if target<=actual:
                emp_josh_three_percent = (actual/target)*100  
            else:
                emp_josh_three_percent = 0.0
        else:
            emp_josh_three_percent = 0.0

        organization_emp_four_performance_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__icontains=current_date).aggregate(Sum('kpi_target'))
        organization_emp_four_performance_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__icontains=current_date).aggregate(Sum('kpi_actual'))

        if organization_emp_four_performance_target['kpi_target__sum']!=None and organization_emp_four_performance_actual['kpi_actual__sum']!=None:
            target = round(organization_emp_four_performance_target['kpi_target__sum'],2)
            actual = round(organization_emp_four_performance_actual['kpi_actual__sum'],2)

            if target<=actual:
                emp_josh_four_percent = (actual/target)*100  
            else:
                emp_josh_four_percent = 0.0
        else:
            emp_josh_four_percent = 0.0

        organization_emp_five_performance_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__icontains=current_date).aggregate(Sum('kpi_target'))
        organization_emp_five_performance_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__icontains=current_date).aggregate(Sum('kpi_actual'))

        if organization_emp_five_performance_target['kpi_target__sum']!=None and organization_emp_five_performance_actual['kpi_actual__sum']!=None:
            target = round(organization_emp_five_performance_target['kpi_target__sum'],2)
            actual = round(organization_emp_five_performance_actual['kpi_actual__sum'],2)

            if target<=actual:
                emp_josh_five_percent = (actual/target)*100  
            else:
                emp_josh_five_percent = 0.0
        else:
            emp_josh_five_percent = 0.0


    elif time_period=="yesterday":
        yesterday_date = current_date-timedelta(days=1)
        team_josh_one    = JoshReason.objects.filter(manager_id=request.data.get("team_id"),created_at__icontains=yesterday_date,emoji_point=1).count()
        team_josh_two    = JoshReason.objects.filter(manager_id=request.data.get("team_id"),created_at__icontains=yesterday_date,emoji_point=2).count()
        team_josh_three  = JoshReason.objects.filter(manager_id=request.data.get("team_id"),created_at__icontains=yesterday_date,emoji_point=3).count()

        total_emp_josh_sum = team_josh_one + team_josh_two + team_josh_three
        
        if not total_emp_josh_sum:
            total_emp_josh_sum = 1

        team_josh_one_percent   = (team_josh_one*100)/total_emp_josh_sum

        team_josh_two_percent   = (team_josh_two*100)/total_emp_josh_sum

        team_josh_three_percent = (team_josh_three*100)/total_emp_josh_sum



        # Team mood for pie chart

        team_josh_count  = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__icontains=yesterday_date).count()
        
        if not team_josh_count:
            team_josh_count = 1

        team_josh  = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__icontains=yesterday_date)

        team_josh_sum  = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__icontains=yesterday_date).aggregate(Sum('emoji_point'))['emoji_point__sum']

        team_josh_count_one = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__icontains=yesterday_date,emoji_point=1).count()
        team_josh_count_one_percent = round((team_josh_count_one *100)/team_josh_count,2)  

        team_josh_count_two = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__icontains=yesterday_date,emoji_point=2).count()
        team_josh_count_two_percent = round((team_josh_count_two * 100)/team_josh_count,2)  

        team_josh_count_three = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__icontains=yesterday_date,emoji_point=3).count()
        team_josh_count_three_percent = round((team_josh_count_three * 100)/team_josh_count,2)  

        team_josh_count_four = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__icontains=yesterday_date,emoji_point=4).count()
        team_josh_count_four_percent = round((team_josh_count_four * 100)/team_josh_count,2)  

        team_josh_count_five = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__icontains=yesterday_date,emoji_point=5).count()
        team_josh_count_five_percent = round((team_josh_count_five * 100)/team_josh_count,2)  


        # team kpi data based on josh for  pie chart

        organization_emp_one_performance_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__icontains=yesterday_date).aggregate(Sum('kpi_target'))
        organization_emp_one_performance_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__icontains=yesterday_date).aggregate(Sum('kpi_actual'))
        
        if organization_emp_one_performance_target['kpi_target__sum']!=None and organization_emp_one_performance_actual['kpi_actual__sum']!=None:
            target = round(organization_emp_one_performance_target['kpi_target__sum'],2)
            actual = round(organization_emp_one_performance_actual['kpi_actual__sum'],2)

            if target<=actual:
                emp_josh_one_percent = (actual/target)*100  
            else:
                emp_josh_one_percent = 0.0
        else:
            emp_josh_one_percent = 0.0

        organization_emp_two_performance_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__icontains=yesterday_date).aggregate(Sum('kpi_target'))
        organization_emp_two_performance_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__icontains=yesterday_date).aggregate(Sum('kpi_actual'))

        if organization_emp_two_performance_target['kpi_target__sum']!=None and organization_emp_two_performance_actual['kpi_actual__sum']!=None:
            target = round(organization_emp_two_performance_target['kpi_target__sum'],2)
            actual = round(organization_emp_two_performance_actual['kpi_actual__sum'],2)

            if target<=actual:
                emp_josh_two_percent = (actual/target)*100  
            else:
                emp_josh_two_percent = 0.0
        else:
            emp_josh_two_percent = 0.0

        organization_emp_three_performance_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__icontains=yesterday_date).aggregate(Sum('kpi_target'))
        organization_emp_three_performance_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__icontains=yesterday_date).aggregate(Sum('kpi_actual'))

        if organization_emp_three_performance_target['kpi_target__sum']!=None and organization_emp_three_performance_actual['kpi_actual__sum']!=None:
            target = round(organization_emp_three_performance_target['kpi_target__sum'],2)
            actual = round(organization_emp_three_performance_actual['kpi_actual__sum'],2)

            if target<=actual:
                emp_josh_three_percent = (actual/target)*100  
            else:
                emp_josh_three_percent = 0.0
        else:
            emp_josh_three_percent = 0.0

        organization_emp_four_performance_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__icontains=yesterday_date).aggregate(Sum('kpi_target'))
        organization_emp_four_performance_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__icontains=yesterday_date).aggregate(Sum('kpi_actual'))

        if organization_emp_four_performance_target['kpi_target__sum']!=None and organization_emp_four_performance_actual['kpi_actual__sum']!=None:
            target = round(organization_emp_four_performance_target['kpi_target__sum'],2)
            actual = round(organization_emp_four_performance_actual['kpi_actual__sum'],2)

            if target<=actual:
                emp_josh_four_percent = (actual/target)*100  
            else:
                emp_josh_four_percent = 0.0
        else:
            emp_josh_four_percent = 0.0

        organization_emp_five_performance_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__icontains=yesterday_date).aggregate(Sum('kpi_target'))
        organization_emp_five_performance_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__icontains=yesterday_date).aggregate(Sum('kpi_actual'))

        if organization_emp_five_performance_target['kpi_target__sum']!=None and organization_emp_five_performance_actual['kpi_actual__sum']!=None:
            target = round(organization_emp_five_performance_target['kpi_target__sum'],2)
            actual = round(organization_emp_five_performance_actual['kpi_actual__sum'],2)

            if target<=actual:
                emp_josh_five_percent = (actual/target)*100  
            else:
                emp_josh_five_percent = 0.0
        else:
            emp_josh_five_percent = 0.0


    elif time_period=="wtd":
        end_date   = current_date
        start_date = end_date -timedelta(days=7)

        team_josh_one    = JoshReason.objects.filter(manager_id=request.data.get("team_id"),created_at__range=[start_date,end_date],emoji_point=1).count()
        team_josh_two    = JoshReason.objects.filter(manager_id=request.data.get("team_id"),created_at__range=[start_date,end_date],emoji_point=2).count()
        team_josh_three  = JoshReason.objects.filter(manager_id=request.data.get("team_id"),created_at__range=[start_date,end_date],emoji_point=3).count()

        total_emp_josh_sum = team_josh_one + team_josh_two + team_josh_three
        
        if not total_emp_josh_sum:
            total_emp_josh_sum = 1

        team_josh_one_percent   = (team_josh_one*100)/total_emp_josh_sum

        team_josh_two_percent   = (team_josh_two*100)/total_emp_josh_sum

        team_josh_three_percent = (team_josh_three*100)/total_emp_josh_sum



        # Team mood for pie chart

        team_josh_count  = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__range=[start_date,end_date]).count()
        
        if not team_josh_count:
            team_josh_count = 1

        team_josh  = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__range=[start_date,end_date])

        team_josh_sum  = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__range=[start_date,end_date]).aggregate(Sum('emoji_point'))['emoji_point__sum']

        team_josh_count_one = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__range=[start_date,end_date],emoji_point=1).count()
        team_josh_count_one_percent = round((team_josh_count_one *100)/team_josh_count,2)  

        team_josh_count_two = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__range=[start_date,end_date],emoji_point=2).count()
        team_josh_count_two_percent = round((team_josh_count_two * 100)/team_josh_count,2)  

        team_josh_count_three = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__range=[start_date,end_date],emoji_point=3).count()
        team_josh_count_three_percent = round((team_josh_count_three * 100)/team_josh_count,2)  

        team_josh_count_four = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__range=[start_date,end_date],emoji_point=4).count()
        team_josh_count_four_percent = round((team_josh_count_four * 100)/team_josh_count,2)  

        team_josh_count_five = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__range=[start_date,end_date],emoji_point=5).count()
        team_josh_count_five_percent = round((team_josh_count_five * 100)/team_josh_count,2)  


        # team kpi data based on josh for  pie chart

        organization_emp_one_performance_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__range=[start_date,end_date]).aggregate(Sum('kpi_target'))
        organization_emp_one_performance_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__range=[start_date,end_date]).aggregate(Sum('kpi_actual'))
        
        if organization_emp_one_performance_target['kpi_target__sum']!=None and organization_emp_one_performance_actual['kpi_actual__sum']!=None:
            target = round(organization_emp_one_performance_target['kpi_target__sum'],2)
            actual = round(organization_emp_one_performance_actual['kpi_actual__sum'],2)

            if target<=actual:
                emp_josh_one_percent = (actual/target)*100  
            else:
                emp_josh_one_percent = 0.0
        else:
            emp_josh_one_percent = 0.0

        organization_emp_two_performance_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__range=[start_date,end_date]).aggregate(Sum('kpi_target'))
        organization_emp_two_performance_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__range=[start_date,end_date]).aggregate(Sum('kpi_actual'))

        if organization_emp_two_performance_target['kpi_target__sum']!=None and organization_emp_two_performance_actual['kpi_actual__sum']!=None:
            target = round(organization_emp_two_performance_target['kpi_target__sum'],2)
            actual = round(organization_emp_two_performance_actual['kpi_actual__sum'],2)

            if target<=actual:
                emp_josh_two_percent = (actual/target)*100  
            else:
                emp_josh_two_percent = 0.0
        else:
            emp_josh_two_percent = 0.0

        organization_emp_three_performance_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__range=[start_date,end_date]).aggregate(Sum('kpi_target'))
        organization_emp_three_performance_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__range=[start_date,end_date]).aggregate(Sum('kpi_actual'))

        if organization_emp_three_performance_target['kpi_target__sum']!=None and organization_emp_three_performance_actual['kpi_actual__sum']!=None:
            target = round(organization_emp_three_performance_target['kpi_target__sum'],2)
            actual = round(organization_emp_three_performance_actual['kpi_actual__sum'],2)

            if target<=actual:
                emp_josh_three_percent = (actual/target)*100  
            else:
                emp_josh_three_percent = 0.0
        else:
            emp_josh_three_percent = 0.0

        organization_emp_four_performance_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__range=[start_date,end_date]).aggregate(Sum('kpi_target'))
        organization_emp_four_performance_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__range=[start_date,end_date]).aggregate(Sum('kpi_actual'))

        if organization_emp_four_performance_target['kpi_target__sum']!=None and organization_emp_four_performance_actual['kpi_actual__sum']!=None:
            target = round(organization_emp_four_performance_target['kpi_target__sum'],2)
            actual = round(organization_emp_four_performance_actual['kpi_actual__sum'],2)

            if target<=actual:
                emp_josh_four_percent = (actual/target)*100  
            else:
                emp_josh_four_percent = 0.0
        else:
            emp_josh_four_percent = 0.0

        organization_emp_five_performance_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__range=[start_date,end_date]).aggregate(Sum('kpi_target'))
        organization_emp_five_performance_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__range=[start_date,end_date]).aggregate(Sum('kpi_actual'))

        if organization_emp_five_performance_target['kpi_target__sum']!=None and organization_emp_five_performance_actual['kpi_actual__sum']!=None:
            target = round(organization_emp_five_performance_target['kpi_target__sum'],2)
            actual = round(organization_emp_five_performance_actual['kpi_actual__sum'],2)

            if target<=actual:
                emp_josh_five_percent = (actual/target)*100  
            else:
                emp_josh_five_percent = 0.0
        else:
            emp_josh_five_percent = 0.0

    elif time_period=="mtd":
        month = current_date.month
        year = current_date.year

        team_josh_one    = JoshReason.objects.filter(manager_id=request.data.get("team_id"),created_at__year=year,created_at__month=month,emoji_point=1).count()
        team_josh_two    = JoshReason.objects.filter(manager_id=request.data.get("team_id"),created_at__year=year,created_at__month=month,emoji_point=2).count()
        team_josh_three  = JoshReason.objects.filter(manager_id=request.data.get("team_id"),created_at__year=year,created_at__month=month,emoji_point=3).count()

        total_emp_josh_sum = team_josh_one + team_josh_two + team_josh_three
        
        if not total_emp_josh_sum:
            total_emp_josh_sum = 1

        team_josh_one_percent   = (team_josh_one*100)/total_emp_josh_sum

        team_josh_two_percent   = (team_josh_two*100)/total_emp_josh_sum

        team_josh_three_percent = (team_josh_three*100)/total_emp_josh_sum



        # Team mood for pie chart

        team_josh_count  = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__year=year,created_at__month=month).count()
        
        if not team_josh_count:
            team_josh_count = 1

        team_josh  = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__year=year,created_at__month=month)

        team_josh_sum  = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__year=year,created_at__month=month).aggregate(Sum('emoji_point'))['emoji_point__sum']

        team_josh_count_one = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__year=year,created_at__month=month,emoji_point=1).count()
        team_josh_count_one_percent = round((team_josh_count_one *100)/team_josh_count,2)  

        team_josh_count_two = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__year=year,created_at__month=month,emoji_point=2).count()
        team_josh_count_two_percent = round((team_josh_count_two * 100)/team_josh_count,2)  

        team_josh_count_three = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__year=year,created_at__month=month,emoji_point=3).count()
        team_josh_count_three_percent = round((team_josh_count_three * 100)/team_josh_count,2)  

        team_josh_count_four = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__year=year,created_at__month=month,emoji_point=4).count()
        team_josh_count_four_percent = round((team_josh_count_four * 100)/team_josh_count,2)  

        team_josh_count_five = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__year=year,created_at__month=month,emoji_point=5).count()
        team_josh_count_five_percent = round((team_josh_count_five * 100)/team_josh_count,2)  


        # team kpi data based on josh for  pie chart

        organization_emp_one_performance_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__year=year,permormance_date__month=month).aggregate(Sum('kpi_target'))
        organization_emp_one_performance_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__year=year,permormance_date__month=month).aggregate(Sum('kpi_actual'))
        
        if organization_emp_one_performance_target['kpi_target__sum']!=None and organization_emp_one_performance_actual['kpi_actual__sum']!=None:
            target = round(organization_emp_one_performance_target['kpi_target__sum'],2)
            actual = round(organization_emp_one_performance_actual['kpi_actual__sum'],2)

            if target<=actual:
                emp_josh_one_percent = (actual/target)*100  
            else:
                emp_josh_one_percent = 0.0
        else:
            emp_josh_one_percent = 0.0

        organization_emp_two_performance_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__year=year,permormance_date__month=month).aggregate(Sum('kpi_target'))
        organization_emp_two_performance_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__year=year,permormance_date__month=month).aggregate(Sum('kpi_actual'))

        if organization_emp_two_performance_target['kpi_target__sum']!=None and organization_emp_two_performance_actual['kpi_actual__sum']!=None:
            target = round(organization_emp_two_performance_target['kpi_target__sum'],2)
            actual = round(organization_emp_two_performance_actual['kpi_actual__sum'],2)

            if target<=actual:
                emp_josh_two_percent = (actual/target)*100  
            else:
                emp_josh_two_percent = 0.0
        else:
            emp_josh_two_percent = 0.0

        organization_emp_three_performance_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__year=year,permormance_date__month=month).aggregate(Sum('kpi_target'))
        organization_emp_three_performance_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__year=year,permormance_date__month=month).aggregate(Sum('kpi_actual'))

        if organization_emp_three_performance_target['kpi_target__sum']!=None and organization_emp_three_performance_actual['kpi_actual__sum']!=None:
            target = round(organization_emp_three_performance_target['kpi_target__sum'],2)
            actual = round(organization_emp_three_performance_actual['kpi_actual__sum'],2)

            if target<=actual:
                emp_josh_three_percent = (actual/target)*100  
            else:
                emp_josh_three_percent = 0.0
        else:
            emp_josh_three_percent = 0.0

        organization_emp_four_performance_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__year=year,permormance_date__month=month).aggregate(Sum('kpi_target'))
        organization_emp_four_performance_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__year=year,permormance_date__month=month).aggregate(Sum('kpi_actual'))

        if organization_emp_four_performance_target['kpi_target__sum']!=None and organization_emp_four_performance_actual['kpi_actual__sum']!=None:
            target = round(organization_emp_four_performance_target['kpi_target__sum'],2)
            actual = round(organization_emp_four_performance_actual['kpi_actual__sum'],2)

            if target<=actual:
                emp_josh_four_percent = (actual/target)*100  
            else:
                emp_josh_four_percent = 0.0
        else:
            emp_josh_four_percent = 0.0

        organization_emp_five_performance_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__year=year,permormance_date__month=month).aggregate(Sum('kpi_target'))
        organization_emp_five_performance_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__year=year,permormance_date__month=month).aggregate(Sum('kpi_actual'))

        if organization_emp_five_performance_target['kpi_target__sum']!=None and organization_emp_five_performance_actual['kpi_actual__sum']!=None:
            target = round(organization_emp_five_performance_target['kpi_target__sum'],2)
            actual = round(organization_emp_five_performance_actual['kpi_actual__sum'],2)

            if target<=actual:
                emp_josh_five_percent = (actual/target)*100  
            else:
                emp_josh_five_percent = 0.0
        else:
            emp_josh_five_percent = 0.0

    elif time_period=="ytd":
        year = current_date.year

        team_josh_one    = JoshReason.objects.filter(manager_id=request.data.get("team_id"),created_at__year=year,emoji_point=1).count()
        team_josh_two    = JoshReason.objects.filter(manager_id=request.data.get("team_id"),created_at__year=year,emoji_point=2).count()
        team_josh_three  = JoshReason.objects.filter(manager_id=request.data.get("team_id"),created_at__year=year,emoji_point=3).count()

        total_emp_josh_sum = team_josh_one + team_josh_two + team_josh_three
        
        if not total_emp_josh_sum:
            total_emp_josh_sum = 1

        team_josh_one_percent   = (team_josh_one*100)/total_emp_josh_sum

        team_josh_two_percent   = (team_josh_two*100)/total_emp_josh_sum

        team_josh_three_percent = (team_josh_three*100)/total_emp_josh_sum


        # Team mood for pie chart

        team_josh_count  = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__icontains=current_date).count()
        
        if not team_josh_count:
            team_josh_count = 1

        team_josh  = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__year=year)

        team_josh_sum  = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__year=year).aggregate(Sum('emoji_point'))['emoji_point__sum']

        team_josh_count_one = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__year=year,emoji_point=1).count()
        team_josh_count_one_percent = round((team_josh_count_one *100)/team_josh_count,2)  

        team_josh_count_two = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__year=year,emoji_point=2).count()
        team_josh_count_two_percent = round((team_josh_count_two * 100)/team_josh_count,2)  

        team_josh_count_three = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__year=year,emoji_point=3).count()
        team_josh_count_three_percent = round((team_josh_count_three * 100)/team_josh_count,2)  

        team_josh_count_four = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__year=year,emoji_point=4).count()
        team_josh_count_four_percent = round((team_josh_count_four * 100)/team_josh_count,2)  

        team_josh_count_five = JoshReason.objects.values().filter(manager_id=request.data.get("team_id"),created_at__year=year,emoji_point=5).count()
        team_josh_count_five_percent = round((team_josh_count_five * 100)/team_josh_count,2)  


        # team kpi data based on josh for  pie chart

        organization_emp_one_performance_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__year=year).aggregate(Sum('kpi_target'))
        organization_emp_one_performance_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__year=year).aggregate(Sum('kpi_actual'))
        
        if organization_emp_one_performance_target['kpi_target__sum']!=None and organization_emp_one_performance_actual['kpi_actual__sum']!=None:
            target = round(organization_emp_one_performance_target['kpi_target__sum'],2)
            actual = round(organization_emp_one_performance_actual['kpi_actual__sum'],2)

            if target<=actual:
                emp_josh_one_percent = (actual/target)*100  
            else:
                emp_josh_one_percent = 0.0
        else:
            emp_josh_one_percent = 0.0

        organization_emp_two_performance_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__year=year).aggregate(Sum('kpi_target'))
        organization_emp_two_performance_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__year=year).aggregate(Sum('kpi_actual'))

        if organization_emp_two_performance_target['kpi_target__sum']!=None and organization_emp_two_performance_actual['kpi_actual__sum']!=None:
            target = round(organization_emp_two_performance_target['kpi_target__sum'],2)
            actual = round(organization_emp_two_performance_actual['kpi_actual__sum'],2)

            if target<=actual:
                emp_josh_two_percent = (actual/target)*100  
            else:
                emp_josh_two_percent = 0.0
        else:
            emp_josh_two_percent = 0.0

        organization_emp_three_performance_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__year=year).aggregate(Sum('kpi_target'))
        organization_emp_three_performance_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__year=year).aggregate(Sum('kpi_actual'))

        if organization_emp_three_performance_target['kpi_target__sum']!=None and organization_emp_three_performance_actual['kpi_actual__sum']!=None:
            target = round(organization_emp_three_performance_target['kpi_target__sum'],2)
            actual = round(organization_emp_three_performance_actual['kpi_actual__sum'],2)

            if target<=actual:
                emp_josh_three_percent = (actual/target)*100  
            else:
                emp_josh_three_percent = 0.0
        else:
            emp_josh_three_percent = 0.0

        organization_emp_four_performance_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__year=year).aggregate(Sum('kpi_target'))
        organization_emp_four_performance_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__year=year).aggregate(Sum('kpi_actual'))

        if organization_emp_four_performance_target['kpi_target__sum']!=None and organization_emp_four_performance_actual['kpi_actual__sum']!=None:
            target = round(organization_emp_four_performance_target['kpi_target__sum'],2)
            actual = round(organization_emp_four_performance_actual['kpi_actual__sum'],2)

            if target<=actual:
                emp_josh_four_percent = (actual/target)*100  
            else:
                emp_josh_four_percent = 0.0
        else:
            emp_josh_four_percent = 0.0

        organization_emp_five_performance_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__year=year).aggregate(Sum('kpi_target'))
        organization_emp_five_performance_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_employees_email,permormance_date__year=year).aggregate(Sum('kpi_actual'))

        if organization_emp_five_performance_target['kpi_target__sum']!=None and organization_emp_five_performance_actual['kpi_actual__sum']!=None:
            target = round(organization_emp_five_performance_target['kpi_target__sum'],2)
            actual = round(organization_emp_five_performance_actual['kpi_actual__sum'],2)

            if target<=actual:
                emp_josh_five_percent = (actual/target)*100  
            else:
                emp_josh_five_percent = 0.0
        else:
            emp_josh_five_percent = 0.0


    context = {}
    context["reasons_for_scores_below_four"]    = {"team_josh_one_percent":team_josh_one_percent,"team_josh_two_percent":team_josh_two_percent,"team_josh_three_percent":team_josh_three_percent}
    
    # used for pie chart for manager josh and kpi percent

    context['team_josh_percent']            = {'one':team_josh_count_one_percent,'two':team_josh_count_two_percent,'three':team_josh_count_three_percent,'four':team_josh_count_four_percent,'five':team_josh_count_five_percent}
    context['team_kpi_met_percent']         = {'one':emp_josh_one_percent,'two':emp_josh_two_percent,'three':emp_josh_three_percent,'four':emp_josh_four_percent,'five':emp_josh_five_percent}

    context['message']                         = 'Data has been received successfully' 
    context['response_code']                   = 200
    return Response(context, status=HTTP_200_OK)




# Manager Team Profile view
@api_view(['GET'])
@authenticate_token
def team_profile(request):
    try:
        unique_code=request.query_params.get('unique_code',None)   #(1 query)    print(unique_code)
    except:
        return Response(data={'msg':'Please Provide Unique Code Value in Params'})
    
    team_profile_data=Manager.objects.filter(team__organization__unique_code=unique_code)
    team_profile_data_count=Manager.objects.filter(team__organization__unique_code=unique_code).count()
    serializer=ManagerSerializer(team_profile_data,many=True)
    return Response(data={'msg':'Success','data':serializer.data,'count':team_profile_data_count,'response_code':'200'},status=HTTP_200_OK)




# TeamCampaign KPI's Views
@api_view(['GET'])
@authenticate_token
def team_Campaign_kpi(request):

    try:
        user_Profile=request.query_params.get('UserProfile',None)
    except:
        return Response(data={'msg':'Please Provide Unique Code Value in Params'})

    user_profile_data=UserProfile.objects.filter(id=user_Profile).first()

    user_profile_id=user_profile_data.id


    team_campaign_kpi_data=TeamCampaign.objects.filter(manager__id=user_profile_id)
    team_campaign_kpi_data_count=TeamCampaign.objects.filter(manager__id=user_profile_id).count()

    serializer=TeamCampaignSerializers(team_campaign_kpi_data,many=True).data
    data = [] 
    for obj in serializer:
        data.append(obj['criteria_point'][0])
    
    return Response(data={'msg':'Success','Data':data,'count':team_campaign_kpi_data_count,'response_code':200},status=status.HTTP_200_OK)




# Industry List Data 
@csrf_exempt
@api_view(['POST'])
@authenticate_token
def industry_list_data(request):
    if request.data.get("unique_code") == '' or request.data.get("unique_code") is None:  
        return Response({'message': 'Please provide unique code', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST) 

    industry_work_data=IndustryWorkType.objects.filter(status=1,organiztaion__unique_code=request.data.get("unique_code")).values()
    
    print("indd===>",industry_work_data)

    context = {}
    context['industry_work_data'] = industry_work_data
    context['message']  = 'industry_work_data data has been received successfully'
    context['response'] =  200
    return Response(context,status.HTTP_200_OK)




#  Kpi Name List Data based on industry work type id

@csrf_exempt
@api_view(['GET'])
@authenticate_token
def  kpiname_list_data(request):
    if request.query_params.get('industry_id') == '' or request.query_params.get('industry_id') is None:  
        return Response({'message': 'Please provide industry id in params', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST) 
    
    industry_id= request.query_params.get('industry_id')
    kpi_name_data= KpiName.objects.filter(industry_work_type__id=request.query_params.get('industry_id')).values()
    context = {}
    if kpi_name_data:
  
        context = {}
        context['kpi_name_data'] = kpi_name_data
        context['message']       = (f"Kpi Name Data successfully found for industry id {industry_id}.")
        context['response_code']      = 200
        return Response(context,status.HTTP_200_OK)

    else:
   
        context['kpi_name_data'] = kpi_name_data
        context['message']       = (f"Kpi Name Data not found  for industry id {industry_id}.")
        context['response_code']      = 201
        return Response(context,status.HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@authenticate_token
def team_performance_lists(request):
    if request.data.get("manager_email") == '' or request.data.get("manager_email") is None:  
        return Response({'message': 'Please provide manager id', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST) 

    if request.data.get("team_id") == '' or request.data.get("team_id") is None:  
        return Response({'message': 'Please provide team id', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST) 

    select_name = request.data.get('select_name')
    select_kpi  = request.data.get('select_kpi')
    select_time_period = request.data.get('select_time_period')


    context = {}

  
    team_performance_data = []
    
    
    manager = UserProfile.objects.filter(user__email=request.data.get("manager_email"),role__id=2).first()
    
    team_member_count = UserProfile.objects.filter(team_id=request.data.get("team_id"),role__id=1).count()

    team_member_data = UserProfile.objects.filter(team_id=request.data.get("team_id"),role__id=1)

    team_member_data_id = UserProfile.objects.filter(team_id=request.data.get("team_id"),role__id=1).values_list('id',flat=True)

    team_member_email = UserProfile.objects.filter(team_id=request.data.get("team_id"),role__id=1).values_list('user__email',flat=True)

   
    if select_name!="all": 
        employee_data = UserProfile.objects.filter(id=select_name).first()

    current_date=datetime.now().date()

    current_time=datetime.now().strftime('%I:%M')
    
    kpi_items = []

    if select_name=="all" and select_kpi=="all" and select_time_period=="all":
       
        kpi_data = KpiName.objects.filter(organiztaion__unique_code=manager.unique_code)
        manager_kpi_met_data = 0
        kpi_wip = 0

        for kpi in kpi_data:

            if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id).exists():
    
                manager_employee_kpi_data_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id).aggregate(Sum('kpi_target'))

                manager_employee_kpi_data_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id).aggregate(Sum('kpi_actual'))
                
                if not manager_employee_kpi_data_target['kpi_target__sum']:
                    pass
                else:
                    kpi_target = round(manager_employee_kpi_data_target['kpi_target__sum'],2)
                

                if not manager_employee_kpi_data_actual['kpi_actual__sum']:
                    pass
                else:
                    kpi_actual = round(manager_employee_kpi_data_actual['kpi_actual__sum'],2)
                
              
                if kpi_target <= kpi_actual:
                    manager_kpi_met_data +=1
                
                if kpi_target>kpi_actual:
                    kpi_wip +=1         


        kpi_data = KpiName.objects.filter(organiztaion__unique_code=manager.unique_code)

        for kpi in kpi_data:
          
            data ={}
            
            if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id).exists():

                total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id).aggregate(Sum('kpi_target'))
                total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id).aggregate(Sum('kpi_actual'))
                
                if total_target['kpi_target__sum'] !=None or total_actual['kpi_actual__sum'] !=None: 
                    data['kpi_name']       = kpi.name
                    data['total_target']   = round(total_target['kpi_target__sum'],2)
                    data['total_actual']   = round(total_actual['kpi_actual__sum'],2)
                    data['total_gap']      = round(total_target['kpi_target__sum'] - total_actual['kpi_actual__sum'],2)
                
                    kpi_items.append(data)

    elif select_name=="all" and select_kpi=="all" and select_time_period=="today":
        # manager_kpi_met_data = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_status=1,permormance_date__icontains=current_date).count() 
       
        # kpi_wip = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,permormance_date__icontains=current_date,kpi_status=0).count() 

        # for member in team_member_data:

        #     challenges = TeamAcceptChallengeHistory.objects.filter(customer_accepted_id=member.id,team_challenge__is_completed_by_manager=0)
     
        #     kpi_wip = 0

        #     if challenges:
        #         for challenge in challenges:
        #             if challenge.team_challenge.start_time<=current_time and challenge.team_challenge.end_time>=current_time:
        #                 kpi_wip +=1
            

        #     team_campaigns = TeamAcceptCampaignHistory.objects.filter(customer_accepted_id=member.id,team_campaign__is_completed_by_manager=0)

        #     for campaign in team_campaigns:
        #         if campaign.team_campaign.start_date<=current_date and campaign.team_campaign.end_date>=current_date:
        #             kpi_data = len(campaign.team_campaign.criteria_point.all())
        #             kpi_wip +=kpi_data

        # for employee_email in team_member_email:
        # kpi_data = KpiName.objects.filter(organiztaion__unique_code=manager.unique_code)

        # for kpi in kpi_data:
        #     data ={}
            
        #     if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__icontains=current_date).exists():

        #         total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__icontains=current_date).aggregate(Sum('kpi_target'))
        #         total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__icontains=current_date).aggregate(Sum('kpi_actual'))

        #         data['kpi_name']       = kpi.name
        #         data['total_target']   = total_target['kpi_target__sum']
        #         data['total_actual']   = total_actual['kpi_actual__sum']
        #         data['total_gap']      = total_target['kpi_target__sum'] - total_actual['kpi_actual__sum']
                
        #         kpi_items.append(data)

        # kpi_data = KpiName.objects.filter(organiztaion__unique_code=manager.unique_code)

        # for kpi in kpi_data:
          
        #     data ={}
            
        #     if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,permormance_date__icontains=current_date,kpi_name_data__id=kpi.id).exists():

        #         total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__icontains=current_date).aggregate(Sum('kpi_target'))
        #         total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__icontains=current_date).aggregate(Sum('kpi_actual'))
                
        #         if total_target['kpi_target__sum'] and total_actual['kpi_actual__sum']: 
        #             data['kpi_name']       = kpi.name
        #             data['total_target']   = round(total_target['kpi_target__sum'],2)
        #             data['total_actual']   = round(total_actual['kpi_actual__sum'],2)
        #             data['total_gap']      = round(total_target['kpi_target__sum'] - total_actual['kpi_actual__sum'],2)
                
        #             kpi_items.append(data)

        
        kpi_data = KpiName.objects.filter(organiztaion__unique_code=manager.unique_code)
        manager_kpi_met_data = 0
        kpi_wip = 0

        for kpi in kpi_data:

            if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__icontains=current_date).exists():
    
                manager_employee_kpi_data_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__icontains=current_date).aggregate(Sum('kpi_target'))

                manager_employee_kpi_data_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__icontains=current_date).aggregate(Sum('kpi_actual'))
                
                if not manager_employee_kpi_data_target['kpi_target__sum']:
                    pass
                else:
                    kpi_target = round(manager_employee_kpi_data_target['kpi_target__sum'],2)
                

                if not manager_employee_kpi_data_actual['kpi_actual__sum']:
                    pass
                else:
                    kpi_actual = round(manager_employee_kpi_data_actual['kpi_actual__sum'],2)
                
              
                if kpi_target <= kpi_actual:
                    manager_kpi_met_data +=1
                
                if kpi_target>kpi_actual:
                    kpi_wip +=1         


        kpi_data = KpiName.objects.filter(organiztaion__unique_code=manager.unique_code)

        for kpi in kpi_data:
          
            data ={}
            
            if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__icontains=current_date).exists():

                total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__icontains=current_date).aggregate(Sum('kpi_target'))
                total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__icontains=current_date).aggregate(Sum('kpi_actual'))
                
                if total_target['kpi_target__sum'] !=None or total_actual['kpi_actual__sum'] !=None: 
                    data['kpi_name']       = kpi.name
                    data['total_target']   = round(total_target['kpi_target__sum'],2)
                    data['total_actual']   = round(total_actual['kpi_actual__sum'],2)
                    data['total_gap']      = round(total_target['kpi_target__sum'] - total_actual['kpi_actual__sum'],2)
                
                    kpi_items.append(data)
            
        
    elif select_name=="all" and select_kpi=="all" and select_time_period=="yesterday":
        yesterday_date = current_date-timedelta(days=1)
        
        # manager_kpi_met_data = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_status=1,permormance_date__icontains=yesterday_date).count() 
       
        # kpi_wip = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,permormance_date__icontains=yesterday_date,kpi_status=0).count() 

        # for member in team_member_data:
        #     kpi_wip = 0

        #     # team_campaigns = TeamCampaign.objects.filter(customer_accepted_id=member.id,is_completed_by_manager=0)
        #     team_campaigns = TeamAcceptCampaignHistory.objects.filter(customer_accepted_id=member.id,team_campaign__is_completed_by_manager=0)

        #     for campaign in team_campaigns:
        #         if campaign.team_challenge.start_date<=yesterday_date and campaign.team_challenge.end_date>=yesterday_date:
        #             kpi_data = len(campaign.team_challenge.criteria_point.all())
        #             kpi_wip +=kpi_data

        # for employee_email in team_member_email:
        # kpi_data = KpiName.objects.filter(organiztaion__unique_code=manager.unique_code)

        # for kpi in kpi_data:
        #     data ={}
            
        #     if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__icontains=yesterday_date).exists():

        #         total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__icontains=yesterday_date).aggregate(Sum('kpi_target'))
        #         total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__icontains=yesterday_date).aggregate(Sum('kpi_actual'))

        #         data['kpi_name']       = kpi.name
        #         data['total_target']   = total_target['kpi_target__sum']
        #         data['total_actual']   = total_actual['kpi_actual__sum']
        #         data['total_gap']      = total_target['kpi_target__sum'] - total_actual['kpi_actual__sum']
                
        #         kpi_items.append(data)


        # kpi_data = KpiName.objects.filter(organiztaion__unique_code=manager.unique_code)

        # for kpi in kpi_data:
          
        #     data ={}
            
        #     if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,permormance_date__icontains=yesterday_date,kpi_name_data__id=kpi.id).exists():

        #         total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__icontains=yesterday_date).aggregate(Sum('kpi_target'))
        #         total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__icontains=yesterday_date).aggregate(Sum('kpi_actual'))
                
        #         if total_target['kpi_target__sum'] and total_actual['kpi_actual__sum']: 
        #             data['kpi_name']       = kpi.name
        #             data['total_target']   = round(total_target['kpi_target__sum'],2)
        #             data['total_actual']   = round(total_actual['kpi_actual__sum'],2)
        #             data['total_gap']      = round(total_target['kpi_target__sum'] - total_actual['kpi_actual__sum'],2)
                
        #             kpi_items.append(data)

        kpi_data = KpiName.objects.filter(organiztaion__unique_code=manager.unique_code)
        
        manager_kpi_met_data = 0
        kpi_wip = 0

        for kpi in kpi_data:

            if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__icontains=yesterday_date).exists():
    
                manager_employee_kpi_data_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__icontains=yesterday_date).aggregate(Sum('kpi_target'))

                manager_employee_kpi_data_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__icontains=yesterday_date).aggregate(Sum('kpi_actual'))
                
                if not manager_employee_kpi_data_target['kpi_target__sum']:
                    pass
                else:
                    kpi_target = round(manager_employee_kpi_data_target['kpi_target__sum'],2)
                

                if not manager_employee_kpi_data_actual['kpi_actual__sum']:
                    pass
                else:
                    kpi_actual = round(manager_employee_kpi_data_actual['kpi_actual__sum'],2)
                
              
                if kpi_target <= kpi_actual:
                    manager_kpi_met_data +=1
                
                if kpi_target>kpi_actual:
                    kpi_wip +=1         


        kpi_data = KpiName.objects.filter(organiztaion__unique_code=manager.unique_code)

        for kpi in kpi_data:
          
            data ={}
            
            if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__icontains=yesterday_date).exists():

                total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__icontains=yesterday_date).aggregate(Sum('kpi_target'))
                total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__icontains=yesterday_date).aggregate(Sum('kpi_actual'))
                
                if total_target['kpi_target__sum'] !=None or total_actual['kpi_actual__sum'] !=None: 
                    data['kpi_name']       = kpi.name
                    data['total_target']   = round(total_target['kpi_target__sum'],2)
                    data['total_actual']   = round(total_actual['kpi_actual__sum'],2)
                    data['total_gap']      = round(total_target['kpi_target__sum'] - total_actual['kpi_actual__sum'],2)
                
                    kpi_items.append(data)
            

    elif select_name=="all" and select_kpi=="all" and select_time_period=="wtd":
        end_date   = current_date
        start_date = end_date -timedelta(days=7)

        # manager_kpi_met_data = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_status=1,permormance_date__date__range=[start_date,end_date]).count() 
       
        # kpi_wip = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,permormance_date__date__range=[start_date,end_date],kpi_status=0).count() 

        # # for member in team_member_data:
        # kpi_wip = 0

        # # team_campaigns = TeamCampaign.objects.filter(customer_accepted_id__in=team_member_data_id,is_completed_by_manager=0)

        # team_campaigns = TeamAcceptCampaignHistory.objects.filter(customer_accepted_id__in=team_member_data_id,team_campaign__is_completed_by_manager=0)

        # while start_date <= end_date:

        #     for campaign in team_campaigns:
        #         if campaign.team_campaign.start_date<=start_date and campaign.team_campaign.end_date>=start_date:
        #             kpi_data = len(campaign.team_campaign.criteria_point.all())
        #             kpi_wip +=kpi_data
        #     start_date  = start_date + timedelta(days=1) 

        # for employee_email in team_member_email:
        
        # kpi_data = KpiName.objects.filter(organiztaion__unique_code=manager.unique_code)

        # for kpi in kpi_data:
        #     data ={}
            
        #     if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__date__range=[start_date,end_date]).exists():

        #         total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__date__range=[start_date,end_date]).aggregate(Sum('kpi_target'))
        #         total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__date__range=[start_date,end_date]).aggregate(Sum('kpi_actual'))

        #         data['kpi_name']       = kpi.name
        #         data['total_target']   = total_target['kpi_target__sum']
        #         data['total_actual']   = total_actual['kpi_actual__sum']
        #         data['total_gap']      = total_target['kpi_target__sum'] - total_actual['kpi_actual__sum']
                
        #         kpi_items.append(data)

        # kpi_data = KpiName.objects.filter(organiztaion__unique_code=manager.unique_code)

        # for kpi in kpi_data:
          
        #     data ={}
            
        #     if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,permormance_date__date__range=[start_date,end_date],kpi_name_data__id=kpi.id).exists():

        #         total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__date__range=[start_date,end_date]).aggregate(Sum('kpi_target'))
        #         total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__date__range=[start_date,end_date]).aggregate(Sum('kpi_actual'))
                
        #         if total_target['kpi_target__sum'] and total_actual['kpi_actual__sum']: 
        #             data['kpi_name']       = kpi.name
        #             data['total_target']   = round(total_target['kpi_target__sum'],2)
        #             data['total_actual']   = round(total_actual['kpi_actual__sum'],2)
        #             data['total_gap']      = round(total_target['kpi_target__sum'] - total_actual['kpi_actual__sum'],2)
                
        #             kpi_items.append(data)



        kpi_data = KpiName.objects.filter(organiztaion__unique_code=manager.unique_code)
        
        manager_kpi_met_data = 0
        kpi_wip = 0

        for kpi in kpi_data:

            if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__date__range=[start_date,end_date]).exists():
    
                manager_employee_kpi_data_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__date__range=[start_date,end_date]).aggregate(Sum('kpi_target'))

                manager_employee_kpi_data_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__date__range=[start_date,end_date]).aggregate(Sum('kpi_actual'))
                
                if not manager_employee_kpi_data_target['kpi_target__sum']:
                    pass
                else:
                    kpi_target = round(manager_employee_kpi_data_target['kpi_target__sum'],2)
                

                if not manager_employee_kpi_data_actual['kpi_actual__sum']:
                    pass
                else:
                    kpi_actual = round(manager_employee_kpi_data_actual['kpi_actual__sum'],2)
                
              
                if kpi_target <= kpi_actual:
                    manager_kpi_met_data +=1
                
                if kpi_target>kpi_actual:
                    kpi_wip +=1         


        kpi_data = KpiName.objects.filter(organiztaion__unique_code=manager.unique_code)

        for kpi in kpi_data:
          
            data ={}
            
            if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__date__range=[start_date,end_date]).exists():

                total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__date__range=[start_date,end_date]).aggregate(Sum('kpi_target'))
                total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__date__range=[start_date,end_date]).aggregate(Sum('kpi_actual'))
                
                if total_target['kpi_target__sum'] !=None or total_actual['kpi_actual__sum'] !=None: 
                    data['kpi_name']       = kpi.name
                    data['total_target']   = round(total_target['kpi_target__sum'],2)
                    data['total_actual']   = round(total_actual['kpi_actual__sum'],2)
                    data['total_gap']      = round(total_target['kpi_target__sum'] - total_actual['kpi_actual__sum'],2)
                
                    kpi_items.append(data)
            



    elif select_name=="all" and select_kpi=="all" and select_time_period=="mtd":
        month = current_date.month
        year = current_date.year

        # manager_kpi_met_data = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_status=1,permormance_date__date__month=month,permormance_date__year=year).count() 
       
        # kpi_wip = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,permormance_date__date__month=month,permormance_date__year=year,kpi_status=0).count() 

        # for member in team_member_data:
        # kpi_wip = 0

        # # team_campaigns = TeamCampaign.objects.filter(customer_accepted_id__in=team_member_data_id,updated_at__month=month,updated_at__year=year,is_completed_by_manager=0)
        
        # team_campaigns = TeamAcceptCampaignHistory.objects.filter(customer_accepted_id__in=team_member_data_id,team_campaign__updated_at__month=month,team_campaign__updated_at__year=year,team_campaign__is_completed_by_manager=0)

        # for campaign in team_campaigns:
        #     kpi_data = len(campaign.criteria_point.all())
        #     kpi_wip +=kpi_data

        # # for employee_email in team_member_email:
        # kpi_data = KpiName.objects.filter(organiztaion__unique_code=manager.unique_code)

        # for kpi in kpi_data:
        #     data ={}
            
        #     if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__month=month,permormance_date__year=year):

        #         total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__month=month,permormance_date__year=year).aggregate(Sum('kpi_target'))
        #         total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__month=month,permormance_date__year=year).aggregate(Sum('kpi_actual'))

        #         data['kpi_name']       = kpi.name
        #         data['total_target']   = total_target['kpi_target__sum']
        #         data['total_actual']   = total_actual['kpi_actual__sum']
        #         data['total_gap']      = total_target['kpi_target__sum'] - total_actual['kpi_actual__sum']
                
        #         kpi_items.append(data)

        # kpi_data = KpiName.objects.filter(organiztaion__unique_code=manager.unique_code)

        # for kpi in kpi_data:
            
        #     data ={}
            
        #     if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,permormance_date__date__month=month,permormance_date__year=year,kpi_name_data__id=kpi.id).exists():

        #         total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__date__month=month,permormance_date__year=year).aggregate(Sum('kpi_target'))
        #         total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__date__month=month,permormance_date__year=year).aggregate(Sum('kpi_actual'))
                
        #         if total_target['kpi_target__sum'] and total_actual['kpi_actual__sum']: 
        #             data['kpi_name']       = kpi.name
        #             data['total_target']   = round(total_target['kpi_target__sum'],2)
        #             data['total_actual']   = round(total_actual['kpi_actual__sum'],2)
        #             data['total_gap']      = round(total_target['kpi_target__sum'] - total_actual['kpi_actual__sum'],2)
                
        #             kpi_items.append(data)



        kpi_data = KpiName.objects.filter(organiztaion__unique_code=manager.unique_code)
        
        manager_kpi_met_data = 0
        kpi_wip = 0

        for kpi in kpi_data:

            if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__date__month=month,permormance_date__year=year).exists():
    
                manager_employee_kpi_data_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__date__month=month,permormance_date__year=year).aggregate(Sum('kpi_target'))

                manager_employee_kpi_data_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__date__month=month,permormance_date__year=year).aggregate(Sum('kpi_actual'))
                
                if not manager_employee_kpi_data_target['kpi_target__sum']:
                    pass
                else:
                    kpi_target = round(manager_employee_kpi_data_target['kpi_target__sum'],2)
                

                if not manager_employee_kpi_data_actual['kpi_actual__sum']:
                    pass
                else:
                    kpi_actual = round(manager_employee_kpi_data_actual['kpi_actual__sum'],2)
                
              
                if kpi_target <= kpi_actual:
                    manager_kpi_met_data +=1
                
                if kpi_target>kpi_actual:
                    kpi_wip +=1         


        kpi_data = KpiName.objects.filter(organiztaion__unique_code=manager.unique_code)

        for kpi in kpi_data:
          
            data ={}
            
            if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__date__month=month,permormance_date__year=year).exists():

                total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__date__month=month,permormance_date__year=year).aggregate(Sum('kpi_target'))
                total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__date__month=month,permormance_date__year=year).aggregate(Sum('kpi_actual'))
                
                if total_target['kpi_target__sum'] !=None or total_actual['kpi_actual__sum'] !=None: 
                    data['kpi_name']       = kpi.name
                    data['total_target']   = round(total_target['kpi_target__sum'],2)
                    data['total_actual']   = round(total_actual['kpi_actual__sum'],2)
                    data['total_gap']      = round(total_target['kpi_target__sum'] - total_actual['kpi_actual__sum'],2)
                
                    kpi_items.append(data)
            

        
    elif select_name=="all" and select_kpi=="all" and select_time_period=="ytd":
        year = current_date.year
        

        # manager_kpi_met_data = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_status=1,permormance_date__year=year).count() 
       
        # kpi_wip = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,permormance_date__year=year,kpi_status=0).count() 

        # for member in team_member_data:
        # kpi_wip = 0

        # team_campaigns = TeamCampaign.objects.filter(customer_accepted_id__in=team_member_data_id,updated_at__year=year,is_completed_by_manager=0)
        
        # team_campaigns = TeamAcceptCampaignHistory.objects.filter(customer_accepted_id__in=team_member_data_id,team_campaign__updated_at__year=year,team_campaign__is_completed_by_manager=0)

        # for campaign in team_campaigns:
        #     kpi_data = len(campaign.team_campaign.criteria_point.all())
        #     kpi_wip +=kpi_data

        # # for employee_email in team_member_email:
        # kpi_data = KpiName.objects.filter(organiztaion__unique_code=manager.unique_code)

        # for kpi in kpi_data:
        #     data ={}
            
        #     if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__year=year).exists():

        #         total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__year=year).aggregate(Sum('kpi_target'))
        #         total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__year=year).aggregate(Sum('kpi_actual'))

        #         data['kpi_name']       = kpi.name
        #         data['total_target']   = total_target['kpi_target__sum']
        #         data['total_actual']   = total_actual['kpi_actual__sum']
        #         data['total_gap']      = total_target['kpi_target__sum'] - total_actual['kpi_actual__sum']
                
        #         kpi_items.append(data)

        # kpi_data = KpiName.objects.filter(organiztaion__unique_code=manager.unique_code)

        # for kpi in kpi_data:
            
        #     data ={}
            
        #     if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,permormance_date__year=year,kpi_name_data__id=kpi.id).exists():

        #         total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__year=year).aggregate(Sum('kpi_target'))
        #         total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__year=year).aggregate(Sum('kpi_actual'))
                
        #         if total_target['kpi_target__sum'] and total_actual['kpi_actual__sum']: 
        #             data['kpi_name']       = kpi.name
        #             data['total_target']   = round(total_target['kpi_target__sum'],2)
        #             data['total_actual']   = round(total_actual['kpi_actual__sum'],2)
        #             data['total_gap']      = round(total_target['kpi_target__sum'] - total_actual['kpi_actual__sum'],2)
                
        #             kpi_items.append(data)



        kpi_data = KpiName.objects.filter(organiztaion__unique_code=manager.unique_code)
        
        manager_kpi_met_data = 0
        kpi_wip = 0

        for kpi in kpi_data:

            if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__year=year).exists():
    
                manager_employee_kpi_data_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__year=year).aggregate(Sum('kpi_target'))

                manager_employee_kpi_data_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__year=year).aggregate(Sum('kpi_actual'))
                
                if not manager_employee_kpi_data_target['kpi_target__sum']:
                    pass
                else:
                    kpi_target = round(manager_employee_kpi_data_target['kpi_target__sum'],2)
                

                if not manager_employee_kpi_data_actual['kpi_actual__sum']:
                    pass
                else:
                    kpi_actual = round(manager_employee_kpi_data_actual['kpi_actual__sum'],2)
                
              
                if kpi_target <= kpi_actual:
                    manager_kpi_met_data +=1
                
                if kpi_target>kpi_actual:
                    kpi_wip +=1         


        kpi_data = KpiName.objects.filter(organiztaion__unique_code=manager.unique_code)

        for kpi in kpi_data:
          
            data ={}
            
            if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__year=year).exists():

                total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__year=year).aggregate(Sum('kpi_target'))
                total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id,permormance_date__year=year).aggregate(Sum('kpi_actual'))
                
                if total_target['kpi_target__sum'] !=None or total_actual['kpi_actual__sum'] !=None: 
                    data['kpi_name']       = kpi.name
                    data['total_target']   = round(total_target['kpi_target__sum'],2)
                    data['total_actual']   = round(total_actual['kpi_actual__sum'],2)
                    data['total_gap']      = round(total_target['kpi_target__sum'] - total_actual['kpi_actual__sum'],2)
                
                    kpi_items.append(data)



    elif select_name=="all" and select_kpi!="all" and select_time_period=="all":
        
        # manager_kpi_met_data = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,kpi_status=1).count() 
       
        # kpi_wip = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,kpi_status=0).count() 

        # for member in team_member_data:
        #     # challenges = TeamChallenge.objects.filter(customer_accepted_id=member.id,kpi_name_id=select_kpi,is_completed_by_manager=0)
            
        #     challenges = TeamAcceptChallengeHistory.objects.filter(customer_accepted_id=member.id,team_challenge__kpi_name_id=select_kpi,team_challenge__is_completed_by_manager=0)

        #     kpi_wip = 0

        #     if challenges:
        #         for challenge in challenges:
        #             if challenge.team_challenge.start_time<=current_time and challenge.team_challenge.end_time>=current_time:
        #                 kpi_wip +=1
            
        #     # team_campaigns = TeamCampaign.objects.filter(customer_accepted_id=member.id,is_completed_by_manager=0)

        #     team_campaigns = TeamAcceptCampaignHistory.objects.filter(customer_accepted_id=member.id,team_campaign__is_completed_by_manager=0)

        #     for campaign in team_campaigns:
        #         if campaign.team_campaign.start_date<=current_date and campaign.team_campaign.end_date>=current_date:
        #             kpi_data = len(campaign.team_campaign.criteria_point.filter(kpi_id=select_kpi))
        #             kpi_wip +=kpi_data

        # for employee_email in team_member_email:

        # kpi_data = KpiName.objects.filter(id=select_kpi).first()

        # data ={}
        
        # if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi).exists():

        #     total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi).aggregate(Sum('kpi_target'))
        #     total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi).aggregate(Sum('kpi_actual'))

        #     data['kpi_name']       = kpi_data.name
        #     data['total_target']   = total_target['kpi_target__sum']
        #     data['total_actual']   = total_actual['kpi_actual__sum']
        #     data['total_gap']      = total_target['kpi_target__sum'] - total_actual['kpi_actual__sum']
            
        #     kpi_items.append(data)

        # if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id).exists():

        #     total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id).aggregate(Sum('kpi_target'))
        #     total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=kpi.id).aggregate(Sum('kpi_actual'))
            
        #     if total_target['kpi_target__sum'] and total_actual['kpi_actual__sum']: 
        #         data['kpi_name']       = kpi.name
        #         data['total_target']   = round(total_target['kpi_target__sum'],2)
        #         data['total_actual']   = round(total_actual['kpi_actual__sum'],2)
        #         data['total_gap']      = round(total_target['kpi_target__sum'] - total_actual['kpi_actual__sum'],2)
            
        #         kpi_items.append(data)
  
        kpi_data = KpiName.objects.filter(id=select_kpi).first()
        
        manager_kpi_met_data = 0

        kpi_wip = 0

      
        if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi).exists():

            manager_employee_kpi_data_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi).aggregate(Sum('kpi_target'))

            manager_employee_kpi_data_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi).aggregate(Sum('kpi_actual'))
            
            if not manager_employee_kpi_data_target['kpi_target__sum']:
                pass
            else:
                kpi_target = round(manager_employee_kpi_data_target['kpi_target__sum'],2)
            

            if not manager_employee_kpi_data_actual['kpi_actual__sum']:
                pass
            else:
                kpi_actual = round(manager_employee_kpi_data_actual['kpi_actual__sum'],2)
            
            
            if kpi_target <= kpi_actual:
                manager_kpi_met_data +=1
            
            if kpi_target>kpi_actual:
                kpi_wip +=1         

          
        data ={}
        
        if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi).exists():

            total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi).aggregate(Sum('kpi_target'))
            total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi).aggregate(Sum('kpi_actual'))
            
            if total_target['kpi_target__sum'] !=None or total_actual['kpi_actual__sum'] !=None: 
                data['kpi_name']       = kpi_data.name
                data['total_target']   = round(total_target['kpi_target__sum'],2)
                data['total_actual']   = round(total_actual['kpi_actual__sum'],2)
                data['total_gap']      = round(total_target['kpi_target__sum'] - total_actual['kpi_actual__sum'],2)
            
                kpi_items.append(data)


    elif select_name=="all" and select_kpi!="all" and select_time_period=="today":
    
        # manager_kpi_met_data = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_status=1,kpi_name_data__id=select_kpi,permormance_date__icontains=current_date).count() 
       
        # kpi_wip = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,kpi_status=0,permormance_date__icontains=current_date).count() 

        # for member in team_member_data:
        #     # challenges = TeamChallenge.objects.filter(customer_accepted_id=member.id,kpi_name_id=select_kpi,is_completed_by_manager=0)
            
        #     challenges = TeamAcceptChallengeHistory.objects.filter(customer_accepted_id=member.id,team_challenge__kpi_name_id=select_kpi,team_challenge__is_completed_by_manager=0)

        #     kpi_wip = 0

        #     if challenges:
        #         for challenge in challenges:
        #             if challenge.team_challenge.start_time<=current_time and challenge.team_challenge.end_time>=current_time:
        #                 kpi_wip +=1
            
        #     # team_campaigns = TeamCampaign.objects.filter(customer_accepted_id=member.id,is_completed_by_manager=0)

        #     team_campaigns = TeamAcceptCampaignHistory.objects.filter(customer_accepted_id=member.id,team_campaign__is_completed_by_manager=0)

        #     for campaign in team_campaigns:
        #         if campaign.team_campaign.start_date<=current_date and campaign.team_campaign.end_date>=current_date:
        #             kpi_data = len(campaign.team_campaign.criteria_point.filter(kpi_id=select_kpi))
        #             kpi_wip +=kpi_data

        # # for employee_email in team_member_email:
        # kpi_data = KpiName.objects.filter(id=select_kpi).first()

     
        # data ={}
        
        # if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__icontains=current_date).exists():

        #     total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__icontains=current_date).aggregate(Sum('kpi_target'))
        #     total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__icontains=current_date).aggregate(Sum('kpi_actual'))

        #     data['kpi_name']       = kpi.name
        #     data['total_target']   = total_target['kpi_target__sum']
        #     data['total_actual']   = total_actual['kpi_actual__sum']
        #     data['total_gap']      = total_target['kpi_target__sum'] - total_actual['kpi_actual__sum']
            
        #     kpi_items.append(data)
        

        kpi_data = KpiName.objects.filter(id=select_kpi).first()
        
        manager_kpi_met_data = 0

        kpi_wip = 0

      
        if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__icontains=current_date).exists():

            manager_employee_kpi_data_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__icontains=current_date).aggregate(Sum('kpi_target'))

            manager_employee_kpi_data_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__icontains=current_date).aggregate(Sum('kpi_actual'))
            
            if not manager_employee_kpi_data_target['kpi_target__sum']:
                pass
            else:
                kpi_target = round(manager_employee_kpi_data_target['kpi_target__sum'],2)
            

            if not manager_employee_kpi_data_actual['kpi_actual__sum']:
                pass
            else:
                kpi_actual = round(manager_employee_kpi_data_actual['kpi_actual__sum'],2)
            
            
            if kpi_target <= kpi_actual:
                manager_kpi_met_data +=1
            
            if kpi_target>kpi_actual:
                kpi_wip +=1         

          
        data ={}
        
        if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__icontains=current_date).exists():

            total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__icontains=current_date).aggregate(Sum('kpi_target'))
            total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__icontains=current_date).aggregate(Sum('kpi_actual'))
            
            if total_target['kpi_target__sum'] !=None or total_actual['kpi_actual__sum'] !=None: 
                data['kpi_name']       = kpi_data.name
                data['total_target']   = round(total_target['kpi_target__sum'],2)
                data['total_actual']   = round(total_actual['kpi_actual__sum'],2)
                data['total_gap']      = round(total_target['kpi_target__sum'] - total_actual['kpi_actual__sum'],2)
            
                kpi_items.append(data)



    elif select_name=="all" and select_kpi!="all" and select_time_period=="yesterday":
        yesterday_date = current_date-timedelta(days=1)
        
        # manager_kpi_met_data = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_status=1,kpi_name_data__id=select_kpi,permormance_date__icontains=yesterday_date).count() 
       
        # for member in team_member_data:
            # challenges = TeamChallenge.objects.filter(customer_accepted_id=member.id,kpi_name_id=select_kpi,is_completed_by_manager=0)
            
            # challenges = TeamAcceptChallengeHistory.objects.filter(customer_accepted_id=member.id,team_challenge__kpi_name_id=select_kpi,team_challenge__is_completed_by_manager=0)

            # kpi_wip = 0

            # if challenges:
            #     for challenge in challenges:
            #         if challenge.team_challenge.start_time<=yesterday_date and challenge.team_challenge.end_time>=yesterday_date:
            #             kpi_wip +=1
            
            # # team_campaigns = TeamCampaign.objects.filter(customer_accepted_id=member.id,is_completed_by_manager=0)
            
            # team_campaigns = TeamAcceptCampaignHistory.objects.filter(customer_accepted_id=member.id,team_campaign__is_completed_by_manager=0)

            # for campaign in team_campaigns:
            #     if campaign.team_campaign.start_date<=yesterday_date and campaign.team_campaign.end_date>=yesterday_date:
            #         kpi_data = len(campaign.team_campaign.criteria_point.filter(kpi_id=select_kpi))
            #         kpi_wip +=kpi_data

        # for employee_email in team_member_email:
        # kpi_data = KpiName.objects.filter(id=select_kpi).first()

     
        # data ={}
        
        # if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__icontains=yesterday_date).exists():

        #     total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__icontains=yesterday_date).aggregate(Sum('kpi_target'))
        #     total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__icontains=yesterday_date).aggregate(Sum('kpi_actual'))

        #     data['kpi_name']       = kpi.name
        #     data['total_target']   = total_target['kpi_target__sum']
        #     data['total_actual']   = total_actual['kpi_actual__sum']
        #     data['total_gap']      = total_target['kpi_target__sum'] - total_actual['kpi_actual__sum']
            
        #     kpi_items.append(data)



        kpi_data = KpiName.objects.filter(id=select_kpi).first()
        
        manager_kpi_met_data = 0

        kpi_wip = 0

      
        if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__icontains=yesterday_date).exists():

            manager_employee_kpi_data_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__icontains=yesterday_date).aggregate(Sum('kpi_target'))

            manager_employee_kpi_data_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__icontains=yesterday_date).aggregate(Sum('kpi_actual'))
            
            if not manager_employee_kpi_data_target['kpi_target__sum']:
                pass
            else:
                kpi_target = round(manager_employee_kpi_data_target['kpi_target__sum'],2)
            

            if not manager_employee_kpi_data_actual['kpi_actual__sum']:
                pass
            else:
                kpi_actual = round(manager_employee_kpi_data_actual['kpi_actual__sum'],2)
            
            
            if kpi_target <= kpi_actual:
                manager_kpi_met_data +=1
            
            if kpi_target>kpi_actual:
                kpi_wip +=1         

          
        data ={}
        
        if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__icontains=yesterday_date).exists():

            total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__icontains=yesterday_date).aggregate(Sum('kpi_target'))
            total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__icontains=yesterday_date).aggregate(Sum('kpi_actual'))
            
            if total_target['kpi_target__sum'] !=None or total_actual['kpi_actual__sum'] !=None: 
                data['kpi_name']       = kpi_data.name
                data['total_target']   = round(total_target['kpi_target__sum'],2)
                data['total_actual']   = round(total_actual['kpi_actual__sum'],2)
                data['total_gap']      = round(total_target['kpi_target__sum'] - total_actual['kpi_actual__sum'],2)
            
                kpi_items.append(data)
    

    elif select_name=="all" and select_kpi!="all" and select_time_period=="wtd":
        end_date   = current_date
        start_date = end_date -timedelta(days=7)
        
        # manager_kpi_met_data = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,kpi_status=1,permormance_date__date__range=[start_date,end_date]).count() 

       
        # # for member in team_member_data:
       
        # # team_campaigns = TeamCampaign.objects.filter(customer_accepted_id__in=team_member_data_id,is_completed_by_manager=0)

        # team_campaigns = TeamAcceptCampaignHistory.objects.filter(customer_accepted_id__in=team_member_data_id,team_campaign__is_completed_by_manager=0)

        # while start_date <= end_date:

        #     for campaign in team_campaigns:
        #         if campaign.team_campaign.start_date<=start_date and campaign.team_campaign.end_date>=start_date:
        #             kpi_data = len(campaign.team_campaign.criteria_point.filter(kpi_id=select_kpi))
        #             kpi_wip +=kpi_data
        #     start_date  = start_date + timedelta(days=1) 

        # # for employee_email in team_member_email:
        # kpi_data = KpiName.objects.filter(id=select_kpi).first()


        # data ={}
        
        # if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__date__range=[start_date,end_date]).exists():

        #     total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__date__range=[start_date,end_date]).aggregate(Sum('kpi_target'))
        #     total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__date__range=[start_date,end_date]).aggregate(Sum('kpi_actual'))

        #     data['kpi_name']       = kpi.name
        #     data['total_target']   = total_target['kpi_target__sum']
        #     data['total_actual']   = total_actual['kpi_actual__sum']
        #     data['total_gap']      = total_target['kpi_target__sum'] - total_actual['kpi_actual__sum']
            
        #     kpi_items.append(data)


        kpi_data = KpiName.objects.filter(id=select_kpi).first()
        
        manager_kpi_met_data = 0

        kpi_wip = 0

      
        if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__date__range=[start_date,end_date]).exists():

            manager_employee_kpi_data_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__date__range=[start_date,end_date]).aggregate(Sum('kpi_target'))

            manager_employee_kpi_data_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__date__range=[start_date,end_date]).aggregate(Sum('kpi_actual'))
            
            if not manager_employee_kpi_data_target['kpi_target__sum']:
                pass
            else:
                kpi_target = round(manager_employee_kpi_data_target['kpi_target__sum'],2)
            

            if not manager_employee_kpi_data_actual['kpi_actual__sum']:
                pass
            else:
                kpi_actual = round(manager_employee_kpi_data_actual['kpi_actual__sum'],2)
            
            
            if kpi_target <= kpi_actual:
                manager_kpi_met_data +=1
            
            if kpi_target>kpi_actual:
                kpi_wip +=1         

          
        data ={}
        
        if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__date__range=[start_date,end_date]).exists():

            total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__date__range=[start_date,end_date]).aggregate(Sum('kpi_target'))
            total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__date__range=[start_date,end_date]).aggregate(Sum('kpi_actual'))
            
            if total_target['kpi_target__sum'] !=None or total_actual['kpi_actual__sum'] !=None: 
                data['kpi_name']       = kpi_data.name
                data['total_target']   = round(total_target['kpi_target__sum'],2)
                data['total_actual']   = round(total_actual['kpi_actual__sum'],2)
                data['total_gap']      = round(total_target['kpi_target__sum'] - total_actual['kpi_actual__sum'],2)
            
                kpi_items.append(data)
    

        
    elif select_name=="all" and select_kpi!="all" and select_time_period=="mtd":
        month = current_date.month
        year = current_date.year

        # manager_kpi_met_data = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_status=1,kpi_name_data__id=select_kpi,permormance_date__month=month,permormance_date__year=year).count() 
       
        # # for member in team_member_data:
        # kpi_wip = 0

        # # team_campaigns = TeamCampaign.objects.filter(customer_accepted_id__in=team_member_data_id,updated_at__month=month,updated_at__year=year,is_completed_by_manager=0)
        
        # team_campaigns = TeamAcceptCampaignHistory.objects.filter(customer_accepted_id__in=team_member_data_id,team_campaign__updated_at__month=month,team_campaign__updated_at__year=year,team_campaign__is_completed_by_manager=0)

        # for campaign in team_campaigns:
        #     kpi_data = len(campaign.team_campaign.criteria_point.filter(kpi_id=select_kpi))
        #     kpi_wip +=kpi_data

        # # for employee_email in team_member_email:
        # kpi_data = KpiName.objects.filter(id=select_kpi).first()

        # data ={}
        
        # if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__month=month,performance_date__year=year).exists():

        #     total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__month=month,permormance_date__year=year).aggregate(Sum('kpi_target'))
        #     total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__month=month,permormance_date__year=year).aggregate(Sum('kpi_actual'))

        #     data['kpi_name']       = kpi.name
        #     data['total_target']   = total_target['kpi_target__sum']
        #     data['total_actual']   = total_actual['kpi_actual__sum']
        #     data['total_gap']      = total_target['kpi_target__sum'] - total_actual['kpi_actual__sum']
            
        #     kpi_items.append(data)

        kpi_data = KpiName.objects.filter(id=select_kpi).first()
        
        manager_kpi_met_data = 0

        kpi_wip = 0

      
        if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__month=month,permormance_date__year=year).exists():

            manager_employee_kpi_data_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__month=month,permormance_date__year=year).aggregate(Sum('kpi_target'))

            manager_employee_kpi_data_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__month=month,permormance_date__year=year).aggregate(Sum('kpi_actual'))
            
            if not manager_employee_kpi_data_target['kpi_target__sum']:
                pass
            else:
                kpi_target = round(manager_employee_kpi_data_target['kpi_target__sum'],2)
            

            if not manager_employee_kpi_data_actual['kpi_actual__sum']:
                pass
            else:
                kpi_actual = round(manager_employee_kpi_data_actual['kpi_actual__sum'],2)
            
            
            if kpi_target <= kpi_actual:
                manager_kpi_met_data +=1
            
            if kpi_target>kpi_actual:
                kpi_wip +=1         

          
        data ={}
        
        if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__month=month,permormance_date__year=year).exists():

            total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__month=month,permormance_date__year=year).aggregate(Sum('kpi_target'))
            total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__month=month,permormance_date__year=year).aggregate(Sum('kpi_actual'))
            
            if total_target['kpi_target__sum'] !=None or total_actual['kpi_actual__sum'] !=None: 
                data['kpi_name']       = kpi_data.name
                data['total_target']   = round(total_target['kpi_target__sum'],2)
                data['total_actual']   = round(total_actual['kpi_actual__sum'],2)
                data['total_gap']      = round(total_target['kpi_target__sum'] - total_actual['kpi_actual__sum'],2)
            
                kpi_items.append(data)
    



    elif select_name=="all" and select_kpi!="all" and select_time_period=="ytd":
        year = current_date.year
        
   
        # manager_kpi_met_data = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_status=1,kpi_name_data__id=select_kpi,permormance_date__year=year).count() 
       
        # # for member in team_member_data:
        # kpi_wip = 0

        # # team_campaigns = TeamCampaign.objects.filter(customer_accepted_id__in=team_member_data_id,updated_at__year=year,is_completed_by_manager=0)
        
        # team_campaigns = TeamAcceptCampaignHistory.objects.filter(customer_accepted_id__in=team_member_data_id,team_campaign__updated__year=year,team_campaign__is_completed_by_manager=0)

        # for campaign in team_campaigns:
        #     kpi_data = len(campaign.team_campaign.criteria_point.filter(kpi_id=select_kpi))
        #     kpi_wip +=kpi_data

        # # for employee_email in team_member_email:
        # kpi_data = KpiName.objects.filter(id=select_kpi).first()

        # data ={}
        
        # if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,performance_date__year=year).exists():

        #     total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__year=year).aggregate(Sum('kpi_target'))
        #     total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__year=year).aggregate(Sum('kpi_actual'))

        #     data['kpi_name']       = kpi.name
        #     data['total_target']   = total_target['kpi_target__sum']
        #     data['total_actual']   = total_actual['kpi_actual__sum']
        #     data['total_gap']      = total_target['kpi_target__sum'] - total_actual['kpi_actual__sum']
            
        #     kpi_items.append(data)


        kpi_data = KpiName.objects.filter(id=select_kpi).first()
        
        manager_kpi_met_data = 0

        kpi_wip = 0

      
        if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__year=year).exists():

            manager_employee_kpi_data_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__year=year).aggregate(Sum('kpi_target'))

            manager_employee_kpi_data_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__year=year).aggregate(Sum('kpi_actual'))
            
            if not manager_employee_kpi_data_target['kpi_target__sum']:
                pass
            else:
                kpi_target = round(manager_employee_kpi_data_target['kpi_target__sum'],2)
            

            if not manager_employee_kpi_data_actual['kpi_actual__sum']:
                pass
            else:
                kpi_actual = round(manager_employee_kpi_data_actual['kpi_actual__sum'],2)
            
            
            if kpi_target <= kpi_actual:
                manager_kpi_met_data +=1
            
            if kpi_target>kpi_actual:
                kpi_wip +=1         

          
        data ={}
        
        if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__year=year).exists():

            total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__year=year).aggregate(Sum('kpi_target'))
            total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=team_member_email,kpi_name_data__id=select_kpi,permormance_date__year=year).aggregate(Sum('kpi_actual'))
            
            if total_target['kpi_target__sum'] !=None or total_actual['kpi_actual__sum'] !=None: 
                data['kpi_name']       = kpi_data.name
                data['total_target']   = round(total_target['kpi_target__sum'],2)
                data['total_actual']   = round(total_actual['kpi_actual__sum'],2)
                data['total_gap']      = round(total_target['kpi_target__sum'] - total_actual['kpi_actual__sum'],2)
            
                kpi_items.append(data)
    


    elif select_name!="all" and select_kpi=="all" and select_time_period=="all":

        # manager_kpi_met_data = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_status=1).count() 
       
    
        # # challenges = TeamChallenge.objects.filter(customer_accepted_id=employee_data.id,is_completed_by_manager=0)
        
        # challenges = TeamAcceptChallengeHistory.objects.filter(customer_accepted_id=employee_data.id,team_challenge__is_completed_by_manager=0)


        # kpi_wip = 0

        # if challenges:
        #     for challenge in challenges:
        #         if challenge.team_challenge.start_time<=current_time and challenge.team_challenge.end_time>=current_time:
        #             kpi_wip +=1
            
        #     # team_campaigns = TeamCampaign.objects.filter(customer_accepted_id=employee_data.id,is_completed_by_manager=0)

        #     team_campaigns = TeamAcceptCampaignHistory.objects.filter(customer_accepted_id=employee_data.id,team_campaign__is_completed_by_manager=0)

        #     for campaign in team_campaigns:
        #         if campaign.team_campaign.start_date<=current_date and campaign.team_campaign.end_date>=current_date:
        #             kpi_data = len(campaign.team_campaign.criteria_point.all())
        #             kpi_wip +=kpi_data

        # # for employee_email in team_member_email:
        # kpi_data = KpiName.objects.filter(organiztaion__unique_code=manager.unique_code)

        # for kpi in kpi_data:
        #     data ={}
            
        #     if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id).exists():

        #         total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id).aggregate(Sum('kpi_target'))
        #         total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id).aggregate(Sum('kpi_actual'))

        #         data['kpi_name']       = kpi.name
        #         data['total_target']   = total_target['kpi_target__sum']
        #         data['total_actual']   = total_actual['kpi_actual__sum']
        #         data['total_gap']      = total_target['kpi_target__sum'] - total_actual['kpi_actual__sum']
                
        #         kpi_items.append(data)


        kpi_data = KpiName.objects.filter(organiztaion__unique_code=manager.unique_code)
        
        manager_kpi_met_data = 0
        kpi_wip = 0

        for kpi in kpi_data:

            if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id).exists():
    
                manager_employee_kpi_data_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id).aggregate(Sum('kpi_target'))

                manager_employee_kpi_data_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id).aggregate(Sum('kpi_actual'))
                
                if not manager_employee_kpi_data_target['kpi_target__sum']:
                    pass
                else:
                    kpi_target = round(manager_employee_kpi_data_target['kpi_target__sum'],2)
                

                if not manager_employee_kpi_data_actual['kpi_actual__sum']:
                    pass
                else:
                    kpi_actual = round(manager_employee_kpi_data_actual['kpi_actual__sum'],2)
                
              
                if kpi_target <= kpi_actual:
                    manager_kpi_met_data +=1
                
                if kpi_target>kpi_actual:
                    kpi_wip +=1         


        kpi_data = KpiName.objects.filter(organiztaion__unique_code=manager.unique_code)

        for kpi in kpi_data:
          
            data ={}
            
            if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id).exists():

                total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id).aggregate(Sum('kpi_target'))
                total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id).aggregate(Sum('kpi_actual'))
                
                if total_target['kpi_target__sum'] !=None or total_actual['kpi_actual__sum'] !=None: 
                    data['kpi_name']       = kpi.name
                    data['total_target']   = round(total_target['kpi_target__sum'],2)
                    data['total_actual']   = round(total_actual['kpi_actual__sum'],2)
                    data['total_gap']      = round(total_target['kpi_target__sum'] - total_actual['kpi_actual__sum'],2)
                
                    kpi_items.append(data)

 
    elif select_name!="all" and select_kpi=="all" and select_time_period=="today":
        
        # manager_kpi_met_data = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_status=1,permormance_date__icontains=current_date).count() 
       
    
        # # challenges = TeamChallenge.objects.filter(customer_accepted_id=employee_data.id,is_completed_by_manager=0)
        
        # challenges = TeamAcceptChallengeHistory.objects.filter(customer_accepted_id=employee_data.id,team_challenge__is_completed_by_manager=0)


        # kpi_wip = 0

        # if challenges:
        #     for challenge in challenges:
        #         if challenge.team_challenge.start_time<=current_time and challenge.team_challenge.end_time>=current_time:
        #             kpi_wip +=1
            
        #     # team_campaigns = TeamCampaign.objects.filter(customer_accepted_id=employee_data.id,is_completed_by_manager=0)

        #     team_campaigns = TeamAcceptCampaignHistory.objects.filter(customer_accepted_id=employee_data.id,team_campaign__is_completed_by_manager=0)

        #     for campaign in team_campaigns:
        #         if campaign.team_campaign.start_date<=current_date and campaign.team_campaign.end_date>=current_date:
        #             kpi_data = len(campaign.team_campaign.criteria_point.all())
        #             kpi_wip +=kpi_data

        # for employee_email in team_member_email:
        # kpi_data = KpiName.objects.filter(organiztaion__unique_code=manager.unique_code)

        # for kpi in kpi_data:
        #     data ={}
            
        #     if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__icontains=current_date).exists():

        #         total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__icontains=current_date).aggregate(Sum('kpi_target'))
        #         total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__icontains=current_date).aggregate(Sum('kpi_actual'))

        #         data['kpi_name']       = kpi.name
        #         data['total_target']   = total_target['kpi_target__sum']
        #         data['total_actual']   = total_actual['kpi_actual__sum']
        #         data['total_gap']      = total_target['kpi_target__sum'] - total_actual['kpi_actual__sum']
                
        #         kpi_items.append(data)



        kpi_data = KpiName.objects.filter(organiztaion__unique_code=manager.unique_code)
        
        manager_kpi_met_data = 0
        kpi_wip = 0

        for kpi in kpi_data:

            if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__icontains=current_date).exists():
    
                manager_employee_kpi_data_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__icontains=current_date).aggregate(Sum('kpi_target'))

                manager_employee_kpi_data_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__icontains=current_date).aggregate(Sum('kpi_actual'))
                
                if not manager_employee_kpi_data_target['kpi_target__sum']:
                    pass
                else:
                    kpi_target = round(manager_employee_kpi_data_target['kpi_target__sum'],2)
                

                if not manager_employee_kpi_data_actual['kpi_actual__sum']:
                    pass
                else:
                    kpi_actual = round(manager_employee_kpi_data_actual['kpi_actual__sum'],2)
                
              
                if kpi_target <= kpi_actual:
                    manager_kpi_met_data +=1
                
                if kpi_target>kpi_actual:
                    kpi_wip +=1         


        kpi_data = KpiName.objects.filter(organiztaion__unique_code=manager.unique_code)

        for kpi in kpi_data:
          
            data ={}
            
            if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__icontains=current_date).exists():

                total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__icontains=current_date).aggregate(Sum('kpi_target'))
                total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__icontains=current_date).aggregate(Sum('kpi_actual'))
                
                if total_target['kpi_target__sum'] !=None or total_actual['kpi_actual__sum'] !=None: 
                    data['kpi_name']       = kpi.name
                    data['total_target']   = round(total_target['kpi_target__sum'],2)
                    data['total_actual']   = round(total_actual['kpi_actual__sum'],2)
                    data['total_gap']      = round(total_target['kpi_target__sum'] - total_actual['kpi_actual__sum'],2)
                
                    kpi_items.append(data)


    elif select_name!="all" and select_kpi=="all" and select_time_period=="yesterday":
        yesterday_date = current_date-timedelta(days=1)

        # manager_kpi_met_data = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_status=1,permormance_date__icontains=yesterday_date).count() 
       
    
        # kpi_wip = 0

        # # team_campaigns = TeamCampaign.objects.filter(customer_accepted_id=employee_data.id,is_completed_by_manager=0)

        # team_campaigns = TeamAcceptCampaignHistory.objects.filter(customer_accepted_id=employee_data.id,team_campaign__is_completed_by_manager=0)

        # for campaign in team_campaigns:
        #     if campaign.team_campaign.start_date<=yesterday_date and campaign.team_campaign.end_date>=yesterday_date:
        #         kpi_data = len(campaign.team_campaign.criteria_point.all())
        #         kpi_wip +=kpi_data

        # # for employee_email in team_member_email:
        # kpi_data = KpiName.objects.filter(organiztaion__unique_code=manager.unique_code)

        # for kpi in kpi_data:
        #     data ={}
            
        #     if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__icontains=yesterday_date).exists():

        #         total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__icontains=yesterday_date).aggregate(Sum('kpi_target'))
        #         total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__icontains=yesterday_date).aggregate(Sum('kpi_actual'))

        #         data['kpi_name']       = kpi.name
        #         data['total_target']   = total_target['kpi_target__sum']
        #         data['total_actual']   = total_actual['kpi_actual__sum']
        #         data['total_gap']      = total_target['kpi_target__sum'] - total_actual['kpi_actual__sum']
                
        #         kpi_items.append(data)


        kpi_data = KpiName.objects.filter(organiztaion__unique_code=manager.unique_code)
        
        manager_kpi_met_data = 0
        kpi_wip = 0

        for kpi in kpi_data:

            if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__icontains=yesterday_date).exists():
    
                manager_employee_kpi_data_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__icontains=yesterday_date).aggregate(Sum('kpi_target'))

                manager_employee_kpi_data_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__icontains=yesterday_date).aggregate(Sum('kpi_actual'))
                
                if not manager_employee_kpi_data_target['kpi_target__sum']:
                    pass
                else:
                    kpi_target = round(manager_employee_kpi_data_target['kpi_target__sum'],2)
                

                if not manager_employee_kpi_data_actual['kpi_actual__sum']:
                    pass
                else:
                    kpi_actual = round(manager_employee_kpi_data_actual['kpi_actual__sum'],2)
                
              
                if kpi_target <= kpi_actual:
                    manager_kpi_met_data +=1
                
                if kpi_target>kpi_actual:
                    kpi_wip +=1         


        kpi_data = KpiName.objects.filter(organiztaion__unique_code=manager.unique_code)

        for kpi in kpi_data:
          
            data ={}
            
            if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__icontains=yesterday_date).exists():

                total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__icontains=yesterday_date).aggregate(Sum('kpi_target'))
                total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__icontains=yesterday_date).aggregate(Sum('kpi_actual'))
                
                if total_target['kpi_target__sum'] !=None or total_actual['kpi_actual__sum'] !=None: 
                    data['kpi_name']       = kpi.name
                    data['total_target']   = round(total_target['kpi_target__sum'],2)
                    data['total_actual']   = round(total_actual['kpi_actual__sum'],2)
                    data['total_gap']      = round(total_target['kpi_target__sum'] - total_actual['kpi_actual__sum'],2)
                
                    kpi_items.append(data)

 
    elif select_name!="all" and select_kpi=="all" and select_time_period=="wtd":
        end_date   = current_date
        start_date = end_date -timedelta(days=7)
        
        # manager_kpi_met_data = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_status=1,permormance_date__date__range=[start_date,end_date]).count() 
       
        # kpi_wip = 0


        # while start_date <= end_date:
        #     # team_campaigns = TeamCampaign.objects.filter(customer_accepted_id=employee_data.id,is_completed_by_manager=0)

        #     team_campaigns = TeamAcceptCampaignHistory.objects.filter(customer_accepted_id=employee_data.id,team_campaign__is_completed_by_manager=0)

        #     for campaign in team_campaigns:
        #         if campaign.team_campaign.start_date<=start_date and campaign.team_campaign.end_date>=start_date:
        #             kpi_data = len(campaign.team_campaign.criteria_point.all())
        #             kpi_wip +=kpi_data
        #     start_date  = start_date + timedelta(days=1) 

        # # for employee_email in team_member_email:
        # kpi_data = KpiName.objects.filter(organiztaion__unique_code=manager.unique_code)
        
        # for kpi in kpi_data:
        #     data ={}
            
        #     if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__date__range=[start_date,end_date]).exists():

        #         total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__date__range=[start_date,end_date]).aggregate(Sum('kpi_target'))
        #         total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__date__range=[start_date,end_date]).aggregate(Sum('kpi_actual'))

        #         data['kpi_name']       = kpi.name
        #         data['total_target']   = total_target['kpi_target__sum']
        #         data['total_actual']   = total_actual['kpi_actual__sum']
        #         data['total_gap']      = total_target['kpi_target__sum'] - total_actual['kpi_actual__sum']
                
        #         kpi_items.append(data)


        kpi_data = KpiName.objects.filter(organiztaion__unique_code=manager.unique_code)
        
        manager_kpi_met_data = 0
        kpi_wip = 0

        for kpi in kpi_data:

            if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__date__range=[start_date,end_date]).exists():
    
                manager_employee_kpi_data_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__date__range=[start_date,end_date]).aggregate(Sum('kpi_target'))

                manager_employee_kpi_data_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__date__range=[start_date,end_date]).aggregate(Sum('kpi_actual'))
                
                if not manager_employee_kpi_data_target['kpi_target__sum']:
                    pass
                else:
                    kpi_target = round(manager_employee_kpi_data_target['kpi_target__sum'],2)
                

                if not manager_employee_kpi_data_actual['kpi_actual__sum']:
                    pass
                else:
                    kpi_actual = round(manager_employee_kpi_data_actual['kpi_actual__sum'],2)
                
              
                if kpi_target <= kpi_actual:
                    manager_kpi_met_data +=1
                
                if kpi_target>kpi_actual:
                    kpi_wip +=1         


        kpi_data = KpiName.objects.filter(organiztaion__unique_code=manager.unique_code)

        for kpi in kpi_data:
          
            data ={}
            
            if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__date__range=[start_date,end_date]).exists():

                total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__date__range=[start_date,end_date]).aggregate(Sum('kpi_target'))
                total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__date__range=[start_date,end_date]).aggregate(Sum('kpi_actual'))
                
                if total_target['kpi_target__sum'] !=None or total_actual['kpi_actual__sum'] !=None: 
                    data['kpi_name']       = kpi.name
                    data['total_target']   = round(total_target['kpi_target__sum'],2)
                    data['total_actual']   = round(total_actual['kpi_actual__sum'],2)
                    data['total_gap']      = round(total_target['kpi_target__sum'] - total_actual['kpi_actual__sum'],2)
                
                    kpi_items.append(data)


    elif select_name!="all" and select_kpi=="all" and select_time_period=="mtd":
        month = current_date.month
        year = current_date.year

        # manager_kpi_met_data = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_status=1,permormance_date__month=month,permormance_date__year=year).count() 
       
        # kpi_wip = 0

     
        # # team_campaigns = TeamCampaign.objects.filter(customer_accepted_id=employee_data.id,updated_at__month=month,updated_at__year=year,is_completed_by_manager=0)

        # team_campaigns = TeamAcceptCampaignHistory.objects.filter(customer_accepted_id=employee_data.id,team_campaign__updated_at__month=month,team_campaign__updated_at__year=year,team_campaign__is_completed_by_manager=0)

        # for campaign in team_campaigns:
        #         kpi_data = len(campaign.team_campaign.criteria_point.all())
        #         kpi_wip +=kpi_data
     
        # # for employee_email in team_member_email:
        # kpi_data = KpiName.objects.filter(organiztaion__unique_code=manager.unique_code)
        
        # for kpi in kpi_data:
        #     data ={}
            
        #     if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__month=month,permormance_date__year=year).exists():

        #         total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__month=month,permormance_date__year=year).aggregate(Sum('kpi_target'))
        #         total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__month=month,permormance_date__year=year).aggregate(Sum('kpi_actual'))

        #         data['kpi_name']       = kpi.name
        #         data['total_target']   = total_target['kpi_target__sum']
        #         data['total_actual']   = total_actual['kpi_actual__sum']
        #         data['total_gap']      = total_target['kpi_target__sum'] - total_actual['kpi_actual__sum']
                
        #         kpi_items.append(data)


        kpi_data = KpiName.objects.filter(organiztaion__unique_code=manager.unique_code)
        
        manager_kpi_met_data = 0
        kpi_wip = 0

        for kpi in kpi_data:

            if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__month=month,permormance_date__year=year).exists():
    
                manager_employee_kpi_data_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__month=month,permormance_date__year=year).aggregate(Sum('kpi_target'))

                manager_employee_kpi_data_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__month=month,permormance_date__year=year).aggregate(Sum('kpi_actual'))
                
                if not manager_employee_kpi_data_target['kpi_target__sum']:
                    pass
                else:
                    kpi_target = round(manager_employee_kpi_data_target['kpi_target__sum'],2)
                

                if not manager_employee_kpi_data_actual['kpi_actual__sum']:
                    pass
                else:
                    kpi_actual = round(manager_employee_kpi_data_actual['kpi_actual__sum'],2)
                
              
                if kpi_target <= kpi_actual:
                    manager_kpi_met_data +=1
                
                if kpi_target>kpi_actual:
                    kpi_wip +=1         


        kpi_data = KpiName.objects.filter(organiztaion__unique_code=manager.unique_code)

        for kpi in kpi_data:
          
            data ={}
            
            if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__month=month,permormance_date__year=year).exists():

                total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__month=month,permormance_date__year=year).aggregate(Sum('kpi_target'))
                total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__month=month,permormance_date__year=year).aggregate(Sum('kpi_actual'))
                
                if total_target['kpi_target__sum'] !=None or total_actual['kpi_actual__sum'] !=None: 
                    data['kpi_name']       = kpi.name
                    data['total_target']   = round(total_target['kpi_target__sum'],2)
                    data['total_actual']   = round(total_actual['kpi_actual__sum'],2)
                    data['total_gap']      = round(total_target['kpi_target__sum'] - total_actual['kpi_actual__sum'],2)
                
                    kpi_items.append(data)


    elif select_name!="all" and select_kpi=="all" and select_time_period=="ytd":
        year = current_date.year

        # manager_kpi_met_data = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_status=1,permormance_date__year=year).count() 
       
        # kpi_wip = 0

     
        # # team_campaigns = TeamCampaign.objects.filter(customer_accepted_id=employee_data.id,updated_at__year=year,is_completed_by_manager=0)

        # team_campaigns = TeamAcceptCampaignHistory.objects.filter(customer_accepted_id=employee_data.id,team_campaign__updated_at__year=year,team_campaign__is_completed_by_manager=0)

        # for campaign in team_campaigns:
        #         kpi_data = len(campaign.team_campaign.criteria_point.all())
        #         kpi_wip +=kpi_data
     
        # # for employee_email in team_member_email:
        # kpi_data = KpiName.objects.filter(organiztaion__unique_code=manager.unique_code)
        
        # for kpi in kpi_data:
        #     data ={}
            
        #     if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__year=year).exists():

        #         total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__year=year).aggregate(Sum('kpi_target'))
        #         total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__year=year).aggregate(Sum('kpi_actual'))

        #         data['kpi_name']       = kpi.name
        #         data['total_target']   = total_target['kpi_target__sum']
        #         data['total_actual']   = total_actual['kpi_actual__sum']
        #         data['total_gap']      = total_target['kpi_target__sum'] - total_actual['kpi_actual__sum']
                
        #         kpi_items.append(data)


        kpi_data = KpiName.objects.filter(organiztaion__unique_code=manager.unique_code)
        
        manager_kpi_met_data = 0
        kpi_wip = 0

        for kpi in kpi_data:

            if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__year=year).exists():
    
                manager_employee_kpi_data_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__year=year).aggregate(Sum('kpi_target'))

                manager_employee_kpi_data_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__year=year).aggregate(Sum('kpi_actual'))
                
                if not manager_employee_kpi_data_target['kpi_target__sum']:
                    pass
                else:
                    kpi_target = round(manager_employee_kpi_data_target['kpi_target__sum'],2)
                

                if not manager_employee_kpi_data_actual['kpi_actual__sum']:
                    pass
                else:
                    kpi_actual = round(manager_employee_kpi_data_actual['kpi_actual__sum'],2)
                
              
                if kpi_target <= kpi_actual:
                    manager_kpi_met_data +=1
                
                if kpi_target>kpi_actual:
                    kpi_wip +=1         


        kpi_data = KpiName.objects.filter(organiztaion__unique_code=manager.unique_code)

        for kpi in kpi_data:
          
            data ={}
            
            if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__year=year).exists():

                total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__year=year).aggregate(Sum('kpi_target'))
                total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=kpi.id,permormance_date__year=year).aggregate(Sum('kpi_actual'))
                
                if total_target['kpi_target__sum'] !=None or total_actual['kpi_actual__sum'] !=None: 
                    data['kpi_name']       = kpi.name
                    data['total_target']   = round(total_target['kpi_target__sum'],2)
                    data['total_actual']   = round(total_actual['kpi_actual__sum'],2)
                    data['total_gap']      = round(total_target['kpi_target__sum'] - total_actual['kpi_actual__sum'],2)
                
                    kpi_items.append(data)

      
    elif select_name!="all" and select_kpi!="all" and select_time_period=="all":

        # manager_kpi_met_data = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data=select_kpi,kpi_status=1).count() 
       
     
        # # challenges = TeamChallenge.objects.filter(customer_accepted_id=employee_data.id,kpi_name_id=select_kpi,is_completed_by_manager=0)

        # challenges = TeamAcceptChallengeHistory.objects.filter(customer_accepted_id=employee_data.id,team_challenge__kpi_name_id=select_kpi,team_challenge__is_completed_by_manager=0)

        # kpi_wip = 0

        # if challenges:
        #     for challenge in challenges:
        #         if challenge.team_challenge.start_time<=current_time and challenge.team_challenge.end_time>=current_time:
        #             kpi_wip +=1
        
        # # team_campaigns = TeamCampaign.objects.filter(customer_accepted_id=employee_data.id,is_completed_by_manager=0)

        # team_campaigns = TeamAcceptCampaignHistory.objects.filter(customer_accepted_id=employee_data.id,team_campaign__is_completed_by_manager=0)

        # for campaign in team_campaigns:
        #     if campaign.team_campaign.start_date<=current_date and campaign.team_campaign.end_date>=current_date:
        #         kpi_data = len(campaign.team_campaign.criteria_point.filter(kpi_id=select_kpi))
        #         kpi_wip +=kpi_data

        # # for employee_email in team_member_email:
        # kpi_data = KpiName.objects.filter(id=select_kpi).first()

        # data ={}
        
        # if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi).exists():

        #     total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi).aggregate(Sum('kpi_target'))
        #     total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi).aggregate(Sum('kpi_actual'))

        #     data['kpi_name']       = kpi_data.name
        #     data['total_target']   = total_target['kpi_target__sum']
        #     data['total_actual']   = total_actual['kpi_actual__sum']
        #     data['total_gap']      = total_target['kpi_target__sum'] - total_actual['kpi_actual__sum']
            
        #     kpi_items.append(data)
    

        kpi_data = KpiName.objects.filter(id=select_kpi).first()
        
        manager_kpi_met_data = 0

        kpi_wip = 0

      
        if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi).exists():

            manager_employee_kpi_data_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi).aggregate(Sum('kpi_target'))

            manager_employee_kpi_data_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi).aggregate(Sum('kpi_actual'))
            
            if not manager_employee_kpi_data_target['kpi_target__sum']:
                pass
            else:
                kpi_target = round(manager_employee_kpi_data_target['kpi_target__sum'],2)
            

            if not manager_employee_kpi_data_actual['kpi_actual__sum']:
                pass
            else:
                kpi_actual = round(manager_employee_kpi_data_actual['kpi_actual__sum'],2)
            
            
            if kpi_target <= kpi_actual:
                manager_kpi_met_data +=1
            
            if kpi_target>kpi_actual:
                kpi_wip +=1         

          
        data ={}
        
        if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi).exists():

            total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi).aggregate(Sum('kpi_target'))
            total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi).aggregate(Sum('kpi_actual'))
            
            if total_target['kpi_target__sum'] !=None or total_actual['kpi_actual__sum'] !=None: 
                data['kpi_name']       = kpi_data.name
                data['total_target']   = round(total_target['kpi_target__sum'],2)
                data['total_actual']   = round(total_actual['kpi_actual__sum'],2)
                data['total_gap']      = round(total_target['kpi_target__sum'] - total_actual['kpi_actual__sum'],2)
            
                kpi_items.append(data)
    

    elif select_name!="all" and select_kpi!="all" and select_time_period=="today":
        # manager_kpi_met_data = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data=select_kpi,kpi_status=1,permormance_date__icontains=current_date).count() 
       
     
        # # challenges = TeamChallenge.objects.filter(customer_accepted_id=employee_data.id,kpi_name_id=select_kpi,is_completed_by_manager=0)

        # challenges = TeamAcceptChallengeHistory.objects.filter(customer_accepted_id=employee_data.id,team_challenge__kpi_name_id=select_kpi,team_challenge__is_completed_by_manager=0)

        # kpi_wip = 0

        # if challenges:
        #     for challenge in challenges:
        #         if challenge.team_challenge.start_time<=current_time and challenge.team_challenge.end_time>=current_time:
        #             kpi_wip +=1
        
        # # team_campaigns = TeamCampaign.objects.filter(customer_accepted_id=employee_data.id,is_completed_by_manager=0)

        # team_campaigns = TeamAcceptCampaignHistory.objects.filter(customer_accepted_id=employee_data.id,team_campaign__is_completed_by_manager=0)

        # for campaign in team_campaigns:
        #     if campaign.team_campaign.start_date<=current_date and campaign.team_campaign.end_date>=current_date:
        #         kpi_data = len(campaign.team_campaign.criteria_point.filter(kpi_id=select_kpi))
        #         kpi_wip +=kpi_data

        # # for employee_email in team_member_email:
        # kpi_data = KpiName.objects.filter(id=select_kpi).first()

        # data ={}
        
        # if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__icontains=current_date).exists():

        #     total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__icontains=current_date).aggregate(Sum('kpi_target'))
        #     total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__icontains=current_date).aggregate(Sum('kpi_actual'))

        #     data['kpi_name']       = kpi_data.name
        #     data['total_target']   = total_target['kpi_target__sum']
        #     data['total_actual']   = total_actual['kpi_actual__sum']
        #     data['total_gap']      = total_target['kpi_target__sum'] - total_actual['kpi_actual__sum']
            
        #     kpi_items.append(data)
    
        kpi_data = KpiName.objects.filter(id=select_kpi).first()
        
        manager_kpi_met_data = 0

        kpi_wip = 0

      
        if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__icontains=current_date).exists():

            manager_employee_kpi_data_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__icontains=current_date).aggregate(Sum('kpi_target'))

            manager_employee_kpi_data_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__icontains=current_date).aggregate(Sum('kpi_actual'))
            
            if not manager_employee_kpi_data_target['kpi_target__sum']:
                pass
            else:
                kpi_target = round(manager_employee_kpi_data_target['kpi_target__sum'],2)
            

            if not manager_employee_kpi_data_actual['kpi_actual__sum']:
                pass
            else:
                kpi_actual = round(manager_employee_kpi_data_actual['kpi_actual__sum'],2)
            
            
            if kpi_target <= kpi_actual:
                manager_kpi_met_data +=1
            
            if kpi_target>kpi_actual:
                kpi_wip +=1         

          
        data ={}
        
        if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__icontains=current_date).exists():

            total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__icontains=current_date).aggregate(Sum('kpi_target'))
            total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__icontains=current_date).aggregate(Sum('kpi_actual'))
            
            if total_target['kpi_target__sum'] !=None or total_actual['kpi_actual__sum'] !=None: 
                data['kpi_name']       = kpi_data.name
                data['total_target']   = round(total_target['kpi_target__sum'],2)
                data['total_actual']   = round(total_actual['kpi_actual__sum'],2)
                data['total_gap']      = round(total_target['kpi_target__sum'] - total_actual['kpi_actual__sum'],2)
            
                kpi_items.append(data)

     
    elif select_name!="all" and select_kpi!="all" and select_time_period=="yesterday":
        yesterday_date = current_date-timedelta(days=1)
        
        # manager_kpi_met_data = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data=select_kpi,kpi_status=1,permormance_date__icontains=yesterday_date).count() 
       
     
        # # team_campaigns = TeamCampaign.objects.filter(customer_accepted_id=employee_data.id,is_completed_by_manager=0)

        # team_campaigns = TeamAcceptCampaignHistory.objects.filter(customer_accepted_id=employee_data.id,team_campaign__is_completed_by_manager=0)

        # for campaign in team_campaigns:
        #     if campaign.team_campaign.start_date<=yesterday_date and campaign.team_campaign.end_date>=yesterday_date:
        #         kpi_data = len(campaign.team_campaign.criteria_point.filter(kpi_id=select_kpi))
        #         kpi_wip +=kpi_data

        # # for employee_email in team_member_email:
        # kpi_data = KpiName.objects.filter(id=select_kpi).first()

        # data ={}
        
        # if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__icontains=yesterday_date).exists():

        #     total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__icontains=yesterday_date).aggregate(Sum('kpi_target'))
        #     total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__icontains=yesterday_date).aggregate(Sum('kpi_actual'))

        #     data['kpi_name']       = kpi_data.name
        #     data['total_target']   = total_target['kpi_target__sum']
        #     data['total_actual']   = total_actual['kpi_actual__sum']
        #     data['total_gap']      = total_target['kpi_target__sum'] - total_actual['kpi_actual__sum']
            
        #     kpi_items.append(data)
    

        kpi_data = KpiName.objects.filter(id=select_kpi).first()
        
        manager_kpi_met_data = 0

        kpi_wip = 0

      
        if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__icontains=yesterday_date).exists():

            manager_employee_kpi_data_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__icontains=yesterday_date).aggregate(Sum('kpi_target'))

            manager_employee_kpi_data_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__icontains=yesterday_date).aggregate(Sum('kpi_actual'))
            
            if not manager_employee_kpi_data_target['kpi_target__sum']:
                pass
            else:
                kpi_target = round(manager_employee_kpi_data_target['kpi_target__sum'],2)
            

            if not manager_employee_kpi_data_actual['kpi_actual__sum']:
                pass
            else:
                kpi_actual = round(manager_employee_kpi_data_actual['kpi_actual__sum'],2)
            
            
            if kpi_target <= kpi_actual:
                manager_kpi_met_data +=1
            
            if kpi_target>kpi_actual:
                kpi_wip +=1         

          
        data ={}
        
        if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__icontains=yesterday_date).exists():

            total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__icontains=yesterday_date).aggregate(Sum('kpi_target'))
            total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__icontains=yesterday_date).aggregate(Sum('kpi_actual'))
            
            if total_target['kpi_target__sum'] !=None or total_actual['kpi_actual__sum'] !=None: 
                data['kpi_name']       = kpi_data.name
                data['total_target']   = round(total_target['kpi_target__sum'],2)
                data['total_actual']   = round(total_actual['kpi_actual__sum'],2)
                data['total_gap']      = round(total_target['kpi_target__sum'] - total_actual['kpi_actual__sum'],2)
            
                kpi_items.append(data)

    elif select_name!="all" and select_kpi!="all" and select_time_period=="wtd":
        end_date   = current_date
        start_date = end_date -timedelta(days=7)
        
        # manager_kpi_met_data = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data=select_kpi,kpi_status=1,permormance_date__date__range=[start_date,end_date]).count() 
       
     
        # # team_campaigns = TeamCampaign.objects.filter(customer_accepted_id=employee_data.id,is_completed_by_manager=0)

        # team_campaigns = TeamAcceptCampaignHistory.objects.filter(customer_accepted_id=employee_data.id,team_campaign__is_completed_by_manager=0)

        # while start_date <= end_date:  
        #     for campaign in team_campaigns:
        #         if campaign.team_campaign.start_date<=start_date and campaign.team_campaign.end_date>=start_date:
        #             kpi_data = len(campaign.team_campaign.criteria_point.filter(kpi_id=select_kpi))
        #             kpi_wip +=kpi_data
        #     start_date = start_date + timedelta(days=1)

        # # for employee_email in team_member_email:
        # kpi_data = KpiName.objects.filter(id=select_kpi).first()

        # data ={}
        
        # if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__date__range=[start_date,end_date]).exists():

        #     total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__date__range=[start_date,end_date]).aggregate(Sum('kpi_target'))
        #     total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__date__range=[start_date,end_date]).aggregate(Sum('kpi_actual'))

        #     data['kpi_name']       = kpi_data.name
        #     data['total_target']   = total_target['kpi_target__sum']
        #     data['total_actual']   = total_actual['kpi_actual__sum']
        #     data['total_gap']      = total_target['kpi_target__sum'] - total_actual['kpi_actual__sum']
            
        #     kpi_items.append(data)
 

        kpi_data = KpiName.objects.filter(id=select_kpi).first()
        
        manager_kpi_met_data = 0

        kpi_wip = 0

      
        if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__date__range=[start_date,end_date]).exists():

            manager_employee_kpi_data_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__date__range=[start_date,end_date]).aggregate(Sum('kpi_target'))

            manager_employee_kpi_data_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__date__range=[start_date,end_date]).aggregate(Sum('kpi_actual'))
            
            if not manager_employee_kpi_data_target['kpi_target__sum']:
                pass
            else:
                kpi_target = round(manager_employee_kpi_data_target['kpi_target__sum'],2)
            

            if not manager_employee_kpi_data_actual['kpi_actual__sum']:
                pass
            else:
                kpi_actual = round(manager_employee_kpi_data_actual['kpi_actual__sum'],2)
            
            
            if kpi_target <= kpi_actual:
                manager_kpi_met_data +=1
            
            if kpi_target>kpi_actual:
                kpi_wip +=1         

          
        data ={}
        
        if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__date__range=[start_date,end_date]).exists():

            total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__date__range=[start_date,end_date]).aggregate(Sum('kpi_target'))
            total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__date__range=[start_date,end_date]).aggregate(Sum('kpi_actual'))
            
            if total_target['kpi_target__sum'] !=None or total_actual['kpi_actual__sum'] !=None: 
                data['kpi_name']       = kpi_data.name
                data['total_target']   = round(total_target['kpi_target__sum'],2)
                data['total_actual']   = round(total_actual['kpi_actual__sum'],2)
                data['total_gap']      = round(total_target['kpi_target__sum'] - total_actual['kpi_actual__sum'],2)
            
                kpi_items.append(data)

        
    elif select_name!="all" and select_kpi!="all" and select_time_period=="mtd":
        month = current_date.month
        year = current_date.year
        
        # manager_kpi_met_data = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data=select_kpi,kpi_status=1,permormance_date__date__month=month,permormance_date__date__year=year).count() 
       
        # # team_campaigns = TeamCampaign.objects.filter(customer_accepted_id=employee_data.id,updated_at__month=month,updated_at__year=year,is_completed_by_manager=0)

        # team_campaigns = TeamAcceptCampaignHistory.objects.filter(customer_accepted_id=employee_data.id,team_campaign__updated_at__month=month,team_campaign__updated_at__year=year,team_campaign__is_completed_by_manager=0)

        # for campaign in team_campaigns:
        #     if campaign.team_campaign.start_date<=start_date and campaign.team_campaign.end_date>=start_date:
        #         kpi_data = len(campaign.team_campaign.criteria_point.filter(kpi_id=select_kpi))
        #         kpi_wip +=kpi_data

        # # for employee_email in team_member_email:
        # kpi_data = KpiName.objects.filter(id=select_kpi).first()

        # data ={}
        
        # if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__date__month=month,permormance_date__date__year=year).exists():

        #     total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__date__month=month,permormance_date__date__year=year).aggregate(Sum('kpi_target'))
        #     total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__date__month=month,permormance_date__date__year=year).aggregate(Sum('kpi_actual'))

        #     data['kpi_name']       = kpi_data.name
        #     data['total_target']   = total_target['kpi_target__sum']
        #     data['total_actual']   = total_actual['kpi_actual__sum']
        #     data['total_gap']      = total_target['kpi_target__sum'] - total_actual['kpi_actual__sum']
            
        #     kpi_items.append(data)
 
        kpi_data = KpiName.objects.filter(id=select_kpi).first()
        
        manager_kpi_met_data = 0

        kpi_wip = 0

      
        if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__date__month=month,permormance_date__date__year=year).exists():

            manager_employee_kpi_data_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__date__month=month,permormance_date__date__year=year).aggregate(Sum('kpi_target'))

            manager_employee_kpi_data_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__date__month=month,permormance_date__date__year=year).aggregate(Sum('kpi_actual'))
            
            if not manager_employee_kpi_data_target['kpi_target__sum']:
                pass
            else:
                kpi_target = round(manager_employee_kpi_data_target['kpi_target__sum'],2)
            

            if not manager_employee_kpi_data_actual['kpi_actual__sum']:
                pass
            else:
                kpi_actual = round(manager_employee_kpi_data_actual['kpi_actual__sum'],2)
            
            
            if kpi_target <= kpi_actual:
                manager_kpi_met_data +=1
            
            if kpi_target>kpi_actual:
                kpi_wip +=1         

          
        data ={}
        
        if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__date__month=month,permormance_date__date__year=year).exists():

            total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__date__month=month,permormance_date__date__year=year).aggregate(Sum('kpi_target'))
            total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__date__month=month,permormance_date__date__year=year).aggregate(Sum('kpi_actual'))
            
            if total_target['kpi_target__sum'] !=None or total_actual['kpi_actual__sum'] !=None: 
                data['kpi_name']       = kpi_data.name
                data['total_target']   = round(total_target['kpi_target__sum'],2)
                data['total_actual']   = round(total_actual['kpi_actual__sum'],2)
                data['total_gap']      = round(total_target['kpi_target__sum'] - total_actual['kpi_actual__sum'],2)
            
                kpi_items.append(data)

    elif select_name!="all" and select_kpi!="all" and select_time_period=="ytd":
        year = current_date.year
        
        # manager_kpi_met_data = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data=select_kpi,kpi_status=1,permormance_date__date__year=year).count() 
       
        # # team_campaigns = TeamCampaign.objects.filter(customer_accepted_id=employee_data.id,updated_at__year=year,is_completed_by_manager=0)
       
        # team_campaigns = TeamAcceptCampaignHistory.objects.filter(customer_accepted_id=employee_data.id,team_campaign__updated_at__year=year,team_campaign__is_completed_by_manager=0)

        # for campaign in team_campaigns:
        #     if campaign.team_campaign.start_date<=current_date and campaign.team_campaign.end_date>=current_date:
        #         kpi_data = len(campaign.team_campaign.criteria_point.filter(kpi_id=select_kpi))
        #         kpi_wip +=kpi_data

        # # for employee_email in team_member_email:
        # kpi_data = KpiName.objects.filter(id=select_kpi).first()

        # data ={}
        
        # if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__date__year=year).exists():

        #     total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__date__year=year).aggregate(Sum('kpi_target'))
        #     total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__date__year=year).aggregate(Sum('kpi_actual'))

        #     data['kpi_name']       = kpi_data.name
        #     data['total_target']   = total_target['kpi_target__sum']
        #     data['total_actual']   = total_actual['kpi_actual__sum']
        #     data['total_gap']      = total_target['kpi_target__sum'] - total_actual['kpi_actual__sum']
            
        #     kpi_items.append(data)

        kpi_data = KpiName.objects.filter(id=select_kpi).first()
        
        manager_kpi_met_data = 0

        kpi_wip = 0

      
        if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__date__year=year).exists():

            manager_employee_kpi_data_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__date__year=year).aggregate(Sum('kpi_target'))

            manager_employee_kpi_data_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__date__year=year).aggregate(Sum('kpi_actual'))
            
            if not manager_employee_kpi_data_target['kpi_target__sum']:
                pass
            else:
                kpi_target = round(manager_employee_kpi_data_target['kpi_target__sum'],2)
            

            if not manager_employee_kpi_data_actual['kpi_actual__sum']:
                pass
            else:
                kpi_actual = round(manager_employee_kpi_data_actual['kpi_actual__sum'],2)
            
            
            if kpi_target <= kpi_actual:
                manager_kpi_met_data +=1
            
            if kpi_target>kpi_actual:
                kpi_wip +=1         

          
        data ={}
        
        if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__date__year=year).exists():

            total_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__date__year=year).aggregate(Sum('kpi_target'))
            total_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=employee_data.user.email,kpi_name_data__id=select_kpi,permormance_date__date__year=year).aggregate(Sum('kpi_actual'))
            
            if total_target['kpi_target__sum'] !=None or total_actual['kpi_actual__sum'] !=None: 
                data['kpi_name']       = kpi_data.name
                data['total_target']   = round(total_target['kpi_target__sum'],2)
                data['total_actual']   = round(total_actual['kpi_actual__sum'],2)
                data['total_gap']      = round(total_target['kpi_target__sum'] - total_actual['kpi_actual__sum'],2)
            
                kpi_items.append(data)

    
  
    
    context['team_member_count']        = team_member_count

    context['manager_kpi_met_data']     = manager_kpi_met_data
    
    context['kpi_wip']                  = kpi_wip

    context['kpi_data']                 = kpi_items
    
    context['message']                  = 'Team performance data has been received successfully' 
    context['response_code']            = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)



@csrf_exempt
@api_view(["POST"])
@authenticate_token
def kpi_lists(request):
    if request.data.get("unique_code") == '' or request.data.get("unique_code") is None:  
        return Response({'message': 'Please provide unique code', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST) 
    
    kpi_data = KpiName.objects.values().filter(organiztaion__unique_code=request.data.get("unique_code"))


    context = {}
    context['kpi_data']                 = kpi_data  
    context['message']                  = 'KPI data has been received successfully' 
    context['response_code']            = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
@authenticate_token
def manager_kpi_met_and_wip(request):
    if request.data.get("manager_id") == '' or request.data.get("manager_id") is None:  
        return Response({'message': 'Please provide manager id', 'response_code':201}, status=HTTP_200_OK) 

    if request.data.get("team_id") == '' or request.data.get("team_id") is None:  
        return Response({'message': 'Please provide team id', 'response_code':201}, status=HTTP_200_OK) 

    try:
        user_profile = UserProfile.objects.filter(id=request.data.get("manager_id")).first()
    except Exception as e:
        return Response({"message":str(e)}, status=HTTP_404_NOT_FOUND)

    if user_profile:
        current_date=datetime.now().date()
        current_time=datetime.now().strftime('%I:%M')
        
        current_month = current_date.month
        
        employee_email = UserProfile.objects.filter(team_id=request.data.get("team_id"),role__id=1).values_list('user__email',flat=True)

        # manager_employee_kpi_met_data = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=employee_email,kpi_status=1,permormance_date__date__lte=current_date).count()
        
        # manager_employee_kpi_wip_data = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=employee_email,kpi_status=0,permormance_date__month=current_month).count()

        kpi_data = KpiName.objects.filter(organiztaion__unique_code=user_profile.unique_code)
        
        kpi_met_count = 0
        
        kpi_wip_count = 0

        for kpi in kpi_data:

            if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=employee_email,kpi_name_data__id=kpi.id).exists():
    
                manager_employee_kpi_data_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=employee_email,kpi_name_data__id=kpi.id).aggregate(Sum('kpi_target'))

                manager_employee_kpi_data_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email__in=employee_email,kpi_name_data__id=kpi.id).aggregate(Sum('kpi_actual'))
                
                if not manager_employee_kpi_data_target['kpi_target__sum']:
                    pass
                else:
                    kpi_target = round(manager_employee_kpi_data_target['kpi_target__sum'],2)
                

                if not manager_employee_kpi_data_actual['kpi_actual__sum']:
                    pass
                else:
                    kpi_actual = round(manager_employee_kpi_data_actual['kpi_actual__sum'],2)
                
                if manager_employee_kpi_data_target['kpi_target__sum']!=None and manager_employee_kpi_data_actual['kpi_actual__sum']!=None:
                
                    if kpi_target <= kpi_actual:
                        kpi_met_count +=1
                    
                    if kpi_target > kpi_actual:
                        kpi_wip_count +=1         


        # challenges = TeamChallenge.objects.filter(manager=user_profile.id,is_completed_by_manager=0)

        # kpi_wip = 0
        # if challenges:
        #     for challenge in challenges:
        #         if challenge.start_time<=current_time and challenge.end_time>=current_time:
        #             kpi_wip +=1
        # team_campaigns = TeamCampaign.objects.filter(manager=user_profile.id,is_completed_by_manager=0)
        # for campaign in team_campaigns:
        #     if campaign.start_date<=current_date and campaign.end_date>=current_date:
        #         kpi_data = len(campaign.criteria_point.all())
        #         kpi_wip +=1 
        
        context = {}
        
        context['manager_kpi_met_data']  = kpi_met_count
        context['total_kpi_wip']         = kpi_wip_count
        context['message']               = 'KPI met and wip data received successfully'
        context['response_code']         = HTTP_200_OK
        return Response(context, status=HTTP_200_OK)
    else:
        context = {}
        context['message']               = 'Success'
        context['response_code']         = HTTP_200_OK
        return Response(context, status=HTTP_200_OK)



# Team wellbeing data
@csrf_exempt
@api_view(["POST"])
@authenticate_token
def team_wellbeing_lists(request):
    if request.data.get("team_id") == '' or request.data.get("team_id") is None:  
        return Response({'message': 'Please provide user team id', 'response_code':201}, status=HTTP_200_OK) 

    if request.data.get("time_period_all") == '' or request.data.get("time_period_all") is None:  
        return Response({'message': 'Please provide time period all', 'response_code':201}, status=HTTP_200_OK) 

    time_period_all = request.data.get("time_period_all")

    current_date = datetime.now().date()
    
    user_profile_ids = UserProfile.objects.filter(team_id=request.data.get("team_id"),role__id=1).values_list('id',flat=True)

    team_employee_count = UserProfile.objects.filter(team_id=request.data.get("team_id"),role__id=1).count()

    if time_period_all=="today":
        
        steps_taken     = StepsTaken.objects.filter(user_profile__id__in=user_profile_ids,created_at__icontains=current_date).aggregate(Sum('steps_count'))

        if not steps_taken['steps_count__sum']:
            steps_count = 0
        else:
            steps_count = steps_taken['steps_count__sum']       
 
        health_metric = HealthMetric.objects.filter(status=1,active=1).first()
        
        steps_percent = 0.0

        if steps_count:
            steps_percent = ((steps_count/(health_metric.target*team_employee_count))*(health_metric.weightage*team_employee_count))*100  
         

        learning_data   = ReadSkillAndHobbyData.objects.filter(user_profile__id__in= user_profile_ids,created_at__icontains=current_date).aggregate(Sum('spent_time_seconds'))
        
        if not learning_data['spent_time_seconds__sum']:
            learning_hours = 0
        else:
            learning_hours = convert_seconds_to_hours(learning_data['spent_time_seconds__sum'])         
        
        health_metric = HealthMetric.objects.filter(status=2,active=1).first()
        
        learning_percent = 0.0

        if learning_hours:
            total_minutes = convert_seconds_to_minutes(learning_data['spent_time_seconds__sum'])

            learning_percent = ((total_minutes/(health_metric.target*team_employee_count))*(health_metric.weightage*team_employee_count))*100 



        meditation_data = watchTimeData.objects.filter(user_profile__id__in=user_profile_ids,created_at__icontains=current_date).aggregate(Sum('spent_time_seconds'))  # Health and Fitness

        if not meditation_data['spent_time_seconds__sum']:
            meditation_hours = 0
        else:
            meditation_hours = convert_seconds_to_hours(meditation_data['spent_time_seconds__sum'])         
        

        health_metric = HealthMetric.objects.filter(status=3,active=1).first()
 
        meditation_percent = 0.0

        if meditation_hours:
            total_minutes = convert_seconds_to_minutes(meditation_data['spent_time_seconds__sum'])

            meditation_percent = ((total_minutes/(health_metric.target*team_employee_count))*(health_metric.weightage*team_employee_count))*100 


    elif time_period_all=="yesterday":
        yesterday_date = current_date-timedelta(days=1)

        steps_taken     = StepsTaken.objects.filter(user_profile__id__in=user_profile_ids,created_at__icontains=yesterday_date).aggregate(Sum('steps_count'))

        if not steps_taken['steps_count__sum']:
            steps_count = 0
        else:
            steps_count = steps_taken['steps_count__sum']        
        
        health_metric = HealthMetric.objects.filter(status=1,active=1).first()
        
        steps_percent = 0.0

        if steps_count:
            steps_percent = ((steps_count/(health_metric.target*team_employee_count))*(health_metric.weightage*team_employee_count))*100  
        
        
        learning_data   = ReadSkillAndHobbyData.objects.filter(user_profile__id__in=user_profile_ids,created_at__icontains=yesterday_date).aggregate(Sum('spent_time_seconds'))
        
        if not learning_data['spent_time_seconds__sum']:
            learning_hours = 0
        else:
            learning_hours = convert_seconds_to_hours(learning_data['spent_time_seconds__sum'])         

   
        
        health_metric = HealthMetric.objects.filter(status=2,active=1).first()
        
        learning_percent = 0.0

        if learning_hours:
            total_minutes = convert_seconds_to_minutes(learning_data['spent_time_seconds__sum'])

            learning_percent = ((total_minutes/(health_metric.target*team_employee_count))*(health_metric.weightage*team_employee_count))*100



        meditation_data = watchTimeData.objects.filter(user_profile__id__in=user_profile_ids,created_at__icontains=yesterday_date).aggregate(Sum('spent_time_seconds'))  # Health and Fitness

        if not meditation_data['spent_time_seconds__sum']:
            meditation_hours = 0
        else:
            meditation_hours = convert_seconds_to_hours(meditation_data['spent_time_seconds__sum'])         
        
        health_metric = HealthMetric.objects.filter(status=3,active=1).first()
 
        meditation_percent = 0.0

        if meditation_hours:
            total_minutes = convert_seconds_to_minutes(meditation_data['spent_time_seconds__sum'])

            meditation_percent = ((total_minutes/(health_metric.target*team_employee_count))*(health_metric.weightage*team_employee_count))*100

    
    elif time_period_all=="wtd":
        end_date   = current_date
        start_date = end_date -timedelta(days=7)
        
     
        steps_taken     = StepsTaken.objects.filter(user_profile__id__in=user_profile_ids,created_at__date__range=[start_date,end_date]).aggregate(Sum('steps_count'))

        if not steps_taken['steps_count__sum']:
            steps_count = 0
        else:
            steps_count = steps_taken['steps_count__sum']        


        health_metric = HealthMetric.objects.filter(status=1,active=1).first()
        
        steps_percent = 0.0

        if steps_count:
            steps_percent = ((steps_count/(health_metric.target*team_employee_count))*(health_metric.weightage*team_employee_count))*100  
        

        learning_data   = ReadSkillAndHobbyData.objects.filter(user_profile__id__in=user_profile_ids,created_at__date__range=[start_date,end_date]).aggregate(Sum('spent_time_seconds'))
        
        if not learning_data['spent_time_seconds__sum']:
            learning_hours = 0
        else:
            learning_hours = convert_seconds_to_hours(learning_data['spent_time_seconds__sum'])         

        health_metric = HealthMetric.objects.filter(status=2,active=1).first()
        
        learning_percent = 0.0

        if learning_hours:
            total_minutes = convert_seconds_to_minutes(learning_data['spent_time_seconds__sum'])

            learning_percent = ((total_minutes/(health_metric.target*team_employee_count))*(health_metric.weightage*team_employee_count))*100


        meditation_data = watchTimeData.objects.filter(user_profile__id__in=user_profile_ids,created_at__date__range=[start_date,end_date]).aggregate(Sum('spent_time_seconds'))  # Health and Fitness

        if not meditation_data['spent_time_seconds__sum']:
            meditation_hours = 0
        else:
            meditation_hours = convert_seconds_to_hours(meditation_data['spent_time_seconds__sum'])         


        health_metric = HealthMetric.objects.filter(status=3,active=1).first()
 
        meditation_percent = 0.0

        if meditation_hours:
            total_minutes = convert_seconds_to_minutes(meditation_data['spent_time_seconds__sum'])

            meditation_percent = ((total_minutes/(health_metric.target*team_employee_count))*(health_metric.weightage*team_employee_count))*100

    
    elif time_period_all=="mtd":
        month = current_date.month
        year = current_date.year
        
       
        steps_taken     = StepsTaken.objects.filter(user_profile__id__in=user_profile_ids,created_at__year=year,created_at__month=month).aggregate(Sum('steps_count'))

        if not steps_taken['steps_count__sum']:
            steps_count = 0
        else:
            steps_count = steps_taken['steps_count__sum']

        health_metric = HealthMetric.objects.filter(status=1,active=1).first()
        
        steps_percent = 0.0

        if steps_count:
            steps_percent = ((steps_count/(health_metric.target*team_employee_count))*(health_metric.weightage*team_employee_count))*100  
        

        learning_data   = ReadSkillAndHobbyData.objects.filter(user_profile__id__in=user_profile_ids,created_at__year=year,created_at__month=month).aggregate(Sum('spent_time_seconds'))
        
        if not learning_data['spent_time_seconds__sum']:
            learning_hours = 0
        else: 
            learning_hours = convert_seconds_to_hours(learning_data['spent_time_seconds__sum'])         

        health_metric = HealthMetric.objects.filter(status=2,active=1).first()
        
        learning_percent = 0.0

        if learning_hours:
            total_minutes = convert_seconds_to_minutes(learning_data['spent_time_seconds__sum'])

            learning_percent = ((total_minutes/(health_metric.target*team_employee_count))*(health_metric.weightage*team_employee_count))*100


        meditation_data = watchTimeData.objects.filter(user_profile__id__in=user_profile_ids,created_at__year=year,created_at__month=month).aggregate(Sum('spent_time_seconds'))  # Health and Fitness

        if not meditation_data['spent_time_seconds__sum']:
            meditation_hours = 0
        else:
            meditation_hours = convert_seconds_to_hours(meditation_data['spent_time_seconds__sum'])         

        health_metric = HealthMetric.objects.filter(status=3,active=1).first()
 
        meditation_percent = 0.0

        if meditation_hours:
            total_minutes = convert_seconds_to_minutes(meditation_data['spent_time_seconds__sum'])

            meditation_percent = ((total_minutes/(health_metric.target*team_employee_count))*(health_metric.weightage*team_employee_count))*100


    elif time_period_all=="ytd":
        year = current_date.year
        
     
        steps_taken     = StepsTaken.objects.filter(user_profile__id__in=user_profile_ids,created_at__year=year).aggregate(Sum('steps_count'))

        if not steps_taken['steps_count__sum']:
            steps_count = 0
        else:
            steps_count = steps_taken['steps_count__sum']        


        health_metric = HealthMetric.objects.filter(status=1,active=1).first()
        
        steps_percent = 0.0

        if steps_count:
            steps_percent = ((steps_count/(health_metric.target*team_employee_count))*(health_metric.weightage*team_employee_count))*100  
        

        learning_data   = ReadSkillAndHobbyData.objects.filter(user_profile__id__in=user_profile_ids,created_at__year=year).aggregate(Sum('spent_time_seconds'))
        
        if not learning_data['spent_time_seconds__sum']:
            learning_hours = 0
        else:
            learning_hours = convert_seconds_to_hours(learning_data['spent_time_seconds__sum'])         

        health_metric = HealthMetric.objects.filter(status=2,active=1).first()
        
        learning_percent = 0.0

        if learning_hours:
            total_minutes = convert_seconds_to_minutes(learning_data['spent_time_seconds__sum'])

            learning_percent = ((total_minutes/(health_metric.target*team_employee_count))*(health_metric.weightage*team_employee_count))*100


        meditation_data = watchTimeData.objects.filter(user_profile__id__in=user_profile_ids,created_at__year=year).aggregate(Sum('spent_time_seconds'))  # Health and Fitness

        if not meditation_data['spent_time_seconds__sum']:
            meditation_hours = 0
        else:
            meditation_hours = convert_seconds_to_hours(meditation_data['spent_time_seconds__sum'])         


        health_metric = HealthMetric.objects.filter(status=3,active=1).first()
 
        meditation_percent = 0.0

        if meditation_hours:
            total_minutes = convert_seconds_to_minutes(meditation_data['spent_time_seconds__sum'])

            meditation_percent = ((total_minutes/(health_metric.target*team_employee_count))*(health_metric.weightage*team_employee_count))*100


    elif time_period_all=="all":
        steps_taken     = StepsTaken.objects.filter(user_profile__id__in=user_profile_ids).aggregate(Sum('steps_count'))

        if not steps_taken['steps_count__sum']:
            steps_count = 0
        else:
            steps_count = steps_taken['steps_count__sum']        

        health_metric = HealthMetric.objects.filter(status=1,active=1).first()
        
        steps_percent = 0.0

        if steps_count:

            steps_percent = ((steps_count/(health_metric.target*team_employee_count))*(health_metric.weightage*team_employee_count))*100  
        

        learning_data   = ReadSkillAndHobbyData.objects.filter(user_profile__id__in=user_profile_ids).aggregate(Sum('spent_time_seconds'))
        
        if not learning_data['spent_time_seconds__sum']:
            learning_hours = 0
        else:
            learning_hours = convert_seconds_to_hours(learning_data['spent_time_seconds__sum'])         


        health_metric = HealthMetric.objects.filter(status=2,active=1).first()
        
        learning_percent = 0.0

        if learning_hours:
            total_minutes = convert_seconds_to_minutes(learning_data['spent_time_seconds__sum'])
          
            learning_percent = ((total_minutes/(health_metric.target*team_employee_count))*(health_metric.weightage*team_employee_count))*100



        meditation_data = watchTimeData.objects.filter(user_profile__id__in=user_profile_ids).aggregate(Sum('spent_time_seconds'))  # Health and Fitness

        if not meditation_data['spent_time_seconds__sum']:
            meditation_hours = 0
        else:
            meditation_hours = convert_seconds_to_hours(meditation_data['spent_time_seconds__sum'])         

        health_metric = HealthMetric.objects.filter(status=3,active=1).first()
 
        meditation_percent = 0.0

        if meditation_hours:
            total_minutes = convert_seconds_to_minutes(meditation_data['spent_time_seconds__sum'])
            
            meditation_percent = ((total_minutes/(health_metric.target*team_employee_count))*(health_metric.weightage*team_employee_count))*100


    context = {}
    
    context['steps_count']         = steps_count
    
    context['learning_hours']      = learning_hours

    context['meditation_hours']    = meditation_hours

    context['wellbeing_percent']   = round(steps_percent + learning_percent + meditation_percent,2)

    context['message']= 'Team wellbeing data has been received successfully'

    context['response_code']            = HTTP_200_OK

    return Response(context, status=HTTP_200_OK)

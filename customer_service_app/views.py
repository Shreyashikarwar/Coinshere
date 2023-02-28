import datetime

from re import X
from telnetlib import STATUS
from django.utils.timezone import now
from rest_framework import serializers, status
from enum import unique
from django.shortcuts import render
import requests
from datetime import datetime, date, timedelta

from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

import json

from decorators.decorators import *



# Model and Serializers Import 
from rest_framework import serializers, status
from rest_framework.response import Response 
from .serializers import *
from .models import *
from line_manager_app.models import *

import pandas as pd

from django.db.models import Sum

from admin_user.models import *

from utils.helpers import *

# Create your views here.

# Create your views here.

@csrf_exempt
@api_view(["GET"])
@authenticate_token
def customer_concat_list(request):

    customer_concat_data = CustomerConcernCategory.objects.filter(status=1)
    customer_concat_data_count = CustomerConcernCategory.objects.filter(status=1).count()

    serializer = CustomerConcernCategorySerializers(customer_concat_data, many=True)
    return Response(data = {'msg':'success','count':customer_concat_data_count,'data':serializer.data,'response_code':200,},status=status.HTTP_200_OK)  
    
    


@csrf_exempt
@api_view(["POST"])
@authenticate_token
def challenge_lists(request):
    if request.data.get("unique_code") == '' or request.data.get("unique_code") is None:  
        return Response({'message': 'Please provide unique code for list challenges', 'response_code':201}, status=HTTP_200_OK) 
    
    if request.data.get("team_id") == '' or request.data.get("team_id") is None:  
        return Response({'message': 'Please provide team id', 'response_code':201}, status=HTTP_200_OK) 

    if request.data.get("employee_id") == '' or request.data.get("employee_id") is None:  
        return Response({'message': 'Please provide employee id', 'response_code':201}, status=HTTP_200_OK) 


    
    current_date=datetime.now().date()
    current_time=datetime.now().strftime('%H:%M:%S')

  
    team_challenges = TeamChallenge.objects.values().filter(is_broadcasted=1,updated_at__date=current_date,manager__unique_code=request.data.get("unique_code"),manager__team_id=request.data.get("team_id"),manager__role__id=2,is_completed_by_manager=0).order_by('-id')
    
    data = [] 

    count_challenge = 0
    
   
    for challenge in team_challenges:
        
      
        if challenge['start_time']<=current_time and current_time<=challenge['end_time']:
            team_challenge_history = TeamAcceptChallengeHistory.objects.filter(team_challenge__id=challenge['id'],customer_accepted_id=request.data.get("employee_id"),created_at__icontains=challenge['updated_at'].date(),is_accepted=1).first()
            
            if team_challenge_history:
                challenge['is_accepted'] = 1
            else:
                challenge['is_accepted'] = 0
            
            kpi_name = KpiName.objects.filter(id=challenge['kpi_name_id']).first()

            if kpi_name:
                challenge['kpi_name'] = kpi_name.name
            else:
                challenge['kpi_name'] = ""    
             
            data.append(challenge)

            count_challenge += 1            

    context = {}
    context['team_challenge_lists']         = data
    context['message']= 'Challenges have been received successfully' 
    context['response_code']            = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)

    
@csrf_exempt
@api_view(["POST"])
@authenticate_token
def campaign_lists(request):
    if request.data.get("unique_code") == '' or request.data.get("unique_code") is None:  
        return Response({'message': 'Please provide unique code for list campaigns', 'response_code': 201}, status=201) 
    
    if request.data.get("team_id") == '' or request.data.get("team_id") is None:  
        return Response({'message': 'Please provide team id', 'response_code':201}, status=HTTP_200_OK) 
        
    current_date = datetime.now().date()
    team_campaigns = TeamCampaign.objects.filter(is_broadcasted=1,manager__unique_code=request.data.get("unique_code"),manager__team_id=request.data.get("team_id"),manager__role__id=2,is_completed_by_manager=0).order_by('-id')

    current_time=datetime.now().strftime('%H:%M:%S')

    data = []

    for obj in team_campaigns:
        if obj.start_date<=current_date and current_date<=obj.end_date:
            dict = {}
            dict['id']                       = obj.id 
            dict['purpose_name']             = obj.campaign_purpose.purpose_name
            dict['campaign_name']            = obj.campaign_name
            dict['contact_person']           = obj.manager.user.first_name +" "+obj.manager.user.last_name
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
    context['team_campaign_lists']     = data
    context['message']= 'Campaign has been received successfully' 
    context['response_code']            = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)


# Deo abhinav 
@csrf_exempt
@api_view(['GET'])
@authenticate_token
def customer_raise_concern(request):
    try:
        user_profile_data = request.query_params.get('user_profile')
    except:
        return Response({'Msg':'Please Provide user_profile_data in params'})

    customer_concat_data=CustomerRaiseConcern.objects.filter(user_profile=user_profile_data)
    customer_concat_data_count=CustomerRaiseConcern.objects.filter(user_profile=user_profile_data).count()
    concat_data_serializer=CustomerRaiseConcernSerializers(customer_concat_data,many=True)

    datas = concat_data_serializer.data
   
    for data in datas:
        
        if data['action_owner_id']==1:
            admin_user = User.objects.filter(id=data['action_owner_id'],is_superuser=1).first()
            action_owner_name = admin_user.first_name +" "+ admin_user.last_name 
        else:            
            admin_user_org = Organiztaion.objects.filter(id=data['action_owner_id']).first()
            action_owner_name = admin_user_org.organization_name

        # user_profile = UserProfile.objects.filter(id=data['action_owner_id']).first()
        
        data['action_owner_name'] = action_owner_name


    return Response(data={'count':customer_concat_data_count,'msg':'Success','data':datas,'response_code':200},status=status.HTTP_200_OK)


# Deo abhinav 
@csrf_exempt
@api_view(['POST'])
@authenticate_token
def customer_raise_concern_update(request):
        id=request.data.get('user_profile')
        concern_category=request.data.get('concern_category')
        
        print("concern category===>",concern_category)

        user_data=UserProfile.objects.get(id=id)
      
        # manager=UserProfile.objects.filter(unique_code=unique_code_data,team_id=user_data.team_id,role__id=2).first()

        serializer = CustomerRaiseConcernSerializers(data=request.data)

        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            customer_raise_concern = CustomerRaiseConcern.objects.filter(id=data['id']).first()

            if int(concern_category)==1:
                admin_user = User.objects.filter(id=1,is_superuser=1).first()

                customer_raise_concern.action_owner_id = admin_user.id
            else:
                unique_code = user_data.unique_code
                
                admin_user = Organiztaion.objects.filter(unique_code=unique_code).first()

                customer_raise_concern.action_owner_id = admin_user.id

            customer_raise_concern.save()
            
            data['action_owner_id']   = admin_user.id
            data['response_code']     = 200
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_201_CREATED)






#Customer Josh Reason Type
 
@api_view(['GET'])
@authenticate_token
def customer_josh_reason_type(request):
    try:
        Customer_reason=ReasonType.objects.all()
    except:
        return Response({'Msg':'Data Not Found'})

    serializer=ReasonTypeSerializers(Customer_reason,many=True)
    return Response(data={'customer_reason_type':serializer.data,'response_code':201},status=status.HTTP_200_OK)



# Create Josh Reason Data

@api_view(['POST'])
@csrf_exempt
def customer_josh_create(request):
    if request.method == 'POST':
        # User profile 
        user_profile_id=request.data.get('user_profile')
        
        #Get User Data 
        user_data=UserProfile.objects.get(id=user_profile_id)
        
        current_date=datetime.now().date()

        if not JoshReason.objects.filter(user_profile=user_data,created_at__icontains=current_date).first():
        
            # Line manager get 
            manager_id=user_data.manager_id
            
            if request.data.get('reason_type')=="" or request.data.get('reason_type') is None:

                points = RewardPointsStimulator.objects.filter(status=10).first()

                if MyRewardPoint.objects.filter(user_profile__id=user_profile_id).exists():

                    my_reward = MyRewardPoint.objects.filter(user_profile__id=user_profile_id).last()

                    point_balance = my_reward.point_balance + int(points.multiplier)

                    my_reward = MyRewardPoint.objects.create(
                        manager_id=0,              
                        user_profile=user_data,
                        earned_point=int(points.multiplier),
                        point_balance=point_balance
                    )
                else:
                    my_reward = MyRewardPoint.objects.create(
                        manager_id=0,              
                        user_profile=user_data,
                        earned_point=int(points.multiplier),
                        point_balance=int(points.multiplier)
                    )



            josh_serializer=JoshReasonSerializers(data=request.data)

            if josh_serializer.is_valid():

                josh_serializer.save()

                data=josh_serializer.data

                josh_reason_data = JoshReason.objects.filter(id=data['id']).first()



                josh_reason_data.manager_id = user_data.team_id
                josh_reason_data.save()

                emoji_point = data['emoji_point']

                if int(emoji_point)<=3:
          
                    points = RewardPointsStimulator.objects.filter(status=11).first()

                    if MyRewardPoint.objects.filter(user_profile__id=user_profile_id).exists():

                        my_reward = MyRewardPoint.objects.filter(user_profile__id=user_profile_id).last()

                        point_balance = my_reward.point_balance + int(points.multiplier)

                        my_reward = MyRewardPoint.objects.create(
                            manager_id=0,              
                            user_profile=user_data,
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

                    userFirebaseToken = user_data.firebase_token

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

                        save_notification(user_data.id,user_data.id,heading,notification_msg,'my_josh')

            
                data['manager_id']= manager_id
                data['response_code'] = 200
                return Response(data, status=status.HTTP_200_OK)
            return Response(josh_serializer.errors, status=status.HTTP_201_CREATED)
        else:
            context = {}
            context['message']= "Today,you have created your josh so you can not create your josh again." 
            context['response_code']            = 201
            return Response(context, status=HTTP_200_OK)




@csrf_exempt
@api_view(["POST"])
@authenticate_token
def accept_challenge_by_customer(request):
  
    if request.data.get("user_id") == '' or request.data.get("user_id") is None:  
        return Response({'message': 'Please provide user id', 'response_code': 201}, status=HTTP_200_OK) 
    
    if request.data.get("challenge_id") == '' or request.data.get("challenge_id") is None:  
        return Response({'message': 'Please provide challenge id', 'response_code':201}, status=HTTP_200_OK) 

    if request.data.get("is_accepted") == '' or request.data.get("is_accepted") is None:  
        return Response({'message': 'Please provide accept id', 'response_code':201}, status=HTTP_200_OK) 
    
    user_profile = UserProfile.objects.filter(id=request.data.get("user_id")).first()
        
    team_challenge = TeamChallenge.objects.filter(id=request.data.get("challenge_id")).first()
    
    points = RewardPointsStimulator.objects.filter(status=5).first()
 
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

    team_accept_challenge                      = TeamAcceptChallengeHistory()
    team_accept_challenge.team_challenge       = team_challenge
    team_accept_challenge.customer_accepted_id = user_profile.id
    team_accept_challenge.is_accepted          = request.data.get("is_accepted")
    team_accept_challenge.save()
    
    
    context = {}
    
    context['message']                  = 'Challenge has been accepted successfully'
    
    context['response_code']            = HTTP_200_OK

    return Response(context, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@authenticate_token
def accept_campaign_by_customer(request):
    if request.data.get("user_id") == '' or request.data.get("user_id") is None:  
        return Response({'message': 'Please provide user id', 'response_code':201}, status=HTTP_200_OK) 

    if request.data.get("campaign_id") == '' or request.data.get("campaign_id") is None:  
        return Response({'message': 'Please provide campaign id', 'response_code': 201}, status=HTTP_200_OK) 

    if request.data.get("is_accepted") == '' or request.data.get("is_accepted") is None:  
        return Response({'message': 'Please provide accept id', 'response_code': 201}, status=HTTP_200_OK) 
        

    user_profile = UserProfile.objects.filter(id=request.data.get("user_id")).first()
        
    team_campaign = TeamCampaign.objects.filter(id=request.data.get("campaign_id")).first()


    team_accept_campaign                      = TeamAcceptCampaignHistory()
    team_accept_campaign.team_campaign        = team_campaign
    team_accept_campaign.customer_accepted_id = user_profile.id
    team_accept_campaign.is_accepted          = request.data.get("is_accepted")
    team_accept_campaign.save()
    
    context = {}
    context['message']= 'Campaign has been accepted successfully' 
    context['response_code']  = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@authenticate_token
def complete_challenge_by_customer(request):
    if request.data.get("user_id") == '' or request.data.get("user_id") is None:  
        return Response({'message': 'Please provide user id', 'response_code': 201}, status=HTTP_200_OK) 

    if request.data.get("challenge_id") == '' or request.data.get("challenge_id") is None:  
        return Response({'message': 'Please provide challenge id', 'response_code':201}, status=HTTP_200_OK) 

    if request.data.get("is_completed_by_customer") == '' or request.data.get("is_completed_by_customer") is None:  
        return Response({'message': 'Please provide is completed by customer id', 'response_code':201}, status=HTTP_200_OK) 


    team_challenge = TeamChallenge.objects.filter(id=request.data.get("challenge_id")).first()
    team_challenge.is_completed_by_customer = request.data.get("is_completed_by_customer")
    team_challenge.save()
    
    context = {}
    context['message']= 'Challenge has been completed successfully' 
    context['response_code']            = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@authenticate_token
def complete_campaign_by_customer(request):
    if request.data.get("user_id") == '' or request.data.get("user_id") is None:  
        return Response({'message': 'Please provide user id', 'response_code':201}, status=HTTP_200_OK) 

    if request.data.get("campaign_id") == '' or request.data.get("campaign_id") is None:  
        return Response({'message': 'Please provide campaign id', 'response_code':201}, status=HTTP_200_OK) 

    if request.data.get("is_completed_by_customer") == '' or request.data.get("is_completed_by_customer") is None:  
        return Response({'message': 'Please provide is completed by customer id', 'response_code': 201}, status=HTTP_200_OK) 


    team_campaign = TeamCampaign.objects.filter(id=request.data.get("campaign_id")).first()
    team_campaign.is_completed_by_customer = request.data.get("is_completed_by_customer")
    team_campaign.save()
        
    
    context = {}
    context['message']= 'Campaign has been completed successfully' 
    context['response_code']            = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)


# @csrf_exempt
# @api_view(["POST"])
# @authenticate_token
# def customer_challenge_point_list(request):
#     if request.data.get("unique_code") == '' or request.data.get("unique_code") is None:  
#         return Response({'message': 'Please provide unique code for list challenges', 'response_code': 201}, status=HTTP_200_OK) 

#     if request.data.get("team_id") == '' or request.data.get("team_id") is None:  
#         return Response({'message': 'Please provide team id', 'response_code': 201}, status=HTTP_200_OK) 
    
    
#     team_challenges = TeamChallenge.objects.values().filter(is_broadcasted=1,manager__unique_code=request.data.get("unique_code"),manager__role__id=2,is_completed_by_manager=0).order_by('-id')
#     context = {}
#     context['team_challenge_lists']     = team_challenges
#     context['message']= 'Challenges have been received successfully' 
#     context['response_code']            = HTTP_200_OK
#     return Response(context, status=HTTP_200_OK)



# @csrf_exempt
# @api_view(["POST"])
# @authenticate_token
# def customer_campaign_point_list(request):
#     if request.data.get("unique_code") == '' or request.data.get("unique_code") is None:  
#         return Response({'message': 'Please provide unique code for list challenges', 'response_code': 201}, status=HTTP_200_OK) 

#     if request.data.get("team_id") == '' or request.data.get("team_id") is None:  
#         return Response({'message': 'Please provide team id', 'response_code': 201}, status=HTTP_200_OK) 

    
#     team_challenges = TeamChallenge.objects.values().filter(is_broadcasted=1,manager__unique_code=request.data.get("unique_code"),manager__role__id=2,is_completed_by_manager=0).order_by('-id')
#     context = {}
#     context['team_challenge_lists']     = team_challenges
#     context['message']= 'Challenges have been received successfully' 
#     context['response_code']            = HTTP_200_OK
#     return Response(context, status=HTTP_200_OK)




# Team josh Reason Type

@csrf_exempt
@api_view(['GET'])
@authenticate_token
def team_josh_reason_today(request):
    try:
        manager_id_data = request.query_params.get('manager_id')
    except:
        return Response({'Msg':'Please Provide manager_id in params'})
 
    teams_reward_data = JoshReason.objects.values_list('emoji_point').filter(manager_id=manager_id_data)
    employee_sum_data = {}

    for employee_id in set(teams_reward_data):
        single_employee = JoshReason.objects.filter(manager_id=manager_id_data).aggregate(Sum('emoji_point'))
        employee_sum_data[employee_id]= single_employee['emoji_point__sum']
        print(single_employee)

            
    return Response(data={'msg':'Success','response_code':200},status=status.HTTP_200_OK)









# customer_josh_reason_list

# Deo abhinav 
@csrf_exempt
@api_view(['GET'])
@authenticate_token
def customer_josh_reason_list(request):
    try:
        user_profile_data = request.query_params.get('user_profile')
    except:
        return Response({'Msg':'Please Provide user_profile_data in params'})

    current_date   = date.today()
    customer_josh_data=JoshReason.objects.filter(user_profile=user_profile_data,created_at__icontains = current_date)
    customer_josh_data_count=JoshReason.objects.filter(user_profile=user_profile_data,created_at = current_date).count()
    concat_josh_serializer=JoshReasonSerializers(customer_josh_data,many=True)

    return Response(data={'count':customer_josh_data_count,'msg':'Success','data':concat_josh_serializer.data,'response_code':200},status=status.HTTP_200_OK)



# Customer Josh Data For Today

@csrf_exempt
@api_view(['GET'])
@authenticate_token
def customer_josh_reason_today(request):
    try:
        user_profile_data = request.query_params.get('user_profile')
    except:
        return Response({'Msg':'Please Provide user_profile_data in params'})

    try:
        manager_id = request.query_params.get('manager_id')
    except:
        return Response({'Msg':'Please Provide manager id in params'})

    
    current_date=datetime.now().date()
    

    customer_josh_data=JoshReason.objects.filter(user_profile__id=user_profile_data,created_at__icontains=current_date).first()

    customer_josh_data_count=JoshReason.objects.filter(user_profile__id=user_profile_data,created_at = current_date).count()
    
    concat_josh_serializer=JoshReasonSerializers(customer_josh_data)

    total_team_mood_count =JoshReason.objects.filter(manager_id=manager_id,created_at__icontains=current_date).count()
    
    if not total_team_mood_count:
        total_team_mood_count = 1
    else:
        total_team_mood_count = total_team_mood_count         

    total_team_mood_sum =JoshReason.objects.filter(manager_id=manager_id,created_at__icontains=current_date).aggregate(Sum('emoji_point'))
    
    if not total_team_mood_sum['emoji_point__sum']:
        total_team_mood_sum = 0
    else:
        total_team_mood_sum = total_team_mood_sum['emoji_point__sum']     
    
    # print(total_team_mood_sum,total_team_mood_count)

    team_mood  = round(total_team_mood_sum / total_team_mood_count)
    

    end_date = current_date

    start_date = current_date - timedelta(days=4)
    
    moodalytics = []

    while start_date<=end_date:
        data = {}
        josh_reason =JoshReason.objects.filter(user_profile__id=user_profile_data,created_at__icontains=start_date).first()

        if josh_reason: 
            data['date']        = start_date
            data['emoji_point'] = josh_reason.emoji_point
        else:
            data['date']        = start_date
            data['emoji_point'] = 0
        
        moodalytics.append(data)

        start_date = start_date +timedelta(days=1)

    return Response(data={'count':customer_josh_data_count,'msg':'Success','data':concat_josh_serializer.data,'team_mood':team_mood,'moodalytics':moodalytics,'response_code':200},status=status.HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@authenticate_token
def notification_lists(request):
    if request.data.get("user_id") == '' or request.data.get("user_id") is None:  
        return Response({'message': 'Please provide user id', 'response_code':201}, status=HTTP_200_OK) 
    
    notifications = Notification.objects.values().filter(to_user_id=request.data.get('user_id'))
    for notification in notifications:
        notification['created_at'] = notification['created_at'].strftime('%d-%m-%Y %I:%M:%S')
    context = {}
    context['notifications'] = notifications
    context['message']= 'Notifications have been receieved successfully' 
    context['response_code']            = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@authenticate_token
def delete_notifications(request):
    if request.data.get("user_id") == '' or request.data.get("user_id") is None:  
        return Response({'message': 'Please provide user id', 'response_code':201}, status=HTTP_200_OK) 

    if request.data.get("notification_ids") == '' or request.data.get("notification_ids") is None:  
        return Response({'message': 'Please provide notification ids', 'response_code':201}, status=HTTP_200_OK) 
    
    notifications = Notification.objects.filter(to_user_id=request.data.get("user_id"),id__in=request.data.get("notification_ids"))
    
    for notification in notifications:
        notification.delete()


    context = {}
    context['message']= 'Notifications have been deleted successfully' 
    context['response_code']            = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@authenticate_token
def mark_read_notifications(request):
    if request.data.get("user_id") == '' or request.data.get("user_id") is None:  
        return Response({'message': 'Please provide user id', 'response_code':201}, status=HTTP_200_OK) 

    if request.data.get("notification_ids") == '' or request.data.get("notification_ids") is None:  
        return Response({'message': 'Please provide notification ids', 'response_code':201}, status=HTTP_200_OK) 
    

    notifications = Notification.objects.filter(to_user_id=request.data.get("user_id"),id__in=request.data.get("notification_ids"))
    
    for notification in notifications:
        notification.is_read = True
        notification.save()


    context = {}
    context['message']= 'Notifications have been marked as read successfully' 
    context['response_code']            = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@authenticate_token
def mark_unread_notifications(request):
    if request.data.get("user_id") == '' or request.data.get("user_id") is None:  
        return Response({'message': 'Please provide user id', 'response_code':201}, status=HTTP_200_OK) 

    if request.data.get("notification_ids") == '' or request.data.get("notification_ids") is None:  
        return Response({'message': 'Please provide notification ids', 'response_code':201}, status=HTTP_200_OK) 

    notifications = Notification.objects.filter(to_user_id=request.data.get("user_id"),id__in=request.data.get("notification_ids"))
    
    for notification in notifications:
        notification.is_read = False
        notification.save()


    context = {}
    context['message']= 'Notifications have been marked as unread successfully' 
    context['response_code']            = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)




# KPI's met and KPI's WIP count

@csrf_exempt
@api_view(["POST"])
@authenticate_token
def my_performance(request):
    if request.data.get("manager_id") == '' or request.data.get("manager_id") is None:  
        return Response({'message': 'Please provide manager id', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST) 

    current_date=datetime.datetime.now().date()

    team_challenge_count = TeamChallenge.objects.filter(manager__id=request.data.get("manager_id"),updated_at_icontains=current_date,is_broadcasted=1,is_accepted=1,is_completed_by_customer=0).count()
    team_challenge_won_count = TeamChallenge.objects.filter(manager__id=request.data.get("manager_id"),updated_at_icontains=current_date,is_broadcasted=1,is_accepted=1,is_completed_by_customer=1).count()
            
    context = {}
    context['today_customer_accepted']  = team_challenge_count
    context['today_customer_won']       = team_challenge_won_count
    context['message']                  = 'Todays challenge count has been received successfully' 
    context['response_code']            = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)




#  My Reward Point listing API's

@csrf_exempt
@api_view(["POST"])
@authenticate_token
def my_reward_point_list(request):

    team_id = request.data.get('team_id')
   
    user_profile_ids = UserProfile.objects.filter(team_id=team_id,role__id=1).values_list('id',flat=True)
      
    time_period_all = request.data.get('time_period_all')
    current_date   = date.today()


    if time_period_all=="time_period_all":
        teams_reward_data = MyRewardPoint.objects.filter(user_profile__id__in=user_profile_ids)
 
    elif time_period_all=="today":
        teams_reward_data = MyRewardPoint.objects.filter(user_profile__id__in=user_profile_ids,created_at__icontains=current_date)
  
    
    elif time_period_all=="yesterday":
        yesterday_date = current_date-timedelta(days=1)
        teams_reward_data = MyRewardPoint.objects.filter(user_profile__id__in=user_profile_ids,created_at__icontains=yesterday_date)
     
     
    elif  time_period_all=="wtd":
        end_date   = current_date
        start_date = end_date -timedelta(days=7)
        teams_reward_data = MyRewardPoint.objects.filter(user_profile__id__in=user_profile_ids, created_at__date__range=[start_date,end_date])


    elif time_period_all=="mtd":
        month = current_date.month
        year = current_date.year
        teams_reward_data = MyRewardPoint.objects.filter(user_profile__id__in=user_profile_ids,created_at__month=month,created_at__year=year)


    elif  time_period_all=="ytd":
        year = current_date.year
        teams_reward_data = MyRewardPoint.objects.filter(user_profile__id__in=user_profile_ids,created_at__date__year=year)

    else:
        return Response(data={'msg':'please provide valid data','response_code':201},status=status.HTTP_201_CREATED)
   
  
  
    employee_sum_data = {}
    team_points_data = []
    

    for employee_id in user_profile_ids:
        single_employee = teams_reward_data.filter(user_profile__id=employee_id).aggregate(Sum('earned_point'))
        if single_employee['earned_point__sum']: 
            employee_sum_data[employee_id]= single_employee['earned_point__sum']

    if employee_sum_data:
        data = {k: v for k, v in sorted(employee_sum_data.items(), key=lambda employee_sum_data: employee_sum_data[1],reverse=True)[:10]}

        for key,value in data.items():
            user_profile = UserProfile.objects.filter(id=int(key)).first()

            team_points_data.append({"points":value,'employee_id':user_profile.id, 'employee_name':user_profile.user.first_name+" "+user_profile.user.last_name,"email":user_profile.user.email})


    context = {}
    context['my_reward_point_list']  =  team_points_data
    context['message']               = 'My Reward Point lists have been received successfully'
    context['response_code']         = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)


# Watch Time Data Serializer // Wellbeing Time Spent
@csrf_exempt
@api_view(['POST'])
@authenticate_token
def watch_time_data(request):

        spent_time_seconds = request.data.get('spent_time_seconds') 
        
        manager_josh_create_serializer=watchTimeDataSerializer(data=request.data)

        if manager_josh_create_serializer.is_valid():
         
            video_watch_data = watchTimeData.objects.filter(user_profile__id=request.data.get("user_profile"),leader_ship_task__id=request.data.get('leader_ship_task'))
            
          
            video = LeaderShipTask.objects.filter(id=int(request.data.get('leader_ship_task'))).first()
            
            user_profile_id = request.data.get("user_profile")
            
            if not video_watch_data:
                
                points = RewardPointsStimulator.objects.filter(status=12).first()

                user_profile = UserProfile.objects.filter(id=user_profile_id).first()

                if MyRewardPoint.objects.filter(user_profile__id=user_profile_id).exists():
        
                    my_reward = MyRewardPoint.objects.filter(user_profile__id=user_profile_id).last()

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

                manager_josh_create_serializer.save()

                video_watch_data = watchTimeData.objects.filter(user_profile__id=request.data.get("user_profile"),leader_ship_task__id=request.data.get('leader_ship_task')).order_by('-id')[0]
    
                video_watch_data.bonus_point = int(points.multiplier)
                video_watch_data.save()
            else:
                points = RewardPointsStimulator.objects.filter(status=13).first()
                
                watch_time = int(str(request.data.get("spent_time")).split(":")[0])

                user_profile = UserProfile.objects.filter(id=user_profile_id).first()

                spent_time_minutes = spent_time_seconds/60

                if MyRewardPoint.objects.filter(user_profile__id=user_profile_id).exists():
        
                    my_reward = MyRewardPoint.objects.filter(user_profile__id=user_profile_id).last()

               
                    point_balance = my_reward.point_balance + int(int(points.multiplier)*spent_time_minutes)


                    my_reward = MyRewardPoint.objects.create(
                        manager_id=0,              
                        user_profile=user_profile,
                        earned_point=int(int(points.multiplier)*spent_time_minutes),
                        point_balance=point_balance
                    )
    
                else:
                    my_reward = MyRewardPoint.objects.create(
                        manager_id=0,              
                        user_profile=user_profile,
                        earned_point=int(int(points.multiplier)*spent_time_minutes),
                        point_balance=int(int(points.multiplier)*spent_time_minutes)
                    )
                    
                manager_josh_create_serializer.save()

                video_watch_data = watchTimeData.objects.filter(user_profile__id=request.data.get("user_profile"),leader_ship_task__id=request.data.get('leader_ship_task')).order_by('-id')[0]

                video_watch_data.bonus_point = int(int(points.multiplier)*spent_time_minutes)
                video_watch_data.save()

            return Response(data={'msg':'Data received Succesfully','Data':manager_josh_create_serializer.data,'response_code':200},status=status.HTTP_200_OK)      
        
        return Response({"msg":"Error"}, status=400)



# Read skill and hobby Time Data Serializer
@csrf_exempt
@api_view(['POST'])
@authenticate_token
def read_skill_and_hobby_time_data(request):
        spent_time_seconds = request.data.get('spent_time_seconds') 
        
        manager_josh_create_serializer=ReadSkillAndHobbyTimeDataSerializer(data=request.data)
        if manager_josh_create_serializer.is_valid():
            
            video_watch_data = ReadSkillAndHobbyData.objects.filter(user_profile__id=request.data.get("user_profile"),skill_and_hobby__id=request.data.get('skill_and_hobby'))
            
            video = SkillAndHobby.objects.filter(id=int(request.data.get('skill_and_hobby'))).first()
            
            user_profile_id = request.data.get("user_profile")

            if not video_watch_data:
                
                points = RewardPointsStimulator.objects.filter(status=14).first()

                user_profile = UserProfile.objects.filter(id=user_profile_id).first()

                if MyRewardPoint.objects.filter(user_profile__id=user_profile_id).exists():
        
                    my_reward = MyRewardPoint.objects.filter(user_profile__id=user_profile_id).last()

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

                manager_josh_create_serializer.save()
                
            else:
                points = RewardPointsStimulator.objects.filter(status=15).first()
                
                watch_time = int(str(request.data.get("spent_time")).split(":")[0])
  
                spent_time_minutes = spent_time_seconds/60

                user_profile = UserProfile.objects.filter(id=user_profile_id).first()

                if MyRewardPoint.objects.filter(user_profile__id=user_profile_id).exists():
        
                    my_reward = MyRewardPoint.objects.filter(user_profile__id=user_profile_id).last()

                    point_balance = my_reward.point_balance + int(int(points.multiplier)*spent_time_minutes)

                    my_reward = MyRewardPoint.objects.create(
                        manager_id=0,              
                        user_profile=user_profile,
                        earned_point=int(int(points.multiplier)*spent_time_minutes),
                        point_balance=point_balance
                    )
                else:
                    my_reward = MyRewardPoint.objects.create(
                        manager_id=0,              
                        user_profile=user_profile,
                        earned_point=int(int(points.multiplier)*spent_time_minutes),
                        point_balance=int(int(points.multiplier)*spent_time_minutes)
                    )
                
                manager_josh_create_serializer.save()
                
            return Response(data={'msg':'Data received Succesfully','Data':manager_josh_create_serializer.data,'response_code':200},status=status.HTTP_200_OK)      
        
        return Response({"msg":"Error"}, status=400)


# Learning Material Time Data Serializer
@csrf_exempt
@api_view(['POST'])
@authenticate_token
def learning_material_time_data(request):
        
        spent_time_seconds = request.data.get('spent_time_seconds') 
        
        manager_josh_create_serializer=LearningMaterialTimeDataSerializer(data=request.data)
        if manager_josh_create_serializer.is_valid():
            
            video_watch_data = LearningMaterialWatchTimeData.objects.filter(user_profile__id=request.data.get("user_profile"),learning_material__id=request.data.get('learning_material'))
            
            video = LearningMaterial.objects.filter(id=int(request.data.get('learning_material'))).first()
            
            user_profile_id = request.data.get("user_profile")

            if not video_watch_data:
                
                points = RewardPointsStimulator.objects.filter(status=30).first()

                user_profile = UserProfile.objects.filter(id=user_profile_id).first()

                if MyRewardPoint.objects.filter(user_profile__id=user_profile_id).exists():
        
                    my_reward = MyRewardPoint.objects.filter(user_profile__id=user_profile_id).last()

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
                
                manager_josh_create_serializer.save()
            
            else:
                points = RewardPointsStimulator.objects.filter(status=31).first()
                
                watch_time = int(str(request.data.get("spent_time")).split(":")[0])

                spent_time_minutes = spent_time_seconds/60


                user_profile = UserProfile.objects.filter(id=user_profile_id).first()

                if MyRewardPoint.objects.filter(user_profile__id=user_profile_id).exists():
        
                    my_reward = MyRewardPoint.objects.filter(user_profile__id=user_profile_id).last()

                    point_balance = my_reward.point_balance + int(int(points.multiplier)*spent_time_minutes)

                    my_reward = MyRewardPoint.objects.create(
                        manager_id=0,              
                        user_profile=user_profile,
                        earned_point=int(int(points.multiplier)*spent_time_minutes),
                        point_balance=point_balance
                    )
                else:
                    my_reward = MyRewardPoint.objects.create(
                        manager_id=0,              
                        user_profile=user_profile,
                        earned_point=int(int(points.multiplier)*spent_time_minutes),
                        point_balance=int(int(points.multiplier)*spent_time_minutes)
                    )
            
                manager_josh_create_serializer.save()
            
            return Response(data={'msg':'Data received Succesfully','Data':manager_josh_create_serializer.data,'response_code':200},status=status.HTTP_200_OK)      
        
        return Response({"msg":"Error"}, status=400)



# Customer Played Serializer
@csrf_exempt
@api_view(['POST'])
@authenticate_token
def customer_played_game_time(request):
        customer_played_Game_serializer= CustomerPlayedGameSerializer(data=request.data)
        
        user_profile_id = request.data.get('user_profile')
        
        if customer_played_Game_serializer.is_valid():

            points = RewardPointsStimulator.objects.filter(status=8).first()
            
            total_points = int(points.multiplier)

        
            user_profile = UserProfile.objects.filter(id=user_profile_id).first()


            customer_played_Game_serializer.save()

            current_date = datetime.now().date()
      
            customer_played_game_count = CustomerPlayedGame.objects.filter(user_profile__id=user_profile_id,created_at__date__lte=current_date).count()
      
            if customer_played_game_count:
                
                if not customer_played_game_count%5:

                    
                    end_date = current_date
                    inc = 1
                    
                    is_given = 0

                    while inc<=5:
                       
                        customer_played_game = CustomerPlayedGame.objects.filter(user_profile__id=user_profile_id,created_at__date=end_date).first()

                        if customer_played_game:
                            is_given +=1   

                        end_date = end_date - timedelta(days=1)   
                        
                        inc +=1   

                    if is_given==5:
                
                        points = RewardPointsStimulator.objects.filter(status=9).first()

                        total_points = total_points + int(points.multiplier)  

            if MyRewardPoint.objects.filter(user_profile__id=user_profile_id).exists():

                my_reward = MyRewardPoint.objects.filter(user_profile__id=user_profile_id).last()

                point_balance = my_reward.point_balance + int(total_points)

                my_reward = MyRewardPoint.objects.create(
                    manager_id=0,              
                    user_profile=user_profile,
                    earned_point=int(total_points),
                    point_balance=point_balance
                )
            else:
                my_reward = MyRewardPoint.objects.create(
                    manager_id=0,              
                    user_profile=user_profile,
                    earned_point=int(total_points),
                    point_balance=int(total_points)
                )

            game_point = GamePoint.objects.create(
            user_profile=user_profile,
            game_type_id = request.data.get('game_name'),
            is_won = True,
            bonus_point = total_points
            )

            return Response(data={'msg':'Data Sent Succesfully','Data':customer_played_Game_serializer.data,'response_code':200},status=status.HTTP_200_OK)

# Customer Played lists

@csrf_exempt
@api_view(['POST'])
@authenticate_token
def customer_played_game_list(request):
    if request.data.get("user_profile_id") == '' or request.data.get("user_profile_id") is None:  
        return Response({'message': 'Please provide user profile id', 'response_code':201}, status=HTTP_200_OK) 

    user_data = CustomerPlayedGame.objects.values().filter(user_profile__id=request.data.get("user_profile_id")).last()
    
    return Response(data={'msg':'Data received succesfully','Data':user_data,'response_code':200},status=status.HTTP_200_OK)
      


@csrf_exempt
@api_view(['GET'])
@authenticate_token
def challenge_point_data(request):
    try:
        user_profile_data = request.query_params.get('user_profile')
    except:
        return Response({'Msg':'Please Provide user_profile_data in params'})

    challenge_point=ChallengePoint.objects.filter().first()
    challenge_point_count=ChallengePoint.objects.filter().count()
    challenge_point_serializer=ChallengePointSerializer(challenge_point)

    return Response(data={'count':challenge_point_count,'msg':'Success','data':challenge_point_serializer.data,'response_code':200},status=status.HTTP_200_OK)




@csrf_exempt
@api_view(['POST'])
@authenticate_token
def win_level_and_points_won(request):
    if request.data.get("employee_id") == '' or request.data.get("employee_id") is None:  
        return Response({'message': 'Please provide employee id', 'response_code':201}, status=HTTP_200_OK) 
    
    my_reward_points = MyRewardPoint.objects.filter(user_profile__id=request.data.get("employee_id")).aggregate(Sum('earned_point'))
    
 
    points = my_reward_points['earned_point__sum']
    if not points:
        points = 0

    win_level_points = points
    
    point_level = PointLevel.objects.filter(status=1).first()


    if not win_level_points%point_level.points:
        win_level = int(win_level_points/point_level.points)
    else:
        win_level = int(win_level_points/point_level.points) + 1


    context = {}

    context['win_level']             = win_level

    context['points_won']            = points  
    
    context['message']               = 'Win level and win points received successfully'
    
    context['response_code']         = HTTP_200_OK

    return Response(context, status=HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
@authenticate_token
def kpi_met_and_wip(request):
    if request.data.get("employee_id") == '' or request.data.get("employee_id") is None:  
        return Response({'message': 'Please provide employee id', 'response_code':201}, status=HTTP_200_OK) 
    
    try:
        user_profile = UserProfile.objects.filter(id=request.data.get("employee_id")).first()
    except Exception as e:
        return Response({"message":str(e)}, status=HTTP_404_NOT_FOUND)

    if user_profile:
        current_date=datetime.now().date()
        current_time=datetime.now().strftime('%I:%M')

        current_month = current_date.month  
        
        # employee_kpi_met_data = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=user_profile.user.email,kpi_status=1,permormance_date__date__lte=current_date).count()

        # employee_kpi_wip_data = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=user_profile.user.email,kpi_status=0,permormance_date__month=current_month).count()

        kpi_data = KpiName.objects.filter(organiztaion__unique_code=user_profile.unique_code)
        
        kpi_met_count = 0
        
        kpi_wip_count = 0

        for kpi in kpi_data:

            if OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=user_profile.user.email,kpi_name_data__id=kpi.id).exists():
    
                manager_employee_kpi_data_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=user_profile.user.email,kpi_name_data__id=kpi.id).aggregate(Sum('kpi_target'))

                manager_employee_kpi_data_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=user_profile.user.email,kpi_name_data__id=kpi.id).aggregate(Sum('kpi_actual'))
                
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
                    elif kpi_target > kpi_actual:
                        kpi_wip_count +=1         


        # challenges = TeamAcceptChallengeHistory.objects.filter(customer_accepted_id=user_profile.id,team_challenge__is_completed_by_manager=0)
        # kpi_wip = 0
        # if challenges:
        #     for challenge in challenges:
        #         if challenge.team_challenge.start_time<=current_time and challenge.team_challenge.end_time>=current_time:
        #             kpi_wip +=1

        # team_campaigns = TeamAcceptCampaignHistory.objects.filter(customer_accepted_id=user_profile.id,team_campaign__is_completed_by_manager=0)
        # for campaign in team_campaigns:
        #     if campaign.team_campaign.start_date<=current_date and campaign.team_campaign.end_date>=current_date:
        #         kpi_data = len(campaign.team_campaign.criteria_point.all())
        #         kpi_wip +=kpi_data
        
        context = {}
        context['total_kpi_met']         = kpi_met_count
        context['total_kpi_wip']         = kpi_wip_count
        context['message']               = 'KPI met and wip data received successfully'
        context['response_code']         = HTTP_200_OK
        return Response(context, status=HTTP_200_OK)
        


# Challenge Point Serializer Data 
@csrf_exempt
@api_view(['GET'])
@authenticate_token
def challenge_point_data(request):
    try:
        user_profile_data = request.query_params.get('user_profile')
        if user_profile_data:
            context = {}
            challenge_data=ChallengePoint.objects.filter(user_profile__id=user_profile_data)
# Played count
            challenges_played_count=ChallengePoint.objects.filter(user_profile__id=user_profile_data).count()
# Won count
            challenges_won_count=ChallengePoint.objects.filter(user_profile__id=user_profile_data,is_won=True).count()
# Bonus Point
            challenges_bonus_point_count=ChallengePoint.objects.filter(user_profile__id=user_profile_data,is_won=True).aggregate(Sum('bonus_point'))
            
            context['challenge_bonus_point']      = challenges_bonus_point_count['bonus_point__sum']
            context['challenges_played_count']    = challenges_played_count
            context['challenges_won_count']       = challenges_won_count
            context['response_code']              = 200
            context['message']                    = f'Challenge_point_data successfully Getting for id {user_profile_data}'
            return Response(context,status=HTTP_200_OK)
        else:
            return Response({'msg':'Please Provide user_profile in params','response_code':201})
    except:
        return Response({'msg':'Please Provide user_profile in params'})
    


# Campaign Point Serializer

# Challenge Point Serializer Data 
@csrf_exempt
@api_view(['GET'])
@authenticate_token
def campaign_point_data(request):
    try:
        user_profile_data = request.query_params.get('user_profile')
        print(user_profile_data)
        if user_profile_data:
            context = {}
            campaign_data=CampaignPoint.objects.filter(user_profile__id=user_profile_data)
# Played count
            campaign_played_count=CampaignPoint.objects.filter(user_profile__id=user_profile_data).count()
# Won count
            campaign_won_count=CampaignPoint.objects.filter(user_profile__id=user_profile_data,is_won=True).count()
# Bonus Point
            campaign_bonus_point_count=CampaignPoint.objects.filter(user_profile__id=user_profile_data,is_won=True).aggregate(Sum('bonus_point'))
            context['campaign_bonus_point_count']   = campaign_bonus_point_count['bonus_point__sum']
            context['campaign_played_count']        = campaign_played_count
            context['campaign_won_count']           = campaign_won_count
            context['response_code']                = 200
            context['message']                      = f'Campaign point data successfully Getting for id {user_profile_data}'
            return Response(context,status=HTTP_200_OK)
        else:
            return Response({'msg':'Please Provide user_profile in params','response_code':201})
    except:
        return Response({'msg':'Please Provide user_profile in params'})
    



@csrf_exempt
@api_view(['GET'])
# @authenticate_token
def habbit_of_the_day_message(request):
    day = datetime.now().day

    health_habbit = HealthHabbit.objects.values_list('habbit_of_the_day',flat=True).filter(status=1,day=day)[0]
    
    context = {}
    context['health_habbit']   = health_habbit
    context['response_code']   = 200
    context['message']         = 'Success'

    return Response(context,status=HTTP_200_OK)



@csrf_exempt
@api_view(["POST"])
@authenticate_token
def save_steps_taken(request):
    if request.data.get("user_profile_id") == '' or request.data.get("user_profile_id") is None:  
        return Response({'message': 'Please provide user profile id', 'response_code':201}, status=HTTP_200_OK) 
    
    if request.data.get("steps_count") == '' or request.data.get("steps_count") is None:  
        return Response({'message': 'Please provide steps count', 'response_code':201}, status=HTTP_200_OK) 

    if request.data.get("date") == '' or request.data.get("date") is None:  
        return Response({'message': 'Please provide date', 'response_code':201}, status=HTTP_200_OK) 

    user_profile_id = request.data.get("user_profile_id")

    user_profile = UserProfile.objects.filter(id=user_profile_id).first()
    
    if StepsTaken.objects.filter(user_profile=user_profile,created_at__icontains=request.data.get("date")).exists():
        steps_taken = StepsTaken.objects.filter(user_profile=user_profile,created_at__icontains=request.data.get("date")).first()
        steps_taken.steps_count = request.data.get("steps_count")
        steps_taken.save()
    else:
        steps_taken = StepsTaken.objects.create(user_profile=user_profile,steps_count=request.data.get("steps_count"))
            
    points = RewardPointsStimulator.objects.filter(status=18).first()

    if MyRewardPoint.objects.filter(user_profile__id=user_profile_id).exists():

        my_reward = MyRewardPoint.objects.filter(user_profile__id=user_profile_id).last()

        point_balance = my_reward.point_balance + int(points.multiplier*request.data.get("steps_count"))

        my_reward = MyRewardPoint.objects.create(
            manager_id=0,              
            user_profile=user_profile,
            earned_point=int(points.multiplier*request.data.get("steps_count")),
            point_balance=point_balance
        )
    else:
        my_reward = MyRewardPoint.objects.create(
            manager_id=0,              
            user_profile=user_profile,
            earned_point=int(points.multiplier*request.data.get("steps_count")),
            point_balance=int(points.multiplier*request.data.get("steps_count"))
        )


    context = {}
    context['message']= 'Steps count data has been saved successfully' 
    context['response_code']            = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)


# Filter wellbeing data
@csrf_exempt
@api_view(["POST"])
@authenticate_token
def wellbeing_lists(request):
    if request.data.get("user_profile_id") == '' or request.data.get("user_profile_id") is None:  
        return Response({'message': 'Please provide user profile id', 'response_code':201}, status=HTTP_200_OK) 

    if request.data.get("time_period_all") == '' or request.data.get("time_period_all") is None:  
        return Response({'message': 'Please provide time period all', 'response_code':201}, status=HTTP_200_OK) 

    time_period_all = request.data.get("time_period_all")

    current_date = datetime.now().date()
    
    user_profile = UserProfile.objects.filter(id=request.data.get("user_profile_id")).first()
    
    if time_period_all=="today":

        steps_taken     = StepsTaken.objects.filter(user_profile=user_profile,created_at__icontains=current_date).aggregate(Sum('steps_count'))

        if not steps_taken['steps_count__sum']:
            steps_count = 0
        else:
            steps_count = steps_taken['steps_count__sum']        

        health_metric = HealthMetric.objects.filter(status=1,active=1).first()
        
        steps_percent = 0.0

        if steps_count:
            steps_percent = ((steps_count/health_metric.target)*health_metric.weightage)*100  
        

        learning_data   = ReadSkillAndHobbyData.objects.filter(user_profile = user_profile,created_at__icontains=current_date).aggregate(Sum('spent_time_seconds'))
        
        if not learning_data['spent_time_seconds__sum']:
            learning_hours = 0
        else:
            learning_hours = convert_seconds_to_hours(learning_data['spent_time_seconds__sum'])         
        
        health_metric = HealthMetric.objects.filter(status=2,active=1).first()
        
        learning_percent = 0.0

        if learning_hours:
            total_minutes = convert_seconds_to_minutes(learning_data['spent_time_seconds__sum'])

            learning_percent = ((total_minutes/health_metric.target)*health_metric.weightage)*100 



        meditation_data = watchTimeData.objects.filter(user_profile=user_profile,created_at__icontains=current_date).aggregate(Sum('spent_time_seconds'))  # Health and Fitness

        if not meditation_data['spent_time_seconds__sum']:
            meditation_hours = 0
        else:
            meditation_hours = convert_seconds_to_hours(meditation_data['spent_time_seconds__sum'])         
        

        health_metric = HealthMetric.objects.filter(status=3,active=1).first()
 
        meditation_percent = 0.0

        if meditation_hours:
            total_minutes = convert_seconds_to_minutes(meditation_data['spent_time_seconds__sum'])

            meditation_percent = ((total_minutes/health_metric.target)*health_metric.weightage)*100 


    elif time_period_all=="yesterday":
        yesterday_date = current_date-timedelta(days=1)

        steps_taken     = StepsTaken.objects.filter(user_profile=user_profile,created_at__icontains=yesterday_date).aggregate(Sum('steps_count'))

        if not steps_taken['steps_count__sum']:
            steps_count = 0
        else:
            steps_count = steps_taken['steps_count__sum']        
        
        health_metric = HealthMetric.objects.filter(status=1,active=1).first()
        
        steps_percent = 0.0

        if steps_count:
            steps_percent = ((steps_count/health_metric.target)*health_metric.weightage)*100  
        
        
        learning_data   = ReadSkillAndHobbyData.objects.filter(user_profile = user_profile,created_at__icontains=yesterday_date).aggregate(Sum('spent_time_seconds'))
        
        if not learning_data['spent_time_seconds__sum']:
            learning_hours = 0
        else:
            learning_hours = convert_seconds_to_hours(learning_data['spent_time_seconds__sum'])         

        
        health_metric = HealthMetric.objects.filter(status=2,active=1).first()
        
        learning_percent = 0.0

        if learning_hours:
            total_minutes = convert_seconds_to_minutes(learning_data['spent_time_seconds__sum'])

            learning_percent = ((total_minutes/health_metric.target)*health_metric.weightage)*100


        meditation_data = watchTimeData.objects.filter(user_profile=user_profile,created_at__icontains=yesterday_date).aggregate(Sum('spent_time_seconds'))  # Health and Fitness

        if not meditation_data['spent_time_seconds__sum']:
            meditation_hours = 0
        else:
            meditation_hours = convert_seconds_to_hours(meditation_data['spent_time_seconds__sum'])         

        health_metric = HealthMetric.objects.filter(status=3,active=1).first()
 
        meditation_percent = 0.0

        if meditation_hours:
            total_minutes = convert_seconds_to_minutes(meditation_data['spent_time_seconds__sum'])

            meditation_percent = ((total_minutes/health_metric.target)*health_metric.weightage)*100

    
    elif time_period_all=="wtd":
        end_date   = current_date
        start_date = end_date -timedelta(days=7)
        
     
        steps_taken     = StepsTaken.objects.filter(user_profile=user_profile,created_at__date__range=[start_date,end_date]).aggregate(Sum('steps_count'))

        if not steps_taken['steps_count__sum']:
            steps_count = 0
        else:
            steps_count = steps_taken['steps_count__sum']        


        health_metric = HealthMetric.objects.filter(status=1,active=1).first()
        
        steps_percent = 0.0

        if steps_count:
            steps_percent = ((steps_count/health_metric.target)*health_metric.weightage)*100  
        

        learning_data   = ReadSkillAndHobbyData.objects.filter(user_profile = user_profile,created_at__date__range=[start_date,end_date]).aggregate(Sum('spent_time_seconds'))
        
        if not learning_data['spent_time_seconds__sum']:
            learning_hours = 0
        else:
            learning_hours = convert_seconds_to_hours(learning_data['spent_time_seconds__sum'])         

        health_metric = HealthMetric.objects.filter(status=2,active=1).first()
        
        learning_percent = 0.0

        if learning_hours:
            total_minutes = convert_seconds_to_minutes(learning_data['spent_time_seconds__sum'])

            learning_percent = ((total_minutes/health_metric.target)*health_metric.weightage)*100


        meditation_data = watchTimeData.objects.filter(user_profile=user_profile,created_at__date__range=[start_date,end_date]).aggregate(Sum('spent_time_seconds'))  # Health and Fitness

        if not meditation_data['spent_time_seconds__sum']:
            meditation_hours = 0
        else:
            meditation_hours = convert_seconds_to_hours(meditation_data['spent_time_seconds__sum'])         


        health_metric = HealthMetric.objects.filter(status=3,active=1).first()
 
        meditation_percent = 0.0

        if meditation_hours:
            total_minutes = convert_seconds_to_minutes(meditation_data['spent_time_seconds__sum'])

            meditation_percent = ((total_minutes/health_metric.target)*health_metric.weightage)*100

    
    elif time_period_all=="mtd":
        month = current_date.month
        year = current_date.year
        
       
        steps_taken     = StepsTaken.objects.filter(user_profile=user_profile,created_at__year=year,created_at__month=month).aggregate(Sum('steps_count'))

        if not steps_taken['steps_count__sum']:
            steps_count = 0
        else:
            steps_count = steps_taken['steps_count__sum']

        health_metric = HealthMetric.objects.filter(status=1,active=1).first()
        
        steps_percent = 0.0

        if steps_count:
            steps_percent = ((steps_count/health_metric.target)*health_metric.weightage)*100  
        

        learning_data   = ReadSkillAndHobbyData.objects.filter(user_profile = user_profile,created_at__year=year,created_at__month=month).aggregate(Sum('spent_time_seconds'))
        
        if not learning_data['spent_time_seconds__sum']:
            learning_hours = 0
        else: 
            learning_hours = convert_seconds_to_hours(learning_data['spent_time_seconds__sum'])         

        health_metric = HealthMetric.objects.filter(status=2,active=1).first()
        
        learning_percent = 0.0

        if learning_hours:
            total_minutes = convert_seconds_to_minutes(learning_data['spent_time_seconds__sum'])

            learning_percent = ((total_minutes/health_metric.target)*health_metric.weightage)*100


        meditation_data = watchTimeData.objects.filter(user_profile=user_profile,created_at__year=year,created_at__month=month).aggregate(Sum('spent_time_seconds'))  # Health and Fitness

        if not meditation_data['spent_time_seconds__sum']:
            meditation_hours = 0
        else:
            meditation_hours = convert_seconds_to_hours(meditation_data['spent_time_seconds__sum'])         

        health_metric = HealthMetric.objects.filter(status=3,active=1).first()
 
        meditation_percent = 0.0

        if meditation_hours:
            total_minutes = convert_seconds_to_minutes(meditation_data['spent_time_seconds__sum'])

            meditation_percent = ((total_minutes/health_metric.target)*health_metric.weightage)*100


    elif time_period_all=="ytd":
        year = current_date.year
        
     
        steps_taken     = StepsTaken.objects.filter(user_profile=user_profile,created_at__year=year).aggregate(Sum('steps_count'))

        if not steps_taken['steps_count__sum']:
            steps_count = 0
        else:
            steps_count = steps_taken['steps_count__sum']        


        health_metric = HealthMetric.objects.filter(status=1,active=1).first()
        
        steps_percent = 0.0

        if steps_count:
            steps_percent = ((steps_count/health_metric.target)*health_metric.weightage)*100  
        

        learning_data   = ReadSkillAndHobbyData.objects.filter(user_profile = user_profile,created_at__year=year).aggregate(Sum('spent_time_seconds'))
        
        if not learning_data['spent_time_seconds__sum']:
            learning_hours = 0
        else:
            learning_hours = convert_seconds_to_hours(learning_data['spent_time_seconds__sum'])         

        health_metric = HealthMetric.objects.filter(status=2,active=1).first()
        
        learning_percent = 0.0

        if learning_hours:
            total_minutes = convert_seconds_to_minutes(learning_data['spent_time_seconds__sum'])

            learning_percent = ((total_minutes/health_metric.target)*health_metric.weightage)*100


        meditation_data = watchTimeData.objects.filter(user_profile=user_profile,created_at__year=year).aggregate(Sum('spent_time_seconds'))  # Health and Fitness

        if not meditation_data['spent_time_seconds__sum']:
            meditation_hours = 0
        else:
            meditation_hours = convert_seconds_to_hours(meditation_data['spent_time_seconds__sum'])         


        health_metric = HealthMetric.objects.filter(status=3,active=1).first()
 
        meditation_percent = 0.0

        if meditation_hours:
            total_minutes = convert_seconds_to_minutes(meditation_data['spent_time_seconds__sum'])

            meditation_percent = ((total_minutes/health_metric.target)*health_metric.weightage)*100


    elif time_period_all=="all":
        steps_taken     = StepsTaken.objects.filter(user_profile=user_profile).aggregate(Sum('steps_count'))

        if not steps_taken['steps_count__sum']:
            steps_count = 0
        else:
            steps_count = steps_taken['steps_count__sum']        

        health_metric = HealthMetric.objects.filter(status=1,active=1).first()
        
        steps_percent = 0.0

        if steps_count:

            steps_percent = ((steps_count/health_metric.target)*health_metric.weightage)*100  
        

        learning_data   = ReadSkillAndHobbyData.objects.filter(user_profile = user_profile).aggregate(Sum('spent_time_seconds'))
        
       
        if not learning_data['spent_time_seconds__sum']:
            learning_hours = 0
        else:
            learning_hours = convert_seconds_to_hours(learning_data['spent_time_seconds__sum'])         


        health_metric = HealthMetric.objects.filter(status=2,active=1).first()
        
        learning_percent = 0.0

        if learning_hours:
            total_minutes = convert_seconds_to_minutes(learning_data['spent_time_seconds__sum'])
          
            learning_percent = ((total_minutes/health_metric.target)*health_metric.weightage)*100



        meditation_data = watchTimeData.objects.filter(user_profile=user_profile).aggregate(Sum('spent_time_seconds'))  # Health and Fitness

        if not meditation_data['spent_time_seconds__sum']:
            meditation_hours = 0
        else:
            meditation_hours = convert_seconds_to_hours(meditation_data['spent_time_seconds__sum'])         

        health_metric = HealthMetric.objects.filter(status=3,active=1).first()
 
        meditation_percent = 0.0

        if meditation_hours:
            total_minutes = convert_seconds_to_minutes(meditation_data['spent_time_seconds__sum'])
            
            meditation_percent = ((total_minutes/health_metric.target)*health_metric.weightage)*100
        
       
    context = {}
    
    context['steps_count']         = steps_count
    
    context['learning_hours']      = learning_hours  # skill and hobby

    context['meditation_hours']    = meditation_hours

    context['wellbeing_percent']   = round(steps_percent + learning_percent + meditation_percent,2)
   
    context['message']= 'Wellbeing data has been received successfully'

    context['response_code']            = HTTP_200_OK

    return Response(context, status=HTTP_200_OK)





@csrf_exempt
@api_view(['POST'])
@authenticate_token
def kpi_performance_lists(request):
    if request.data.get("employee_id") == '' or request.data.get("employee_id") is None:  
        return Response({'message': 'Please provide employee id', 'response_code':201}, status=HTTP_200_OK) 

    if request.data.get("unique_code") == '' or request.data.get("unique_code") is None:  
        return Response({'message': 'Please provide unique code', 'response_code':201}, status=HTTP_200_OK) 

    try:
        user_profile = UserProfile.objects.filter(id=request.data.get("employee_id")).first()
    except Exception as e:
        return Response({"message":str(e)}, status=HTTP_404_NOT_FOUND)

    if user_profile:
        current_date=datetime.now().date()
        current_time=datetime.now().strftime('%I:%M')

        month = datetime.now().month


        kpi_obj = KpiName.objects.filter(organiztaion__unique_code=request.data.get("unique_code"))

        kpi_percent_data = []

        total_percent = 0

        total_no_kpi = 0

        for kpi in kpi_obj:

            employee_kpi_performance_data = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=user_profile.user.email,kpi_name=kpi.name)
            
            employee_kpi_performance_data_target = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=user_profile.user.email,kpi_name=kpi.name).aggregate(Sum('kpi_target'))
            
            employee_kpi_performance_data_actual = OrganizationEmployeePerformanceData.objects.filter(organization_employee_data__email=user_profile.user.email,kpi_name=kpi.name).aggregate(Sum('kpi_actual'))
            
            kpi_target = employee_kpi_performance_data_target['kpi_target__sum']     
 
            kpi_actual = employee_kpi_performance_data_actual['kpi_actual__sum']

            if not kpi_target:
                kpi_target = 1

            data = {}

            if kpi_target!=None and kpi_actual!=None:           
  
                if kpi_actual<kpi_target:
                    data['kpi_name']    = kpi.name
                    data['kpi_percent'] = round((kpi_actual/kpi_target)*100,2)
                    data['kpi_status']  = "Not met"

                elif kpi_actual>=kpi_target:
                    data['kpi_name']    = kpi.name
                    data['kpi_percent'] = round((kpi_actual/kpi_target)*100,2)
                    data['kpi_status']  = "Met"

                total_percent +=round((kpi_actual/kpi_target)*100,2)

                total_no_kpi +=1

                kpi_percent_data.append(data)

        if not total_no_kpi:
            total_no_kpi = 1

        context = {}

        context['total_kpi_percent_data'] = total_percent/total_no_kpi

        context['kpi_percent_data']      = kpi_percent_data

        context['message']               = 'KPI performance data received successfully'
        context['response_code']         = HTTP_200_OK
        return Response(context, status=HTTP_200_OK)

#   path('game-point-list/',game_point_list),

@csrf_exempt
@api_view(['POST'])
@authenticate_token
def game_point_list(request):
    if request.data.get("employee_id") == '' or request.data.get("employee_id") is None:  
        return Response({'message': 'Please provide employee id', 'response_code':201}, status=HTTP_200_OK) 


    total_played_games = GamePoint.objects.filter(user_profile__id=request.data.get("employee_id")).count()

    game_point = GamePoint.objects.filter(user_profile__id=request.data.get("employee_id")).aggregate(Sum('bonus_point'))
   

    if not game_point['bonus_point__sum']:
        total_point = 0
    else:
        total_point = game_point['bonus_point__sum']     

    context = {}
    context['total_played_games']    = total_played_games
    context['total_bonus']           = total_point

    context['message']               = 'Game point data received successfully'
    context['response_code']         = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)




# Motivational Message

@csrf_exempt
@api_view(['POST'])
# @authenticate_token
def user_motivational_message_list(request):
    if request.data.get("employee_id") == '' or request.data.get("employee_id") is None:  
        return Response({'message': 'Please provide employee id', 'response_code':201}, status=HTTP_200_OK) 
    
 
    user_employee = UserProfile.objects.filter(id=request.data.get("employee_id")).first()
    
    team_id = user_employee.team_id
    
    team_member_id = UserProfile.objects.filter(team_id=team_id,role__id=1).values_list('id',flat=True)
    
    
    employee_sum_data = {}

    user_count = 0

    for employee_id in team_member_id:
        single_employee = MyRewardPoint.objects.filter(user_profile__id=employee_id).aggregate(Sum('earned_point'))
        user_count +=1 
        if single_employee['earned_point__sum']: 
            employee_sum_data[employee_id]= single_employee['earned_point__sum']
    
    status = 0

    if employee_sum_data:
        top_ten_data = {k: v for k, v in sorted(employee_sum_data.items(), key=lambda employee_sum_data: employee_sum_data[1],reverse=True)[:10]}

        for key,value in top_ten_data.items():
            user_profile = UserProfile.objects.filter(id=int(key)).first()
            if user_employee.id==user_profile.id:
               status = 1

        bottom_ten_data = {k: v for k, v in sorted(employee_sum_data.items(), key=lambda employee_sum_data: employee_sum_data[1],reverse=False)[:10]}

        for key,value in bottom_ten_data.items():
            user_profile = UserProfile.objects.filter(id=int(key)).first()
            if user_employee.id==user_profile.id:
    
                if user_count>=20:
                   status = 2
        
        if status==1:
            # top 10
            msg = "Well done, you are in the Top 10, give yourself a pat on the back and keep it up"
        elif status==2:
            # bottom 10
            msg = "We know it can be hard, but you can still do it, we know you can"
        else:
            # middle 80
            msg = "You are going good, push yourself harder and see yourself in the Top 10"

    context = {}
    
    context['motivation_message']    = msg
    context['message']               = 'Success'
    context['response_code']         = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)




#  Filter employee data bar chart and pie chart graph

@csrf_exempt
@api_view(["POST"])
# @authenticate_token
def filter_employee_bar_chart_and_pie_chart(request):
    if request.data.get("employee_id") == '' or request.data.get("employee_id") is None:  
        return Response({'message': 'Please provide employee id', 'response_code':201}, status=HTTP_200_OK) 

    employee_id = request.data.get("employee_id")

    activity_type = request.data.get('activity_type')  # game // challenge // kpi

    time_period = request.data.get('time_period')


    current_date   = date.today()
    datas = []
    

    # Game


    if time_period=="all" and activity_type=="game":
        games = GamePoint.objects.filter(user_profile__id=employee_id).order_by('-id')[:4]


        for game in games:
            employee_game_item = {}
            game_name = GameName.objects.filter(id=game.game_type_id).first()
            employee_game_item['game_name']= game_name.game_type
            employee_game_item['game_date']= game.created_at.date()
            employee_game_item['game_bonus_point']= game.bonus_point

            datas.append(employee_game_item)
 
    elif time_period=="today" and activity_type=="game":
        games = GamePoint.objects.filter(user_profile__id=employee_id,created_at=current_date).order_by('-id')[:4]

        for game in games:
            employee_game_item= {}
            game_name = GameName.objects.filter(id=game.game_type_id).first()
            employee_game_item['game_name']= game_name.game_type
            employee_game_item['game_date']= game.created_at.date()
            employee_game_item['game_bonus_point']= game.bonus_point
            # at last append this data on empty list
            datas.append(employee_game_item)


    
    elif time_period=="yesterday" and activity_type=="game":
        yesterday_date = current_date-timedelta(days=1)

        games = GamePoint.objects.filter(user_profile__id=employee_id,created_at=yesterday_date).order_by('-id')[:4]


        for game in games:
            employee_game_item= {}
            game_name = GameName.objects.filter(id=game.game_type_id).first()
            employee_game_item['game_name']= game_name.game_type
            employee_game_item['game_date']= game.created_at.date()
            employee_game_item['game_bonus_point']= game.bonus_point
            # at last append this data on empty list
            datas.append(employee_game_item)

     
    elif  time_period=="wtd" and activity_type=="game":
        end_date   = current_date
        start_date = end_date -timedelta(days=7)
        games = GamePoint.objects.filter(user_profile__id=employee_id,created_at=start_date).order_by('-id')[:4]

        for game in games:
            employee_game_item= {}
            game_name = GameName.objects.filter(id=game.game_type_id).first()
            employee_game_item['game_name']= game_name.game_type
            employee_game_item['game_date']= game.created_at.date()
            employee_game_item['game_bonus_point']= game.bonus_point
            # at last append this data on empty list
            datas.append(employee_game_item)


    elif time_period=="mtd" and activity_type=="game":
        month = current_date.month
        year = current_date.year
        games = GamePoint.objects.filter(user_profile__id=employee_id,created_at=month).order_by('-id')[:4]

        for game in games:
            employee_game_item= {}
            game_name = GameName.objects.filter(id=game.game_type_id).first()
            employee_game_item['game_name']= game_name.game_type
            employee_game_item['game_date']= game.created_at.date()
            employee_game_item['game_bonus_point']= game.bonus_point
            # at last append this data on empty list
            datas.append(employee_game_item)

    elif  time_period=="ytd" and activity_type=="game":
        year = current_date.year
        games = GamePoint.objects.filter(user_profile__id=employee_id,created_at=year).order_by('-id')[:4]

        for game in games:
            employee_game_item= {}
            game_name = GameName.objects.filter(id=game.game_type_id).first()
            employee_game_item['game_name']= game_name.game_type
            employee_game_item['game_date']= game.created_at.date()
            employee_game_item['game_bonus_point']= game.bonus_point
            # at last append this data on empty list
            datas.append(employee_game_item)



    # Challenge

    elif time_period=="all" and activity_type=="challenge":
        challenges = ChallengePoint.objects.filter(user_profile__id=employee_id).order_by('-id')[:4]

        for challenge in challenges:
            if challenge.is_won==True:
                employee_challenge_item= {}
                kpi_name = KpiName.objects.filter(id=challenge.challenge.kpi_name_id).first()
                employee_challenge_item['game_name']= kpi_name.name
                employee_challenge_item['game_date']= challenge.created_at.date()
                employee_challenge_item['game_bonus_point']= challenge.bonus_point
                # at last append this data on empty list
                datas.append(employee_challenge_item)

    elif time_period=="today" and activity_type=="challenge":
        challenges = ChallengePoint.objects.filter(user_profile__id=employee_id,created_at__icontains=current_date).order_by('-id')[:4]

        for challenge in challenges:
            if challenge.is_won==True:
                employee_challenge_item= {}
                kpi_name = KpiName.objects.filter(id=challenge.challenge.kpi_name_id).first()
                employee_challenge_item['game_name']= kpi_name.name
                employee_challenge_item['game_date']= challenge.created_at.date()
                employee_challenge_item['game_bonus_point']= challenge.bonus_point
                # at last append this data on empty list
                datas.append(employee_challenge_item)
    
    elif time_period=="yesterday" and activity_type=="challenge":
        yesterday_date = current_date-timedelta(days=1)
        challenges = ChallengePoint.objects.filter(user_profile__id=employee_id,created_at__icontains=yesterday_date).order_by('-id')[:4]

        for challenge in challenges:
            if challenge.is_won==True:
                employee_challenge_item= {}
                kpi_name = KpiName.objects.filter(id=challenge.challenge.kpi_name_id).first()
                employee_challenge_item['game_name']= kpi_name.name
                employee_challenge_item['game_date']= challenge.created_at.date()
                employee_challenge_item['game_bonus_point']= challenge.bonus_point
                # at last append this data on empty list
                datas.append(employee_challenge_item)
     
     
    elif  time_period=="wtd" and activity_type=="challenge":
        end_date   = current_date
        start_date = end_date -timedelta(days=7)
        
        challenges = ChallengePoint.objects.filter(user_profile__id=employee_id,created_at__range=[start_date,end_date]).order_by('-id')[:4]

        for challenge in challenges:
            if challenge.is_won==True:
                employee_challenge_item= {}
                kpi_name = KpiName.objects.filter(id=challenge.challenge.kpi_name_id).first()
                employee_challenge_item['game_name']= kpi_name.name
                employee_challenge_item['game_date']= challenge.created_at.date()
                employee_challenge_item['game_bonus_point']= challenge.bonus_point
                # at last append this data on empty list
                datas.append(employee_challenge_item)

    elif time_period=="mtd" and activity_type=="challenge":
        month = current_date.month
        year = current_date.year
        challenges = ChallengePoint.objects.filter(user_profile__id=employee_id,created_at__month=month,created_at__year=year).order_by('-id')[:4]

        for challenge in challenges:
            if challenge.is_won==True:
                employee_challenge_item= {}
                kpi_name = KpiName.objects.filter(id=challenge.challenge.kpi_name_id).first()
                employee_challenge_item['game_name']= kpi_name.name
                employee_challenge_item['game_date']= challenge.created_at.date()
                employee_challenge_item['game_bonus_point']= challenge.bonus_point
                # at last append this data on empty list
                datas.append(employee_challenge_item)


    elif  time_period=="ytd" and activity_type=="challenge":
        year = current_date.year
        challenges = ChallengePoint.objects.filter(user_profile__id=employee_id,created_at__year=year).order_by('-id')[:4]

        for challenge in challenges:
            if challenge.is_won==True:
                employee_challenge_item= {}
                kpi_name = KpiName.objects.filter(id=challenge.challenge.kpi_name_id).first()
                employee_challenge_item['game_name']= kpi_name.name
                employee_challenge_item['game_date']= challenge.created_at.date()
                employee_challenge_item['game_bonus_point']= challenge.bonus_point
                # at last append this data on empty list
                datas.append(employee_challenge_item)

    # # KPI

    # elif time_period=="all" and activity_type=="kpi":
    #         teams_reward_data = MyRewardPoint.objects.values_list('user_profile__id',flat=True).filter(manager_id=manager_id)
 
    # elif time_period=="today" and activity_type=="kpi":
    #     teams_reward_data = MyRewardPoint.objects.values_list('user_profile__id',flat=True).filter(manager_id=manager_id,created_at__icontains=current_date)
  
    
    # elif time_period=="yesterday" and activity_type=="kpi":
    #     yesterday_date = current_date-timedelta(days=1)
    #     teams_reward_data = MyRewardPoint.objects.values_list('user_profile__id',flat=True).filter(manager_id=manager_id,created_at__icontains=yesterday_date)
     
     
    # elif  time_period=="wtd" and activity_type=="kpi":
    #     end_date   = current_date
    #     start_date = end_date -timedelta(days=7)
    #     teams_reward_data = MyRewardPoint.objects.values_list('user_profile__id',flat=True).filter(manager_id=manager_id, created_at__date__range=[start_date,end_date])


    # elif time_period=="mtd" and activity_type=="kpi":
    #     month = current_date.month
    #     year = current_date.year
    #     teams_reward_data = MyRewardPoint.objects.values_list('user_profile__id',flat=True).filter(manager_id=manager_id,created_at__month=month,created_at__year=year)


    # elif  time_period=="ytd" and activity_type=="kpi":
    #     year = current_date.year
    #     teams_reward_data = MyRewardPoint.objects.values_list('user_profile__id',flat=True).filter(manager_id=manager_id,created_at__date__year=year)

    # else:
    #     return Response(data={'msg':'please provide valid data','response_code':201},status=status.HTTP_201_CREATED)

  
    context = {}
    context['message']               = 'Bar chart and pie chart data have been received successfully'
    context['data']                  =  datas
    # context['challenge_data']        = challenge_data

    context['response_code']         = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)

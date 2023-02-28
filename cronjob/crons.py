
import requests
from datetime import datetime,date, timedelta

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
from rest_framework.response import Response

from admin_user.models import *
from line_manager_app.models import *
from customer_service_app.models import *
import pandas as pd

from utils.helpers import *

from accounts.models import *
from django.db.models import Sum

# # Executed every second
# @csrf_exempt
# @api_view(["GET"])
# @permission_classes((AllowAny,))
# def challenge_cronjob_points_distribution(request):
#     current_date_time=datetime.now()
    
#     current_date_time=current_date_time
    
#     current_date=current_date_time.date()

#     current_time=current_date_time.strftime('%I:%M')
    
#     if TeamAcceptChallengeHistory.objects.values().filter(team_challenge__is_broadcasted=1,team_challenge__updated_at__date=current_date,team_challenge__is_completed_by_manager=1,team_challenge__end_challenge_time=current_time,is_accepted=1).exists():
#         team_challenges = TeamAcceptChallengeHistory.objects.filter(team_challenge__is_broadcasted=1,team_challenge__updated_at__date=current_date,team_challenge__is_completed_by_manager=1,team_challenge__end_challenge_time=current_time,is_accepted=1)
#         for challenge in team_challenges:
          
#             try:
#                 kpi_name = KpiName.objects.get(id=challenge.team_challenge.kpi_name_id)
#             except Exception as e:
#                 kpi_name = None

#             if kpi_name:
#                 kpi_name=kpi_name.name
#             else:
#                 kpi_name=None        

#             try:
#                 user_profile = UserProfile.objects.get(id=challenge.customer_accepted_id)
#             except Exception as e:
#                 user_profile = None

#             if user_profile:
#                 email=user_profile.user.email    
#             else:
#                 email=None

#             employee_performance = OrganizationEmployeePerformanceData.objects.filter(permormance_date__icontains=current_date,kpi_name=kpi_name,organization_employee_data__email=email).first()
            
#             if employee_performance:
#                 if employee_performance.kpi_status==1:
#                     challenge_point = ChallengePoint.objects.create(
#                         user_profile=user_profile,
#                         challenge=challenge.team_challenge,
#                         is_won=True,
#                         bonus_point=challenge.team_challenge.bonus_point
#                     )
                
#                     if MyRewardPoint.objects.filter(user_profile__id=user_profile.id).exists():
#                         my_reward = MyRewardPoint.objects.filter(user_profile__id=user_profile.id).last()
#                         point_balance = my_reward.point_balance + challenge.team_challenge.bonus_point
#                         my_reward = MyRewardPoint.objects.create(
#                             manager_id=challenge.team_challenge.manager.id,              
#                             user_profile=user_profile,
#                             earned_point=challenge.team_challenge.bonus_point,
#                             point_balance=point_balance
#                         )
#                     else:
#                         my_reward = MyRewardPoint.objects.create(
#                             manager_id=challenge.team_challenge.manager.id,              
#                             user_profile=user_profile,
#                             earned_point=challenge.team_challenge.bonus_point,
#                             point_balance=challenge.team_challenge.bonus_point
#                         )
#                 else:
#                     challenge_point = ChallengePoint.objects.create(
#                         user_profile=user_profile,
#                         challenge=challenge.team_challenge,
#                         is_won=False,
#                         bonus_point=0
#                     )

#     context = {}
#     context['message']= 'Success' 
#     context['response_code']            = HTTP_200_OK
#     return Response(context, status=HTTP_200_OK)
        
# # Executed every second
# @csrf_exempt
# @api_view(["GET"])
# @permission_classes((AllowAny,))
# def campaign_cronjob_points_distribution(request):

#     current_date = datetime.now().date()

    
#     if TeamAcceptCampaignHistory.objects.values().filter(team_campaign__is_broadcasted=1,team_campaign__is_completed_by_manager=1,team_campaign__end_campaign_date=current_date,is_accepted=1).exists():

#         team_campaigns = TeamAcceptCampaignHistory.objects.filter(team_campaign__is_broadcasted=1,team_campaign__is_completed_by_manager=1,team_campaign__end_campaign_date=current_date,is_accepted=1)
#         for campaign in team_campaigns:
#             try:
#                 user_profile = UserProfile.objects.get(id=campaign.customer_accepted_id)
#             except Exception as e:
#                 user_profile = None

#             if user_profile:
#                 email=user_profile.user.email    
#             else:
#                 email=None

#             employee_performances = OrganizationEmployeePerformanceData.objects.filter(permormance_date__date__range=[campaign.start_date,campaign.end_date],email=email)
#             for employee_performance in employee_performances:
#                 kpi_data = campaign.team_campaign.criteria_point.filter(value=employee_performance.kpi_name).first()
#                 if kpi_data:    
#                     if employee_performance.kpi_status==1:
                    
#                         campaign_point =CampaignPoint.objects.create(
#                             user_profile=user_profile,
#                             campaign=campaign.team_campaign,
#                             is_won=True,
#                             bonus_point=kpi_data.point
#                         )

#                         if MyRewardPoint.objects.filter(user_profile__id=user_profile.id).exists():
#                             my_reward = MyRewardPoint.objects.filter(user_profile__id=user_profile.id).last()
#                             point_balance = my_reward.point_balance + kpi_data.point
#                             my_reward = MyRewardPoint.objects.create(
#                                 manager_id=campaign.manager.id,              
#                                 user_profile=user_profile,
#                                 earned_point=kpi_data.point,
#                                 point_balance=point_balance
#                             )
#                         else:
#                             my_reward = MyRewardPoint.objects.create(
#                                 manager_id=campaign.team_campaign.manager.id,              
#                                 user_profile=user_profile,
#                                 earned_point=kpi_data.point,
#                                 point_balance=kpi_data.point
#                             )
#                     else:
#                         campaign_point =CampaignPoint.objects.create(
#                             user_profile=user_profile,
#                             campaign=campaign.team_campaign,
#                             is_won=False,
#                             bonus_point=0
#                         )
#     context = {}
#     context['message']= 'Success' 
#     context['response_code']            = HTTP_200_OK
#     return Response(context, status=HTTP_200_OK)
    

# Executed every second

@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def end_challenge_cronjob(request):
    current_date_time=datetime.now()

    current_datetime = current_date_time
    
    current_date= current_datetime.date()

    current_time=current_datetime.strftime("%H:%M:%S")

    if TeamChallenge.objects.values().filter(is_broadcasted=1,updated_at__date=current_date,end_time=current_time,is_completed_by_manager=0).exists():
        team_challenges = TeamChallenge.objects.filter(is_broadcasted=1,updated_at__date=current_date,is_completed_by_manager=0,end_time=current_time)
        for team_challenge in team_challenges:
            team_challenge.is_completed_by_manager=1
            team_challenge.end_challenge_time=current_time

            team_challenge.save()
    context = {}
    context['message']= 'Success' 
    context['response_code']            = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)

# Executed every second
@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def end_campaign_cronjob(request):
    current_date=datetime.now().date()
    
    if TeamCampaign.objects.values().filter(is_broadcasted=1,is_completed_by_manager=0,end_date=current_date).exists():
        team_campaigns = TeamCampaign.objects.filter(is_broadcasted=1,is_completed_by_manager=0,end_date=current_date)
        for team_campaign in team_campaigns:
            team_campaign.is_completed_by_manager=1
            team_campaign.end_campaign_date=current_date
            team_campaign.save()
     
    context = {}
    context['message']= 'Success' 
    context['response_code']            = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)



# Executed every day at 8:30 AM for customers and managers
@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def my_resource_cronjob(request):
    user_profile = UserProfile.objects.filter(is_verified_by_admin=True,is_active=1)
    
    for profile in user_profile:
        userFirebaseToken = profile.firebase_token

        message_title = "My Resource"
        message_body =  "Start your day in a healthy way with meditation and mindfulness at Game On, click here and get started"
        notification_image = ""

        if userFirebaseToken is not None and userFirebaseToken != "" :
            registration_ids = []
            registration_ids.append(userFirebaseToken)
            data_message = {}
            data_message['id'] = 1
            data_message['status'] = 'notification'
            data_message['click_action'] = 'my_resources'

            data_message['image'] = notification_image

            send_android_notification(message_title,message_body,data_message,registration_ids)
            
            heading="My Resource"

            notification_msg="Start your day in a healthy way with meditation and mindfulness at Game On, click here and get started"

            save_notification(profile.id,profile.id,heading,notification_msg,'my_resources')

    context = {}
    context['message']= 'Success' 
    context['response_code']            = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)


# Executed every day at 9:30 AM for customers
@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def home_page_cronjob(request):
    user_profile = UserProfile.objects.filter(is_verified_by_admin=True,is_active=1,role__id=1)
    
    for profile in user_profile:
        userFirebaseToken = profile.firebase_token

        message_title = "KPIs and Wellbeing"
        message_body =  "Are you ready to take your KPIs and well-being to a new level? Click here and get started for the day"
        notification_image = ""

        if userFirebaseToken is not None and userFirebaseToken != "" :
            registration_ids = []
            registration_ids.append(userFirebaseToken)
            data_message = {}
            data_message['id'] = 1
            data_message['status'] = 'notification'
            data_message['click_action'] = 'home_page'

            data_message['image'] = notification_image

            send_android_notification(message_title,message_body,data_message,registration_ids)
            
            heading="KPIs and Wellbeing"

            notification_msg="Are you ready to take your KPIs and wellbeing to a new level? Click here and get started for the day"

            save_notification(profile.id,profile.id,heading,notification_msg,'home_page')


    context = {}
    context['message']= 'Success' 
    context['response_code']            = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)

# Executed every day at 10 AM for customers and managers
@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def josh_page_cronjob(request):
    user_profile = UserProfile.objects.filter(is_verified_by_admin=True,is_active=1)
    
    for profile in user_profile:
        userFirebaseToken = profile.firebase_token

        message_title = "Your Josh"
        message_body =  "How's the Josh Today, click here and tell us"
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

            notification_msg="How's the Josh Today, click here and tell us"

            save_notification(profile.id,profile.id,heading,notification_msg,'my_josh')


    context = {}
    context['message']= 'Success' 
    context['response_code']            = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)


# Executed every day at 11 AM for customers
@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def my_leaderboard_cronjob(request):
    user_profile = UserProfile.objects.filter(is_verified_by_admin=True,is_active=1,role__id=1)
    
    for profile in user_profile:
        userFirebaseToken = profile.firebase_token

        message_title = "My Leaderboard"
        message_body =  "There is sound of coins and notification 'Do you hear that, that is the sound of virtual points waiting for you'"
        notification_image = ""

        if userFirebaseToken is not None and userFirebaseToken != "" :
            registration_ids = []
            registration_ids.append(userFirebaseToken)
            data_message = {}
            data_message['id'] = 1
            data_message['status'] = 'notification'
            data_message['click_action'] = 'my_leaderboard'

            data_message['image'] = notification_image

            send_android_notification(message_title,message_body,data_message,registration_ids)
            
            heading="My Leaderboard"

            notification_msg="There is sound of coins and notification 'Do you hear that, that is the sound of virtual points waiting for you'"

            save_notification(profile.id,profile.id,heading,notification_msg,'my_leaderboard')


    context = {}
    context['message']= 'Success' 
    context['response_code']            = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)



# Executed every day at 12 PM for customers and Managers

@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def my_wellbeing_cronjob(request):
    user_profile = UserProfile.objects.filter(is_verified_by_admin=True,is_active=1)
    
    for profile in user_profile:
        userFirebaseToken = profile.firebase_token

        message_title = "My Wellbeing"
        message_body =  "How many heart points and steps did you look at today? Is it going to be 150 heart points this week and 10000 steps today? You can do it!"
        notification_image = ""

        if userFirebaseToken is not None and userFirebaseToken != "" :
            registration_ids = []
            registration_ids.append(userFirebaseToken)
            data_message = {}
            data_message['id'] = 1
            data_message['status'] = 'notification'
            data_message['click_action'] = 'my_wellbeing'

            data_message['image'] = notification_image

            send_android_notification(message_title,message_body,data_message,registration_ids)
            
            heading="My Wellbeing"

            notification_msg="How many learning hours and steps did you clock today? Is it going to be 8 hours this week and 10000 steps today ? You can do it !"

            save_notification(profile.id,profile.id,heading,notification_msg,'my_wellbeing')


    context = {}
    context['message']= 'Success' 
    context['response_code']            = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)



# Executed every day at 2:30 PM for customers and Managers

@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def game_for_today_cronjob(request):
    user_profile = UserProfile.objects.filter(is_verified_by_admin=True,is_active=1)
    
    for profile in user_profile:
        userFirebaseToken = profile.firebase_token

        message_title = "Game"
        message_body =  "Is it another stressful day or another day of fun, lighten it up with a quick fun game at Game On, come and play now"
        notification_image = ""

        if userFirebaseToken is not None and userFirebaseToken != "" :
            registration_ids = []
            registration_ids.append(userFirebaseToken)
            data_message = {}
            data_message['id'] = 1
            data_message['status'] = 'notification'
            data_message['click_action'] = 'game_for_today'

            data_message['image'] = notification_image

            send_android_notification(message_title,message_body,data_message,registration_ids)
            
            heading="Game"

            notification_msg="Is it another stressful day or another day of fun, lighten it up with a quick fun game at Game On, come and play now"

            save_notification(profile.id,profile.id,heading,notification_msg,'game_for_today')


    context = {}
    context['message']= 'Success' 
    context['response_code']            = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)



# Executed once in a week...at a time every monday

@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def challenges_won_cronjob(request):
  
    end_date = datetime.now().date() - timedelta(days=1)

    start_date = end_date-timedelta(days=6)

    user_profile = UserProfile.objects.filter(is_verified_by_admin=True,is_active=1,role__id=1)
    
    for profile in user_profile:
        challenges_played_count = ChallengePoint.objects.filter(user_profile__id=profile.id,created_at__date__range=[start_date,end_date]).count()
        challenges_win_points = ChallengePoint.objects.filter(user_profile__id=profile.id,is_won=True,created_at__date__range=[start_date,end_date]).aggregate(Sum('bonus_point'))
        
        bonus_point = challenges_win_points['bonus_point__sum']

        if not bonus_point:
            bonus_point = 0
        
        userFirebaseToken = profile.firebase_token

        message_title = "Last Week Challenges"
        message_body =  f"Last week, you played {challenges_played_count} challenges and won {bonus_point} points, you are awesome. Play more challenges this week and win more."
        notification_image = ""

        if userFirebaseToken is not None and userFirebaseToken != "" :
            registration_ids = []
            registration_ids.append(userFirebaseToken)
            data_message = {}
            data_message['id'] = 1
            data_message['status'] = 'notification'
            data_message['click_action'] = 'my_challenges'

            data_message['image'] = notification_image

            send_android_notification(message_title,message_body,data_message,registration_ids)
            
            heading="Last Week Challenges"

            notification_msg=f"Last week, you played {challenges_played_count} challenges and won {bonus_point} points, you are awesome. Play more challenges this week and win more."

            save_notification(profile.id,profile.id,heading,notification_msg,'my_challenges')


    context = {}
    context['message']= 'Success' 
    context['response_code']            = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)



# Executed once in a week...at a time every monday

@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def points_reminder_cronjob(request):
    end_date = datetime.now().date() - timedelta(days=1)
    start_date = end_date-timedelta(days=6)
    user_profile = UserProfile.objects.filter(is_verified_by_admin=True,is_active=1,role__id=1)
    
    for profile in user_profile:
        total_win_point = MyRewardPoint.objects.filter(user_profile__id=profile.id).aggregate(Sum('earned_point'))
        last_week_win_points = MyRewardPoint.objects.filter(user_profile__id=profile.id,created_at__date__range=[start_date,end_date]).aggregate(Sum('earned_point'))
        total_win_point = total_win_point['earned_point__sum']
        
        if not total_win_point:
            total_win_point  = 0

        last_week_bonus_points = last_week_win_points['earned_point__sum']
        if not last_week_bonus_points:
            last_week_bonus_points = 0
        
        userFirebaseToken = profile.firebase_token
        message_title = "Points Reminder"
        message_body =  f"You have {total_win_point} points and last week you added {last_week_bonus_points} points, what this week going be to like. Join in and explore more to earn bonus points."
        notification_image = ""

        if userFirebaseToken is not None and userFirebaseToken != "" :
            registration_ids = []
            registration_ids.append(userFirebaseToken)
            data_message = {}
            data_message['id'] = 1
            data_message['status'] = 'notification'
            data_message['click_action'] = 'my_leaderboard'

            data_message['image'] = notification_image
            send_android_notification(message_title,message_body,data_message,registration_ids)
            heading="Points Reminder"

            notification_msg=f"You have {total_win_point} points and last week you added {last_week_bonus_points} points, what this week going be to like. Join in and explore more to earn bonus points."
            save_notification(profile.id,profile.id,heading,notification_msg,'my_leaderboard')


    context = {}
    context['message']= 'Success' 
    context['response_code']            = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)




# Executed every day at 12:30 PM (if there is challenge) for customers


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def manager_broadcast_challenge_cronjob(request):
    manager_team_ids = UserProfile.objects.filter(is_verified_by_admin=True,is_active=1,role__id=2).values_list('id',flat=True)

    team_challenges = TeamChallenge.objects.filter(manager__id__in=manager_team_ids,is_broadcasted=1)

    current_date = datetime.now().date()

    if team_challenges:
        for challenge in team_challenges:
            
            team_members = UserProfile.objects.filter(team_id=challenge.manager.team_id,is_active=1)

            employee_users = []

            for member in team_members:
                team_challenge = TeamAcceptChallengeHistory.objects.filter(customer_accepted_id=member.id,team_challenge__id=challenge.id,is_accepted=1,team_challenge__updated_at=current_date).first()
                if team_challenge:
                    pass
                else:
                    employee_users.append(member.id)
 
                    manager_name = challenge.manager.user.first_name +" "+ challenge.manager.user.last_name
            
                    userFirebaseToken = member.firebase_token

                    message_title = "New Challenge"
                    message_body =  f"Hey, did you look at the latest business challenge set up by {manager_name} ? We know you can do it ? Have you accepted the challenge yet ?"
                    notification_image = ""

                    if userFirebaseToken is not None and userFirebaseToken != "" :
                        registration_ids = []
                        registration_ids.append(userFirebaseToken)
                        data_message = {}
                        data_message['id'] = 1
                        data_message['status'] = 'notification'
                        data_message['click_action'] = 'my_challenge'

                        data_message['image'] = notification_image

                        send_android_notification(message_title,message_body,data_message,registration_ids)
                        
                        heading="New Challenge"

                        notification_msg=f"Hey, did you look at the latest business challenge set up by {manager_name} ? We know you can do it ? Have you accepted the challenge yet ?"

                        save_notification(member.id,member.id,heading,notification_msg,'my_challenges')


    context = {}
    context['message']= 'Success' 
    context['response_code']            = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)



# Executed every second for customers


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def challenge_timer_before_sixty_minute_cronjob(request):
    current_date=datetime.now().date()
    current_time=datetime.now().strftime('%H:%M:%S')

    user_profile_ids = UserProfile.objects.filter(is_verified_by_admin=True,is_active=1,role__id=1).values_list('id',flat=True)

    team_challenges = TeamAcceptChallengeHistory.objects.filter(customer_accepted_id__in=user_profile_ids,team_challenge__updated_at__date=current_date,team_challenge__is_broadcasted=1,is_accepted=1,team_challenge__is_completed_by_manager=0)
    
    if team_challenges:
        for challenge in team_challenges:
               
            if challenge.team_challenge.start_time<=current_time and challenge.team_challenge.end_time>=current_time and current_date==challenge.team_challenge.updated_at.date():
                
                sixty_minute_before_date_time=datetime.strptime(challenge.team_challenge.end_time,"%H:%M:%S")-timedelta(minutes=60)
                
                sixty_minute_before_time = sixty_minute_before_date_time.strftime("%H:%M:%S")

                if current_time==sixty_minute_before_time:
                    
                
                    profile = UserProfile.objects.filter(id=challenge.customer_accepted_id,is_active=1).first()        

                    manager_name = challenge.team_challenge.manager.user.first_name +" "+ challenge.team_challenge.manager.user.last_name
                    
                    userFirebaseToken = profile.firebase_token

                    if userFirebaseToken:
                            
                        message_title = "My Challenge"
                        message_body =  "Hurry up, you have 60 mins to go to complete the business challenge today, go for gold !"
                        notification_image = ""

                        if userFirebaseToken is not None and userFirebaseToken != "" :
                            registration_ids = []
                            registration_ids.append(userFirebaseToken)
                            data_message = {}
                            data_message['id'] = 1
                            data_message['status'] = 'notification'
                            data_message['click_action'] = 'my_challenge'

                            data_message['image'] = notification_image

                            send_android_notification(message_title,message_body,data_message,registration_ids)
                            
                            heading="My Challenge"

                            notification_msg="Hurry up, you have 60 mins to go to complete the business challenge today, go for gold !"

                            save_notification(profile.id,profile.id,heading,notification_msg,'my_challenge')


    context = {}
    context['message']= 'Success' 
    context['response_code']            = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)



# Executed once in a week...at a time every monday // wellbeing (fitness time spent videos ), Customers and Managers

@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def fitness_time_spent_cronjob(request):
  
    end_date = datetime.now().date() - timedelta(days=1)
    start_date = end_date-timedelta(days=6)
    user_profile = UserProfile.objects.filter(is_verified_by_admin=True,is_active=1)
    
    for profile in user_profile:
        watch_video_played_count = watchTimeData.objects.filter(user_profile__id=profile.id,created_at__date__range=[start_date,end_date]).count()
        watch_video_win_points = watchTimeData.objects.filter(user_profile__id=profile.id,created_at__date__range=[start_date,end_date]).aggregate(Sum('bonus_point'))
        
        bonus_point = watch_video_win_points['bonus_point__sum']

        if not bonus_point:
            bonus_point = 0
        
        userFirebaseToken = profile.firebase_token

        message_title = "Fitness Time Spent"
        message_body =  f"Last week, you played {watch_video_played_count} minutes on wellbeing and won {bonus_point} points, you are awesome. View more fitness videos this week and win more."
        notification_image = ""

        if userFirebaseToken is not None and userFirebaseToken != "" :
            registration_ids = []
            registration_ids.append(userFirebaseToken)
            data_message = {}
            data_message['id'] = 1
            data_message['status'] = 'notification'
            data_message['click_action'] = 'my_wellbeing'

            data_message['image'] = notification_image

            send_android_notification(message_title,message_body,data_message,registration_ids)
            
            heading="Fitness Time Spent"

            notification_msg=f"Last week, you played {watch_video_played_count} minutes on wellbeing and won {bonus_point} points, you are awesome. View more fitness videos this week and win more."

            save_notification(profile.id,profile.id,heading,notification_msg,'my_wellbeing')


    context = {}
    context['message']= 'Success' 
    context['response_code']            = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)



# Executed every second // Customers and Managers

@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def available_game_time_cronjob(request):
  
    user_profile = UserProfile.objects.filter(is_verified_by_admin=True,is_active=1)
    
    for profile in user_profile:
        game_data = GameName.objects.filter(status=1)

        for game in game_data:  
            customer_game = CustomerPlayedGame.objects.filter(user_profile__id=profile.id,game_name__id=game.id,is_end=1).last()
            
            if customer_game: 

                current_date_time=datetime.now()
                
                current_datetime = current_date_time.strftime("%Y-%m-%d %I:%M:%S")
                
                next_avaialable_date_time = customer_game.next_availability_time     
                
                availability = next_avaialable_date_time + timedelta(seconds=1)

                availability = availability.strftime("%Y-%m-%d %I:%M:%S")

        
                if current_datetime==availability:

                    customer_game.is_end = 0
                    customer_game.save()
                    
                    userFirebaseToken = profile.firebase_token

                    message_title = "Play Your Game"
                    message_body =  "The much awaited time has come, the Game of the Day is now available for you to Play and say Goodbye to Stress. Play now ! "
                    
                    notification_image = ""
                    
                    if userFirebaseToken is not None and userFirebaseToken != "" :
                        registration_ids = []
                        registration_ids.append(userFirebaseToken)
                        data_message = {}
                        data_message['id'] = 1
                        data_message['status'] = 'notification'
                        data_message['click_action'] = 'game_for_today'

                        data_message['image'] = notification_image

                        send_android_notification(message_title,message_body,data_message,registration_ids)
                        
                        heading="Play Your Game"

                        notification_msg="The much awaited time has come, the Game of the Day is now available for you to Play and say Goodbye to Stress. Play now ! "
                        
                        save_notification(profile.id,profile.id,heading,notification_msg,'game_for_today')

    context = {}
    context['message']= 'Success' 
    context['response_code']            = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)


# Executed every second # for customers only

@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def challenge_completion_cronjob(request):
  
  
    current_date=datetime.now().date()

    team_challenges = TeamAcceptChallengeHistory.objects.filter(team_challenge__is_broadcasted=1,team_challenge__updated_at__date=current_date,team_challenge__is_completed_by_manager=1)
    
  
    if team_challenges:
         
        for challenge in team_challenges:
            user_profile = UserProfile.objects.filter(id=challenge.customer_accepted_id).first()
            
        
            employee_performance = OrganizationEmployeePerformanceData.objects.filter(permormance_date__icontains=current_date,organization_employee_data__email=user_profile.user.email,is_paid=0).first()
            

        
            if employee_performance:
                  
                
                if round(employee_performance.kpi_target,2)<=round(employee_performance.kpi_actual,2):
                    
                    points = RewardPointsStimulator.objects.filter(status=6).first()
                    
                    challenge_point = ChallengePoint.objects.create(
                        user_profile=user_profile,
                        challenge=challenge.team_challenge,
                        is_won=True,
                        bonus_point=int(points.multiplier)
                    )

                    print("executed")

                    if MyRewardPoint.objects.filter(user_profile__id=user_profile.id).exists():
                        my_reward = MyRewardPoint.objects.filter(user_profile__id=user_profile.id).last()
                        point_balance = my_reward.point_balance + int(points.multiplier)
                        my_reward = MyRewardPoint.objects.create(
                            manager_id=challenge.team_challenge.manager.id,              
                            user_profile=user_profile,
                            earned_point= int(points.multiplier),
                            point_balance=point_balance
                        )
                    else:
                        my_reward = MyRewardPoint.objects.create(
                            manager_id=challenge.team_challenge.manager.id,              
                            user_profile=user_profile,
                            earned_point=int(points.multiplier),
                            point_balance=int(points.multiplier)
                        )
                    employee_performance.is_paid = 1
                    employee_performance.save()
                else:
                    challenge_point = ChallengePoint.objects.create(
                        user_profile=user_profile,
                        challenge=challenge.team_challenge,
                        is_won=False,
                        bonus_point=0
                    )
            
    context = {}
    context['message']= 'Success' 
    context['response_code']            = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)



# Executed every second // challenge streak (5 times in a row) bonus points // for customers only

@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def challenge_completion_streak_bonus_point_cronjob(request):
  
    user_profile = UserProfile.objects.filter(is_verified_by_admin=True,is_active=1,role__id=1)
    
    current_date=datetime.now().date()

    team_challenges = TeamAcceptChallengeHistory.objects.filter(team_challenge__is_broadcasted=1,team_challenge__updated_at__date=current_date,team_challenge__is_completed_by_manager=1)
 
    
    print("team chellenge==>",team_challenges)

    # for profile in user_profile:
    #     pass  
      

    context = {}
    context['message']= 'Success' 
    context['response_code']            = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)





# Executed every second // top 10 bonus // for customers and managers both

@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def top_ten_bonus_point_cronjob(request):
    
    user_profile = UserProfile.objects.filter(is_verified_by_admin=True,is_active=1,role__id=1)
    
    current_date=datetime.now().date()

    team_challenges = TeamAcceptChallengeHistory.objects.filter(team_challenge__is_broadcasted=1,team_challenge__updated_at__date=current_date,team_challenge__is_completed_by_manager=1)
 
    
    print("team chellenge==>",team_challenges)

    # for profile in user_profile:
    #     pass  
      

    context = {}
    context['message']= 'Success' 
    context['response_code']            = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)



# Executed every second // coaching streak bonus // for customers and managers both

@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def coaching_strack_bonus_point_cronjob(request):
    
    user_profile = UserProfile.objects.filter(is_verified_by_admin=True,is_active=1,role__id=1)
    
    current_date=datetime.now().date()

    team_challenges = TeamAcceptChallengeHistory.objects.filter(team_challenge__is_broadcasted=1,team_challenge__updated_at__date=current_date,team_challenge__is_completed_by_manager=1)
 
    
    print("team chellenge==>",team_challenges)

    # for profile in user_profile:
    #     pass  
      

    context = {}
    context['message']= 'Success' 
    context['response_code']            = HTTP_200_OK
    return Response(context, status=HTTP_200_OK)



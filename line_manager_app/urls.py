from django.urls import path,include
from .views import *

urlpatterns = [
    path('create-challenge/',create_challenge),
    path('create-campaign/',create_campaign),
    path('challenge-purpose-list/',challenge_purpose_list),
    path('campaign-purpose-list/',campaign_purpose_list),
    path('review-challenge/',review_challenge),
    path('review-campaign/',review_campaign),
    path('broadcast-challenge/',broadcast_challenge),
    path('broadcast-campaign/',broadcast_campaign),

    # Manager_concern_category
    path('manager-concern-category/',manager_concern_category),
   
    # Manager_raise_concern_update
    path('manager_raise_concern_update/',manager_raise_concern_update),
   
    # Manager_raise_concern_list
    path('manager_raise_concern_list/',manager_raise_concern_list),

    # Manager Josh For Today
    path('manager_josh_reason_today/',manager_josh_reason_today),

    # Manager Josh List Time
    path('manager_josh_reason_type/',manager_josh_reason_type),

    # Manager Johs Create 
    path('manager-josh-reason-create/',manager_josh_create),

    # manager josh Data List
    
    path('manager_josh_reason_list/',manager_josh_reason_list),

    # end Challenge
    path('end-challenge/',end_challenge_by_manager),
    
    # end campaign
    path('end-campaign/',end_campaign_by_manager),

    # Today's Challenge Count
    path('todays-challenge-count/',todays_challenge_count),

    # Team Profile Data
    path('team-profile-list/',team_profile),

    path('team-lists/',team_lists),

    path('team-employee-lists/',team_employee_lists),  # Used inside Team leaderboard for Manager app

    path('team-leaderboard/',team_leaderboard),
    
    path('team-leaderboard-filter/',team_leaderboard_filter),

    path('team-Campaign-kpi-data/',team_Campaign_kpi),

   
    path('team-mood-today/',team_mood_for_today),

    path('team-mood-today-filter/',team_mood_for_today_filter),

    # Industry Type List Data
    path('industry-list-data/',industry_list_data),

    #Kpi Name List Data based on industry work type
    path('kpiname-list-data/',kpiname_list_data),

    path('manager-kpi-met-and-wip/',manager_kpi_met_and_wip),

    # used for listing kpi data based on organization unique code
    path('kpi-lists/',kpi_lists),

    path('team-performance-lists/',team_performance_lists),

    path('team-wellbeing-lists/',team_wellbeing_lists)


]



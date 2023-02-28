from django.urls import path,include
from .views import *


urlpatterns = [

#   Customer  Concern Category List
    path('concern-category-list/',customer_concat_list),
    path('customer-concern-data-list/',customer_raise_concern),
    path('customer-concern-data-update/',customer_raise_concern_update),

# Challange Section
    path('challenge-lists/',challenge_lists),
    path('campaign-lists/',campaign_lists),

# Customer_reason_type 
    path('customer-josh-reason-type/',customer_josh_reason_type),
# Josh Reason Create
    path('customer-josh-reason-create/',customer_josh_create),
# Josh Data Show
    path('customer-josh-reason-list/',customer_josh_reason_list),
# Today's Josh Data
    path('customer-josh-reason-today/',customer_josh_reason_today),
# Today's Team Josh
    path('team-josh-reason-today/',team_josh_reason_today),
    path('accept-challenge/',accept_challenge_by_customer),
    path('accept-campaign/',accept_campaign_by_customer),
  
    path('notification-lists/',notification_lists),
    path('delete-notifications/',delete_notifications),
    path('mark-read-notifications/',mark_read_notifications),
    path('mark-unread-notifications/',mark_unread_notifications),
#my_reward_point_list7
   path('my-reward-point-list/',my_reward_point_list),
   

# watch_time_data 
  path('watch-time-data/',watch_time_data),

# watch_time_data 
  path('read-skill-and-hobby-time-data/',read_skill_and_hobby_time_data),

# watch_time_data 
  path('learning-material-time-data/',learning_material_time_data),

# customer_played_game_time
  path('customer-played-game-time/',customer_played_game_time),

# customer_played_game_time
  path('customer-played-game-list/',customer_played_game_list),

# challenge_point_data
  path('challenge-point-data/',challenge_point_data),

# campaign_point_data
  path('campaign-point-data/',campaign_point_data),


  path('win-level-points/',win_level_and_points_won),

  path('kpi-met-and-wip/',kpi_met_and_wip),


  path('habbit-of-the-day-message/',habbit_of_the_day_message),

  path('save-steps-taken/',save_steps_taken),

  path('wellbeing-lists/',wellbeing_lists),

  path('kpi-performance-lists/',kpi_performance_lists),

  path('game-point-list/',game_point_list),

  path('user-motivational-message-list/',user_motivational_message_list),


  path('filter-employee-bar-chart-pie-chart/',filter_employee_bar_chart_and_pie_chart),
  

]



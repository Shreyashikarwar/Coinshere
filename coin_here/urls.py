"""coin_here URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static



from rest_framework.authtoken.views import obtain_auth_token

from cronjob import crons

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dragonadmin/',include('admin_user.urls')),
    path('accounts/',include('accounts.urls')),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('customers/',include('customer_service_app.urls')),
    path('managers/',include('line_manager_app.urls')),
    
    # path('challenge-points-distribute-cronjob/',crons.challenge_cronjob_points_distribution),
    
    # path('campaign-points-distribute-cronjob/',crons.campaign_cronjob_points_distribution),
    
    path('end-challenge-cronjob/',crons.end_challenge_cronjob),
    
    path('end-campaign-cronjob/',crons.end_challenge_cronjob),
    
    # new cron job

    path('challenge-completion-cronjob/',crons.challenge_completion_cronjob), 

    # path('challenge-completion-streak-bonus-point-cronjob/',crons.challenge_completion_streak_bonus_point_cronjob), 

    # path('game-streak-bonus-point-cronjob/',crons.game_streak_bonus_point_cronjob), 

    # path('top-ten-bonus-point-cronjob/',crons.top_ten_bonus_point_cronjob), 

    # path('coaching-streak-bonus-point-cronjob/',crons.coaching_strack_bonus_point_cronjob), 


    # notification urls

    path('my-resource-cronjob/',crons.my_resource_cronjob), 

    path('home-page-cronjob/',crons.home_page_cronjob),

    path('josh-page-cronjob/',crons.josh_page_cronjob),

    path('my-leaderboard-cronjob/',crons.my_leaderboard_cronjob),

    path('my-wellbeing-cronjob/',crons.my_wellbeing_cronjob),

    path('challenges-won-cronjob/',crons.challenges_won_cronjob),

    path('points-reminder-cronjob/',crons.points_reminder_cronjob),


    path('game-for-today-cronjob/',crons.game_for_today_cronjob),

    path('manager-broadcast-challenge-cronjob/',crons.manager_broadcast_challenge_cronjob),

    path('challenge-timer-before-sixty-minute-cronjob/',crons.challenge_timer_before_sixty_minute_cronjob),

    path("fitness-time-spent-cronjob/",crons.fitness_time_spent_cronjob),

    path("available-game-time-cronjob/",crons.available_game_time_cronjob),


# obtaintoken get 
    
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Game On"
admin.site.site_title = "Game On Admin Portal"
admin.site.index_title = "Welcome to Game On Portal"





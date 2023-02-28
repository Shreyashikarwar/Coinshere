""" URL Configuration for core auth
"""
from django.urls import path, include
from .views import *
from admin_user import admin_web_apis
from .admin_web_apis import *

from rest_framework.authtoken.views import obtain_auth_token
# from admin_user.auth import CustomAuthToken


urlpatterns = [
  
    # Terms & Conditions
  
  
    # Companysite_data GET
    path('companysite-list-data/',companysite_list, name="company_site"),
    
    path('terms/',admin_web_apis.term,name="terms"),

    # skill_and_hobby_list
    path('skill-and-hobby-list/',skill_and_hobby_list, name="company_site"),


    # Leadership_data GET
    path('leadership-list-data/',leadership_list, name="leadership"),
    #Learning Material GET
    path('learningmaterial-list-data/',learningmaterial_list,name="learningmaterial_list"),
    #Other Link GET
    path('otherlink-list-data/',otherlink_list,name="otherlink_list"),
    # Game name data
    path('game-name-list/',game_name_list,name="game-name"),
    # Auth Section Url Path Token
    # Update Gane Data
    path('game_name_list_update/<int:pk>/',game_name_list_update),
    path('avatar-image-lists/',avatar_image_lists),


    # Web API's Section--->Admin User URL's -------------------------------------------
    path('admin-login/',admin_login),
    path('admin-logout/',admin_logout),

    # organization_employee_data_list
    path('organization-employee-data-list/',organization_employee_data_list),
    
    #employee_data_list_baselocation
    path('employee-data-list-baselocation/',employee_data_list_baselocation),

    # organization_city_data
    path('employee-city-list/',employee_city_list),

    # Team_list_data
    path('team-list-data/',team_list_data),


    #Admin Sign up 
    # path('admin-signup/',admin_signup), 

    # Organization Employee Add User

    path('organization-employee/',organization_employee),

    # Manage Concern list Section            ****
    path('manage-concern-list/',manage_concern_list), 
    # user profile list Section
    path('user-profile-list/',user_profile_list)    
]
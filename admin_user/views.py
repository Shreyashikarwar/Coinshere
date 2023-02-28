
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated

from django.contrib.auth.models import User

from rest_framework.response import Response
from datetime import datetime,date

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
from .models import  CompanySite,LeaderShipTask,LearningMaterial,OtherLink,GameName,SkillAndHobby,AvatarImage
from .serializers import CompanySiteSerializers,LeaderShipTaskSerializers,LearningMaterialSerializers,OtherLinkSerializers,GameNameSerializers

from django.contrib.auth import logout
from decorators.decorators import *
from django.conf import settings
# Create Your Views Here 



# Customer Site Portal 
@api_view(['GET'])
@authenticate_token
def companysite_list(request):
    company_site_data = CompanySite.objects.filter(status=1)
    if company_site_data:
        company_site = CompanySite.objects.values().filter(status=1).first()
        company_site['image_data'] = settings.BASE_URL+"media/"+company_site['image_data']
        msg=(f"Data Succefully Get ")
        context = {}
        context['response_code'] = 200
        context['message'] = msg
        context['company_site_data'] = company_site
    return Response(context, status=HTTP_200_OK)




# Skill And Hobby 
@api_view(['GET'])
@authenticate_token
def skill_and_hobby_list(request):
    skill_and_hobby_data = SkillAndHobby.objects.filter(status=1)
    if skill_and_hobby_data:
        skill_and_hobby_data = SkillAndHobby.objects.values().filter(status=1)
        for skill_and_hobby in skill_and_hobby_data:
            skill_and_hobby['image_data'] = settings.BASE_URL+"media/"+skill_and_hobby['image_data']
        msg=(f"Data Succefully Get ")
        context = {}
        context['response_code'] = 200
        context['message'] = msg
        context['skill_and_hobby_data'] = skill_and_hobby_data
    return Response(context, status=HTTP_200_OK)




# Leader Ship Task 
@api_view(['GET'])
@authenticate_token
def leadership_list(request):
    try:
        Leader_ship_data=LeaderShipTask.objects.filter(status=1)
    except:
        return Response({'Msg':'Data Not Found'})
    serializer=LeaderShipTaskSerializers(Leader_ship_data,many=True)
    return Response(data={'leadership_list_Data':serializer.data,'response_code':200},status=status.HTTP_200_OK)


# Learning Material site 
@api_view(['GET'])
@authenticate_token
def learningmaterial_list(request):

    Learning_material_data = LearningMaterial.objects.filter(status=1)
    if Learning_material_data:
        learning_material = LearningMaterial.objects.values().filter(status=1)
        for learn in learning_material:
            learn['image_data'] = settings.BASE_URL+"media/"+learn['image_data']
        msg=(f"Data Succefully Get ")
        context = {}
        context['response_code'] = 200
        context['message'] = msg
        context['learning_material'] = learning_material
    return Response(context, status=HTTP_200_OK)



# Other Link Data 
@api_view(['GET'])
@authenticate_token
def otherlink_list(request):

    other_link_data = OtherLink.objects.filter(status=1)
    if other_link_data:
        other_link = OtherLink.objects.values().filter(status=1)
        for other in other_link:
            other['image_data'] = settings.BASE_URL+"media/"+other['image_data']
        msg=(f"Data Succefully Get ")
        context = {}
        context['response_code'] = 200
        context['message'] = msg
        context['other_link_data'] = other_link
    return Response(context, status=HTTP_200_OK)



# Other Link Data 
@api_view(['GET'])
# @authenticate_token
def avatar_image_lists(request):
    avatar_images = AvatarImage.objects.filter(status=1).values()

    for data in avatar_images:
        data['image'] = settings.BASE_URL +"media/"+data['image']
    
    # print(data)

    context = {}
    context['avatar_images'] = avatar_images
    context['response_code'] = 200
    return Response(context, status=HTTP_200_OK)




# Game Name 
@csrf_exempt
@api_view(["GET"])
@authenticate_token
def game_name_list(request):
    unique_code=request.query_params.get('unique_code')
    print(unique_code)
    unique_code_model = GameName.objects.filter(organization__unique_code=unique_code)
    if unique_code_model:
        game_name_data = GameName.objects.values().filter(organization__unique_code=unique_code)
        for game in game_name_data:
            game['logo'] = settings.BASE_URL+"media/"+game['logo']
        msg=(f"Data Succefully get for unique_code {unique_code} ")
        context = {}
        context['response_code'] = 200
        context['message'] = msg
        context['game_name_data'] = game_name_data
    else:
        context = {}
        msg=(f"Data is not available for unique_code {unique_code} ")
        context['response_code'] = 201
        context['game_name_data'] = []
        context['message'] = msg
    return Response(context, status=HTTP_200_OK)


# Update Game Time 
@csrf_exempt
@api_view(["PATCH"])
@authenticate_token
def game_name_list_update(request,pk):
        try:
            game_serializer = GameNameSerializers(GameName.objects.get(pk=pk))
        except : 
            return Response(data={'msg':'Failed Data Not Found ','status':'false','response_code':201}, status=status.HTTP_201_CREATED)        

        game_id = GameName.objects.get(pk=pk)
        game_serializer = GameNameSerializers(game_id,data = request.data, partial=True)                 
        if game_serializer.is_valid():
            game_serializer.save()
            return Response(data= {'msg':'Data saved Successfully','status':True,'response_code':200}, status=status.HTTP_200_OK)
        else:
            return Response(data= {'msg':"Data not Updated"}, status=status.HTTP_201_CREATED)







# AUthentication  Section                             Login 


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def admin_login(request):
    email = request.data.get('email')
    password = request.data.get('password') 
    if email is None or email == '':
        return Response({'message': 'Email field is required', 'response_code': 201}, status=HTTP_201_CREATED)
    if password is None or password == '':
        return Response({'message': 'Password field is required', 'response_code':201}, status=HTTP_201_CREATED)
    user = User.objects.filter(email=email,is_superuser=True).first()
    if not user:
        return Response({'message': "Your email is not correct", 'response_code': 201}, status=HTTP_201_CREATED)
    check = user.check_password(password)
    if not check:
        return Response({'message': "You password is not correct", 'response_code': 201}, status=HTTP_201_CREATED)
    if user and check:
        user = user
        token,_=Token.objects.get_or_create(user=user)
        context = {}
        context['token']   =    token.key
        context['user_id'] =    user.id
        context['username'] =   user.username
        context['first_name'] = user.first_name
        context['last_name'] = user.last_name 
        return Response(context, status=HTTP_200_OK)


#  Logout Section 

# @csrf_exempt
# @api_view(["POST"])
# def admin_logout(request):
#     if request.data.get('user_id') == '' or request.data.get('user_id') is None:  
#         return Response({'message': 'Please provide a user_id', 'response_code': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST) 
    
#     user_id = request.data.get('user_id')
#     user_instance = Token.objects.filter(user__id=user_id)
#     context = {}

#     if user_instance:
#         user_instance.delete()
#         context['message']       = (f"User Logged Out successfully for user id {user_id}.")
#         context['response']      = 200
#         return Response(context,status.HTTP_200_OK)
#     else:
#         context['message']       = (f" {user_id} is Invalid  User Id.")
#         context['response']      = 201
#         return Response(context,status.HTTP_200_OK)




    
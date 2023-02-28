from lib2to3.pytree import Base
from django.db import models
from accounts.models import * 
from line_manager_app.models import *

from admin_user.models import *

# Create your models here.


# Josh for Customer

class ReasonType(BaseModel):
    reason_name=models.CharField(max_length=50)
    status=models.IntegerField(default=1)

    def __str__(self):
        return self.reason_name +" "+str(self.id)


class JoshReason(BaseModel):
    user_profile=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    reason_type=models.ForeignKey(ReasonType,on_delete=models.CASCADE,null=True,blank=True)
    manager_id =models.IntegerField(blank=True,null=True)   # team id
    description=models.CharField(max_length=200,blank=True,null=True)
    emoji_point=models.IntegerField(null=True,blank=True)  # 1,2,3,4,5

    def __str__(self):
        return str(self.user_profile.user.first_name)+" "+str(self.user_profile.user.last_name)+"|" +str(self.created_at)


# Game Points

class GamePoint(BaseModel):
   
    user_profile=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    game_type_id= models.IntegerField(null=True,blank=True)
    is_won=models.BooleanField(default=False,null=True,blank=True)
    bonus_point=models.IntegerField(default=0)

#     def __str__(self):
#         return str(self.user_profile.first_name)+str(self.no_of_point)

# Notification to customer

class Notification(BaseModel):
    from_user_id=models.IntegerField(null=True,blank=True)
    to_user_id=models.IntegerField(null=True,blank=True) 
    heading=models.CharField(max_length=100)
    activity=models.CharField(max_length=200)
    is_read=models.BooleanField(default=False)
    redirectional_code = models.CharField(max_length=200,null=True,blank=True)

# Activity log of Customer

class ActivityLog(BaseModel):
    user_profile=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    heading=models.CharField(max_length=100)
    activity=models.CharField(max_length=200)
    module=models.BooleanField(default=False)


class CustomerConcernCategory(BaseModel):
    name=models.CharField(max_length=100)
    status=models.IntegerField(default=0)


    def __str__(self):
        return self.name +  ' | '+ str(self.id)


class CustomerRaiseConcern(BaseModel):
    concern_category=models.ForeignKey(CustomerConcernCategory,on_delete=models.CASCADE)
    description=models.CharField(max_length=100)
    user_profile=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    action_owner_id=models.IntegerField(null=True,blank=True)  # Concern send to Manager
    comment=models.CharField(max_length=100,null=True,blank=True)
    status=models.IntegerField(default=1) # 1 means open/ 0 closed


    def __str__(self):

        return self.concern_category.name


# All Customer Points

class MyRewardPoint(BaseModel):
    manager_id  =models.IntegerField(null=True,blank=True)
    user_profile=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    earned_point=models.IntegerField(default=0)
    point_used=models.IntegerField(default=0)
    point_balance=models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)  + ' |  '+ str(self.user_profile.user.first_name) + " "+str(self.user_profile.user.last_name) 


class ChallengePoint(BaseModel):
    user_profile=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    challenge= models.ForeignKey(TeamChallenge,on_delete=models.CASCADE)
    is_won=models.BooleanField(default=False,null=True,blank=True)
    bonus_point=models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)  + ' |  '+ str(self.is_won) 

  
class CampaignPoint(BaseModel):
    user_profile=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    campaign= models.ForeignKey(TeamCampaign,on_delete=models.CASCADE)
    is_won=models.BooleanField(default=False,null=True,blank=True)
    bonus_point=models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)  + ' |  '+ str(self.is_won) 


  



# Health and fitness watch Data 
class watchTimeData(BaseModel):
    spent_time=models.CharField(max_length=10,null=True)
    user_profile=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    leader_ship_task=models.ForeignKey(LeaderShipTask,on_delete=models.CASCADE,null=True,blank=True)
    spent_time_seconds = models.IntegerField(null=True,blank=True)
    bonus_point=models.IntegerField(default=0,null=True,blank=True)


    def __str__(self):
        return str(self.spent_time) 


# Watch Skill and hobby material
class ReadSkillAndHobbyData(BaseModel):
    spent_time=models.CharField(max_length=10,null=True)
    user_profile=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    skill_and_hobby=models.ForeignKey(SkillAndHobby,on_delete=models.CASCADE,null=True,blank=True)
    spent_time_seconds = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return str(self.spent_time)


# Watch Learning material
class LearningMaterialWatchTimeData(BaseModel):
    spent_time=models.CharField(max_length=10,null=True)
    user_profile=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    learning_material=models.ForeignKey(LearningMaterial,on_delete=models.CASCADE,null=True,blank=True)
    spent_time_seconds = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return str(self.spent_time)


class CustomerPlayedGame(BaseModel):
    user_profile=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    game_name=models.ForeignKey(GameName,on_delete=models.CASCADE)
    is_end=models.IntegerField(default=1,blank=True,null=True)
    next_availability_time=models.DateTimeField(null=True,blank=True)  # next availability time for game
    
    def __str__(self):
        return self.game_name.title   + " | " + self.user_profile.user.first_name +" "+ self.user_profile.user.last_name +" | "+str(self.updated_at)


class TeamAcceptChallengeHistory(BaseModel):
    team_challenge = models.ForeignKey(TeamChallenge,on_delete=models.CASCADE)
    customer_accepted_id=models.IntegerField(null=True,blank=True) # Challenge Accepted by Customer
    is_accepted=models.IntegerField(default=0)


class TeamAcceptCampaignHistory(BaseModel):
    team_campaign = models.ForeignKey(TeamCampaign,on_delete=models.CASCADE)
    customer_accepted_id=models.IntegerField(null=True,blank=True) # Challenge Accepted by Customer
    is_accepted=models.IntegerField(default=0)



class HealthHabbit(BaseModel):
    day = models.IntegerField()
    habbit_of_the_day=models.CharField(max_length=100)
    theme = models.CharField(max_length=20)
    status=models.IntegerField(default=1)


# for calculating Weekly Average
class HealthMetric(BaseModel):
    health_metric = models.CharField(max_length=50,null=True,blank=True)
    target=models.IntegerField()
    weightage=models.FloatField(null=True,blank=True)
    status=models.IntegerField(default=0)
    active=models.IntegerField(default=1)



# for Storing steps count
class StepsTaken(BaseModel):
    user_profile = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    steps_count  = models.IntegerField(null=True,blank=True)



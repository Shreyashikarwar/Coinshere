from pyexpat import model
from telnetlib import STATUS
from unicodedata import name
from django.db import models
from accounts.models import *
from django.utils import timezone



# Team Role Profile Data
class Team(BaseModel):
    organization =models.ForeignKey(Organiztaion,on_delete=models.CASCADE)
    team_name=models.CharField(max_length=100)

    def __str__(self):
        return   self.team_name+ " | related to | " + self.organization.organization_name

class Manager(models.Model):
    team=models.OneToOneField(Team,on_delete=models.CASCADE)
    manager_name=models.CharField(max_length=50)
    email = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.manager_name +  " " +  "owner of " + self.team.team_name +"|"+ str(self.id)




class ManagerReasonType(BaseModel):
    reason_name=models.CharField(max_length=50)
    status=models.IntegerField(default=1)

    def __str__(self):
        return self.reason_name


class ManagerJoshReason(BaseModel):
    manager=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    reason_type=models.ForeignKey(ManagerReasonType,on_delete=models.CASCADE,blank=True,null=True)
    description=models.CharField(max_length=200,blank=True,null=True)
    emoji_point=models.IntegerField(null=True,blank=True)  # 1,2,3,4,5


    def __str__(self):
        return str(self.manager.user.first_name)+" "+str(self.manager.user.last_name)+ "|"+str(self.manager.created_at)




# Create your models here.

class ChallengePurpose(BaseModel):
    purpose_name = models.CharField(max_length=100)
    status=models.IntegerField(default=1)


    def __str__(self):
        return self.purpose_name
        
class TeamChallenge(BaseModel):
    manager=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    
    industry_work_type=models.IntegerField(null=True,blank=True)
    kpi_name_id=models.IntegerField(null=True,blank=True)

    customer_accepted_id=models.IntegerField(null=True,blank=True) # Challenge Accepted by Customer
    challenge_purpose=models.ForeignKey(ChallengePurpose,on_delete=models.CASCADE)
    challenge_name=models.CharField(max_length=50)

    start_time=models.CharField(max_length=20)

    end_time=models.CharField(max_length=20)

    activity_details=models.CharField(max_length=200)
    bonus_point=models.IntegerField()                     # Target
    is_broadcasted=models.IntegerField(default=0)
    is_accepted=models.IntegerField(default=0)
    is_completed_by_customer=models.IntegerField(default=0,null=True,blank=True)  # end challenge
    is_completed_by_manager=models.IntegerField(default=0,null=True,blank=True)   # end challenge
    
    customer_accepted_date =models.DateField(null=True,blank=True)
    customer_accepted_time =models.CharField(max_length=30,null=True,blank=True)
    
    customer_completed_date =models.DateField(null=True,blank=True)
    customer_completed_time =models.CharField(max_length=30,null=True,blank=True)

    manager_created_date =models.DateField(null=True,blank=True)  # yy-mm-dd
    manager_created_time =models.CharField(max_length=30,null=True,blank=True)
    
    manager_updated_date =models.DateField(null=True,blank=True)
    manager_updated_time =models.CharField(max_length=30,null=True,blank=True)
    end_challenge_time = models.CharField(max_length=20,null=True,blank=True) # H:M

    kpi_target = models.IntegerField(null=True,blank=True)

    start_time_type =models.CharField(max_length=10,null=True,blank=True)

    end_time_type   = models.CharField(max_length=10,null=True,blank=True)

    def __str__(self):
        return self.challenge_name

class CampaignPurpose(BaseModel):
    purpose_name=models.CharField(max_length=100)
    status=models.IntegerField(default=1)



# KPI's Point 

class CriteriaPoint(BaseModel):
    kpi_id=models.IntegerField(null=True,blank=True) # kpi id
    rule=models.CharField(max_length=50)             # KPI/Rule
    point=models.IntegerField()                      # Target

    def __str__(self):
        return self.rule + "  " +str(self.point)


class TeamCampaign(BaseModel):
    manager=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    
    industry_work_type=models.IntegerField(null=True,blank=True)
  
    campaign_purpose=models.ForeignKey(CampaignPurpose,on_delete=models.CASCADE)
    
    customer_accepted_id=models.IntegerField(null=True,blank=True) # Campaign Accepted by Customer
    
    criteria_point=models.ManyToManyField(CriteriaPoint)
    campaign_name=models.CharField(max_length=50)
    start_date=models.DateField()

    end_date=models.DateField()
  
    is_broadcasted=models.IntegerField(default=0)
    is_accepted=models.IntegerField(default=0,null=True,blank=True)
    is_completed_by_customer=models.IntegerField(default=0,null=True,blank=True)  # end campaign
    is_completed_by_manager=models.IntegerField(default=0,null=True,blank=True)   # end campaign

    end_campaign_date = models.DateField(null=True,blank=True)

    end_campaign_time = models.CharField(max_length=20,null=True,blank=True) # H:M:S



    def __str__(self):
        return self.campaign_name



class ManagerConcernCategory(BaseModel):
    name=models.CharField(max_length=100)
    status=models.IntegerField(default=1)

    def __str__(self):
        return self.name + "|" + str(self.id)


class ManagerRaiseConcern(BaseModel):
    concern_category=models.ForeignKey(ManagerConcernCategory,on_delete=models.CASCADE)
    description=models.CharField(max_length=100)
    user_profile=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    action_owner_id=models.IntegerField(null=True,blank=True)   # Concern send to Super Admin User 
    comment=models.CharField(max_length=100,null=True,blank=True)
    status=models.IntegerField(default=1) # 1 means open/ 0 closed


    def __str__(self):

        return self.concern_category.name





# Industry work Type 
class IndustryWorkType(BaseModel):   # Same as Team Name
    organiztaion=models.ForeignKey(Organiztaion,on_delete=models.SET_NULL,null=True)
    name=models.CharField(max_length=90,null=True)
    status=models.IntegerField(default=1,null=True)

    def __str__(self):
        return self.name + "|" + self.organiztaion.organization_name

      

# KPI Name
class KpiName(BaseModel):
    industry_work_type=models.ForeignKey(IndustryWorkType,on_delete=models.SET_NULL,null=True,blank=True)
    organiztaion=models.ForeignKey(Organiztaion,on_delete=models.SET_NULL,null=True,blank=True)
    name=models.CharField(max_length=30,null=True)

    def __str__(self):
        return self.name

        #  +self.organiztaion.unique_code 
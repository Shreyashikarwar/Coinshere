from importlib.resources import Resource
from django.db import models
from accounts.models import BaseModel, Organiztaion, UserProfile,Role

from line_manager_app.models import Team,Manager,KpiName

# from line_manager_app import ChallengePurpose,CampaignPurpose
# from coin_here.customer_service_app.views import challenge_lists


# Create your models here.




# create organizationToken
class OrganizationToken(BaseModel):
    token=models.CharField(max_length=500,null=True,blank=True)
    organization=models.ForeignKey(Organiztaion,on_delete=models.CASCADE,null=True,blank=True,related_name='organization')

    def __str__(self):
        return self.token



# Comapany portal

class CompanySite(BaseModel):
    organization = models.ForeignKey(Organiztaion,on_delete=models.CASCADE,null=True,blank=True)
    title=models.CharField(max_length=50,null=True)
    image_data=models.ImageField(default=0, upload_to='CompanySite/image/')
    site_url=models.CharField(max_length=500,null=True,blank=True)
    status=models.IntegerField(default=1,null=True,blank=True)
    
    class Meta:
         verbose_name = "Company Site | Company Portal"

    def __str__(self):
        return self.title

# Skill and Hobby

class SkillAndHobby(BaseModel):
    organization = models.ForeignKey(Organiztaion,on_delete=models.CASCADE,null=True,blank=True)
    title=models.CharField(max_length=50,null=True)
    image_data=models.ImageField(default=0, upload_to='skill_and_hobby/images/')
    site_url=models.CharField(max_length=500,null=True,blank=True)
    status=models.IntegerField(default=1,null=True,blank=True)
  
    class Meta:
         verbose_name = "Skill And Hobby | Skill & Hobby"

    def __str__(self):
        return self.title



# Heath & Fitness Videos
class LeaderShipTask(BaseModel):
    organization = models.ForeignKey(Organiztaion,on_delete=models.CASCADE,null=True,blank=True)

    title=models.CharField(max_length=50,null=True)
    video_url=models.CharField(max_length=500)
    status=models.IntegerField(default=1)
  
    class Meta:
        verbose_name = "Leader ShipTask  | Heath & Fitness"

    def __str__(self):
        return self.title


# Learning Material
class LearningMaterial(BaseModel):
    organization = models.ForeignKey(Organiztaion,on_delete=models.CASCADE,null=True,blank=True)

    title=models.CharField(max_length=50,null=True)
    image_data=models.ImageField(default=0,)
    learning_site_url = models.CharField(max_length=500)
    status = models.IntegerField(default=1)

    class Meta:
             verbose_name = "Learning Material  | Learning Material"
    def __str__(self):
        return self.title
        


# Other Links 
class OtherLink(BaseModel):
    organization = models.ForeignKey(Organiztaion,on_delete=models.CASCADE,null=True,blank=True)

    title=models.CharField(max_length=50,null=True)
    image_data=models.ImageField(default=0, upload_to='OtherLink/image/')
    url=models.CharField(max_length=500)
    status=models.IntegerField(default=1)
    
    class Meta:
             verbose_name = "Other Link  | Other Link"

    def __str__(self):
        return self.url



class PointLevel(BaseModel):
    points=models.IntegerField()
    status=models.IntegerField(default=1)




# Game Model 
class GameName(BaseModel):
    GAME_CHOICE_SECTION = [

            ('ACTION', 'Action Game'),
            ('PUZZLE', 'Puzzle Game'),
            ('BRAIN', 'Brain Game'),
    ]
    title=models.CharField(max_length=50,null=True)
    game_type= models.CharField(max_length=20,choices=GAME_CHOICE_SECTION,default='ACTION')
    game_url = models.URLField(max_length=200,null=True)
    logo=models.ImageField(default=0, upload_to='game_play/image',null=True,blank=True)
    organization =models.ForeignKey(Organiztaion, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    purpose=models.CharField(max_length=220,null=True)
    benefits=models.CharField(max_length=300,null=True)
    game_time=models.CharField(max_length=300,null=True,blank=True)
    status = models.IntegerField(default=1)
    
    def __str__(self):
        return self.title + "    : -  " + self.organization.organization_name  + ' |' + str(self.id)


# Organization City Data
class OrganizationCity(models.Model):
    city_name=models.CharField(max_length=220,null=True,blank=True)
    status=models.IntegerField(null=True,blank=True)


    def __str__(self):
        return self.city_name  +' | ' +str(self.id)


class OrganizationEmployeeData(BaseModel):
    organization=models.ForeignKey(Organiztaion,on_delete=models.SET_NULL,null=True)

    emp_code=models.CharField(max_length=100,null=True)
    full_name=models.CharField(max_length=100,null=True,blank=True)

    email=models.CharField(max_length=250,null=True)
    mobile_no=models.IntegerField(null=True)
    gender=models.CharField(max_length=50,null=True)
    designation=models.CharField(max_length=320,null=True)
    organization_city=models.ForeignKey(OrganizationCity,on_delete=models.SET_NULL,null=True,blank=True)
    location=models.CharField(max_length=120,null=True)
    team=models.ForeignKey(Team,on_delete=models.SET_NULL,null=True)
    manager=models.ForeignKey(Manager,on_delete=models.SET_NULL,null=True)
    language=models.CharField(max_length=100,null=True)
    role =models.ForeignKey(Role,on_delete=models.CASCADE,null=True,blank=True)
     

    def __str__(self):
        return str(self.full_name) +"|"+ self.team.team_name + " Team" + "|" + self.role.role_name





class OrganizationEmployeePerformanceData(BaseModel):
    organization=models.ForeignKey(Organiztaion,on_delete=models.SET_NULL,null=True)
    
    organization_employee_data=models.ForeignKey(OrganizationEmployeeData,on_delete=models.SET_NULL,null=True)

    kpi_name=models.CharField(max_length=100,null=True)

    kpi_name_data=models.ForeignKey(KpiName,on_delete=models.SET_NULL,null=True) 

    kpi_type=models.CharField(max_length=100,null=True)

    kpi_target=models.FloatField(null=True,blank=True)

    target_time_period=models.CharField(max_length=50,null=True)

    kpi_actual=models.FloatField(null=True,blank=True)

    permormance_date=models.DateTimeField(null=True,blank=True)

    kpi_status=models.IntegerField(null=True)
    
    is_paid = models.IntegerField(default=0,blank=True,null=True)

    def __str__(self):
        return self.organization_employee_data.full_name 


# Reward Points Stimulator

class RewardPointsStimulator(BaseModel):
    event=models.CharField(max_length=120,null=True)
    name=models.CharField(max_length=200,null=True)
    points=models.CharField(max_length=120,null=True)
    type=models.CharField(max_length=100,null=True)
    multiplier=models.FloatField(max_length=120,null=True)
    units=models.FloatField(null=True)
    no_of_days=models.IntegerField(null=True)
    score=models.FloatField(null=True)
    inr=models.FloatField(null=True)
    percent=models.CharField(max_length=120,null=True)
    status=models.IntegerField(null=True)


    def __str__(self):
        return self.name + ' | ' + self.event+' | ' + self.points + ' | '+ str(self.status)


class AvatarImage(BaseModel):
    image=models.ImageField(upload_to ='avatar/images')
    status=models.IntegerField(default=1)



    # # def __str__(self):
    #     return self.name + ' | ' + self.event+' | ' + self.points + ' | '+ str(self.status)


class ActivityLog(models.Model):
    module = models.CharField(max_length=100, blank=True, null=True)
    sub_module = models.CharField(max_length=100, blank=True, null=True)
    heading = models.TextField()
    activity = models.TextField()
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=150)
    icon = models.CharField(max_length=100, blank=True, null=True)
    platform = models.CharField(max_length=50)
    platform_icon = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.module + ' | ' + self.user_name



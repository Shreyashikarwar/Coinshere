from dataclasses import fields
from pyexpat import model
from rest_framework import serializers 


# Import Models 
from .models import ManagerConcernCategory,ManagerRaiseConcern,ManagerReasonType,ManagerJoshReason,Manager,TeamCampaign




# Manager Concern Category Serializers 


class  ManagerConcernCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model= ManagerConcernCategory
        fields = "__all__"


class ManagerRaiseConcernSerializers(serializers.ModelSerializer):

    class Meta:
        model = ManagerRaiseConcern
        fields = "__all__"
        



# Manager Reason Type

class ManagerReasonTypeSerializers(serializers.ModelSerializer):

    class Meta:
        model = ManagerReasonType
        fields="__all__"




# Manager Raise Concern

class ManagerJoshReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerJoshReason
        fields ="__all__"



# # Team Profile
class ManagerSerializer(serializers.ModelSerializer):
    class Meta:

        model=Manager
        depth = 2
        fields = "__all__"
        


# Team Campaign Serializers fro KPI's Data
class TeamCampaignSerializers(serializers.ModelSerializer):

    class Meta:
        model= TeamCampaign
        depth=1
        fields=('criteria_point',)

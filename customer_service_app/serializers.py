from dataclasses import fields
from pyexpat import model
from rest_framework import serializers 



#Models Import 
from .models import CustomerConcernCategory,CustomerRaiseConcern,ReasonType,JoshReason,MyRewardPoint,watchTimeData,CustomerPlayedGame,ChallengePoint,CampaignPoint,ReadSkillAndHobbyData,LearningMaterialWatchTimeData





# CustomerConcernCategory Serializers (Choice Fields)

class CustomerConcernCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomerConcernCategory
        fields = "__all__"
        




#  CustomerRaiseConcern Data
class CustomerRaiseConcernSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomerRaiseConcern
        fields = "__all__"



# Customer Reason Type
class ReasonTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = ReasonType
        fields = "__all__"



# Josh Reason
class JoshReasonSerializers(serializers.ModelSerializer):

    class Meta:
        model = JoshReason
        fields = "__all__"
        


# MyRewardPoint
class MyRewardPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyRewardPoint
        depth=1
        fileds ="__all__"

# watch Time
class watchTimeDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = watchTimeData
        fields= "__all__"

# watch Time
class ReadSkillAndHobbyTimeDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadSkillAndHobbyData
        fields= "__all__"


# watch Time
class LearningMaterialTimeDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningMaterialWatchTimeData
        fields= "__all__"




# Customer Played Game
class CustomerPlayedGameSerializer(serializers.ModelSerializer):
    class Meta:
        model= CustomerPlayedGame
        fields= "__all__"



# Challenge Point Data
class ChallengePointSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengePoint
        fields = "__all__"
        


# Campaign Point Data
class CampaignPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengePoint
        fields = "__all__"


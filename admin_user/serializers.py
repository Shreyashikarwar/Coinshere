from dataclasses import fields
from rest_framework import serializers

# Models Import 
from .models import  CompanySite,LeaderShipTask,LearningMaterial,OtherLink,GameName




# company site   API
class CompanySiteSerializers(serializers.ModelSerializer):
    class Meta:
        model = CompanySite
        fields="__all__"



# Leader Ship Task  API
class LeaderShipTaskSerializers(serializers.ModelSerializer):
    class Meta:
        model = LeaderShipTask
        fields="__all__"



# Learning Material   API
class LearningMaterialSerializers(serializers.ModelSerializer):
    class Meta:
        model = LearningMaterial
        fields="__all__"




# Other Links   API
class OtherLinkSerializers(serializers.ModelSerializer):
    class Meta:
        model = OtherLink
        fields="__all__"




# GameName API

class GameNameSerializers(serializers.ModelSerializer):
    class Meta:
        model=GameName
        fields = "__all__"
        
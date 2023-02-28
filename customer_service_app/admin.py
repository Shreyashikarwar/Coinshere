from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(ReasonType)
admin.site.register(JoshReason)

admin.site.register(Notification)
admin.site.register(ActivityLog)
admin.site.register(CustomerConcernCategory)
admin.site.register(CustomerRaiseConcern)


admin.site.register(MyRewardPoint)



# class MyRewardPointAdmin(admin.ModelAdmin):
#     list_display = ('created_at',)

# admin.site.register(MyRewardPoint,MyRewardPointAdmin)

admin.site.register(GamePoint)
admin.site.register(ChallengePoint)
admin.site.register(CampaignPoint)




# deo abhinav 
admin.site.register(watchTimeData)


admin.site.register(CustomerPlayedGame)


admin.site.register(TeamAcceptChallengeHistory)

admin.site.register(TeamAcceptCampaignHistory)


admin.site.register(HealthHabbit)

admin.site.register(HealthMetric)

admin.site.register(StepsTaken)


admin.site.register(ReadSkillAndHobbyData)


admin.site.register(LearningMaterialWatchTimeData)

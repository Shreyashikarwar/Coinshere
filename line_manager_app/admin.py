from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(ChallengePurpose)
admin.site.register(CampaignPurpose)
admin.site.register(CriteriaPoint)


class TeamChallengeAdmin(admin.ModelAdmin):
    list_display = ('challenge_name','created_at','updated_at')



admin.site.register(TeamChallenge,TeamChallengeAdmin)



admin.site.register(TeamCampaign)


# admin.site.register(ManagerorOrganization)

admin.site.register(ManagerConcernCategory)

admin.site.register(ManagerRaiseConcern)

admin.site.register(Team)

admin.site.register(Manager)

admin.site.register(ManagerReasonType)

admin.site.register(ManagerJoshReason)



admin.site.register(IndustryWorkType)
admin.site.register(KpiName)
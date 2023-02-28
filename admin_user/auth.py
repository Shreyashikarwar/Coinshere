from lib2to3.pgen2 import token
from requests import request
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from yaml import serialize


# Create Cutomise Custome AUth Token
# class CustomAuthToken(ObtainAuthToken):
#     def post(self,request,*args, **kwargs):

#         serializer=self.serializer_class(data=request.data,context={'request':request})
#         serializer.is_valid(raise_exception=True)
#         user=serializer.validated_data['user']
#         token,created=Token.objects.get_or_create(user=user)
#         return Response(data={'user_id':user.pk,'email':user.email,'first_name':user.first_name,'last_name':user.last_name,'password':user.password,'token':token.key})







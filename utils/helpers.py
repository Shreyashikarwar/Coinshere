from pyfcm import FCMNotification


from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import *

from customer_service_app.models import *

from admin_user.models import *

import calendar

from django.template.loader import get_template

from django.core.mail import EmailMessage

from coin_here.settings import EMAIL_HOST_USER

import math, random

from twilio.rest import Client

import uuid

import string

from cryptography.fernet import Fernet

import http.client as ht


# send android push notifications

def send_android_notification(message_title, message_body, data_message,registration_ids):

    firebase_server_key = Configuration.objects.filter(status=1).first()

    if firebase_server_key.firebase_server_key is not None and firebase_server_key.firebase_server_key != "":

        push_service = FCMNotification(api_key=firebase_server_key.firebase_server_key)

        result =  push_service.notify_multiple_devices(registration_ids=registration_ids,message_title=message_title, message_body=message_body, data_message=data_message)

        return result


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
  
    }



def generate_random_number():
    digits = [i for i in range(0, 10)]

    random_str = ""

    for i in range(6):

        index = math.floor(random.random() * 10)
        
        random_str += str(digits[index])
    return random_str



def save_notification(from_user_id,to_user_id,heading,notification_msg,redirectional_code):

  
    notification = Notification()

    notification.from_user_id           = from_user_id
    notification.to_user_id             = to_user_id
    notification.heading                = heading
    notification.activity               = notification_msg
    notification.redirectional_code     = redirectional_code


    notification.save()


def weeks_in_month(year, month):
    
    return len(calendar.monthcalendar(year, month))


def numberOfDays(y, m):
    
      leap = 0

      if y% 400 == 0:

         leap = 1

      elif y % 100 == 0:

         leap = 0

      elif y% 4 == 0:

         leap = 1

      if m==2:

         return 28 + leap

      list = [1,3,5,7,8,10,12]

      if m in list:

         return 31

      return 30


def convert_seconds_to_hours(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    time ="%d:%02d:%02d" % (hour, minutes, seconds)
    return time


def convert_seconds_to_minutes(seconds):
    seconds = seconds % (24 * 3600)
    minutes = seconds // 60
   
    return minutes



def save_activity(module,sub_module,heading,activity_msg,user_id,user_name,icon,platform,platform_icon):
    
    activity = ActivityLog()

    activity.module = module

    activity.sub_module = sub_module

    activity.heading = heading

    activity.activity = activity_msg

    activity.user_id = user_id

    activity.user_name = user_name

    if icon:

        activity.icon = icon

    else:

       activity.icon = 'add.png'     

    activity.platform = platform

    if platform_icon:

        activity.platform_icon = platform_icon

    else:

        activity.platform_icon = 'web.png'    

    activity.save()



def int_to_roman(num):
      
    m = ["", "M", "MM", "MMM"]
    
    c = ["", "C", "CC", "CCC", "CD", "D",
         "DC", "DCC", "DCCC", "CM "]
         
    x = ["", "X", "XX", "XXX", "XL", "L",
         "LX", "LXX", "LXXX", "XC"]
         
    i = ["", "I", "II", "III", "IV", "V",
         "VI", "VII", "VIII", "IX"]
  
 
    thousands = m[num // 1000]
    hundreds = c[(num % 1000) // 100]
    tens = x[(num % 100) // 10]
    ones = i[num % 10]
  
    ans = (thousands + hundreds +
           tens + ones)
  
    return ans

# used for send otp on email

def send_email(request, template, context, subject, recipient):
    
    subject = subject

    message = get_template(template).render(context)

    msg = EmailMessage(

        subject,

        message,

        EMAIL_HOST_USER,

        [recipient],

    )

    msg.content_subtype = "html"  

    msg.send()

    print("Mail successfully sent")

# used for send otp on mobile no

# def send_sms(sender_id,mobile,message):
    
#     url = 'https://alerts.cbis.in/SMSApi/send'

#     postdata = {

#         "userid": "sahaj",

#         "password": "MilK@01",

#         "sendMethod": "quick",

#         "senderid": sender_id,

#         "mobile": mobile,

#         "msg": message,

#         "msgType": 'unicode',

#         "duplicatecheck": 'true',

#         "duplicatecheck": 'json'

#         }

#     response = requests.post(url, data=postdata)

#     return response.status_code





def generate_otp() : 

    digits = "0123456789"

    OTP = "" 
 
    for i in range(4) : 

        OTP += digits[math.floor(random.random() * 10)] 

    return OTP




TWILIO_ACCOUNT_SID = "fgdyht6765hgfd54tjiuoly896"
TWILIO_AUTH_TOKEN  = "h7qw8euho48998hhjfdhs87qwyaj"


from_mobile_no     = "whatsapp:+91999999999"


def broadcast_message_on_whatsapp(body):
    
   
    account_sid = TWILIO_ACCOUNT_SID
    auth_token =  TWILIO_AUTH_TOKEN

    client = Client(account_sid, auth_token)
    
    to_mobile_no = "whatsapp:+9999999999"

    message = client.messages.create(
            body=body,
            from_=from_mobile_no,
            to=to_mobile_no
        )
    
    print("twilio===>",message.sid)


def generate_token():
    random_token = uuid.uuid4().hex
    return random_token




def generate_random_password():

    characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")

    length = 6
        
    random.shuffle(characters)
    password = []

    for i in range(length):
        password.append(random.choice(characters))

    random.shuffle(password)

    password = "".join(password)

    return password



def encrypt_password(password):
    
    key = Fernet.generate_key()

    fernet = Fernet(key)

    enc_password = fernet.encrypt(password.encode())
    
    return enc_password
 
  
def decrypt_password(password):
    
    key = Fernet.generate_key()

    fernet = Fernet(key)

    dec_password = fernet.decrypt(password).decode()
    
    return dec_password





def send_sms(mobile_no):
  
    conn = ht.HTTPSConnection("api.msg91.com")

    payload = '''{"flow_id": "5436y5tyht65y65ts","sender": "33424","recipients": [{"mobiles":"54365436"}]}'''


    headers = {
        'authkey': "",
        'content-type': "application/JSON"
        }

    conn.request("POST", "/api/v5/flow/", payload, headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))

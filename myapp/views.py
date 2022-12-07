from datetime import datetime
import boto3
import os
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from Restaurant_sns import RestaurantSNS
from botocore.exceptions import ClientError
import logging
from table_token_generater_x21174105 import token

#from publisher import Publisher

# Create your views here.
# from myapp.models import Contact
from .models import booking, table


#SNS 

#SMS_ACTIVATE = True
#SITE_URL = "http://3.239.65.42:8080" 

#if SMS_ACTIVATE:
a_publisher = RestaurantSNS()


def index(request):
    return render(request, 'index.html')


def home(request):

    return render(request, 'index.html')

def menu(request):
    return render(request, 'menu.html')


def reservations(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        date = request.POST.get('date')
        time = request.POST.get('time')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        people = request.POST.get('people')

        reservations = table(name=name, email=email,date=date,time=time,phone=phone,message=message,people=people)

        reservations.save()
        message = "Your table is book and ReservationID #" + token.createtoken()
        a_publisher.send_SMS_message(phone,message)

    return render(request, 'reservations.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        contact = booking(name=name, email=email, subject=subject, message=message)

        contact.save()

    return render(request, 'contact.html')


def gallery(request):

    return render(request, 'gallery.html')


def handleSignup(request):
    if request.method == 'POST':
        # get the post parameters#
        username = request.POST['username']
        fname = request.POST['fname1']
        lname = request.POST['lname1']
        email = request.POST['email1']
        password1 = request.POST['password2']
        password2 = request.POST['password4']
        
        #images =['1.jpeg','2.jpeg','3.jpeg','4.jpeg','5.jpeg','6.jpeg','7.jpeg','9.jpeg','10.jpeg','11.jpeg','chicken.jpeg','colddrinks.jpeg','dinner.jpeg','img-04.jpg','italian.jpeg','logo1.jpeg','logo2.jpeg','momos.jpeg','northindian.jpeg','pizza.jpeg','pizza1.jpeg','sandwich.jpeg','southindian.jpg']
        #images =['logo1 .png','logo2.png']
        #size=len(images);
        # checks for error in filling form
        #validating signupup form
        #for i in images:
            #print(i)
            #upload_file("foodstaticimagesnew",os.path.join(os.getcwd(),"static/img/" + i));
            
        if len(username)>10:
            messages.error(request,"username must be be under 10 character")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, "username must be contain letters and numbers")
            return redirect('home')

        if password1!=password2:
            messages.error(request, "password doesnt match")
            return redirect('home')

        myuser = User.objects.create_user(username,email,password1)
        myuser.first_name = fname
        myuser.last_name = lname
        #myuser.image = image
        myuser.save()
        messages.success(request,"Your account is successfully created")
        return redirect('home')

    else:
        return HttpResponse('404 not found')

def handlelogin(request):
    if request.method == 'POST':
        # get the post parameters#
        username = request.POST['username']
        password= request.POST['password6']

        user =authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            messages.success(request,"Successfully loggged in")
            return redirect('home')
        else:
            messages.success(request,'Invalid creditianials')

    return HttpResponse('404 not found')

def handlelogout(request):
    logout(request)
    messages.success(request,"Suucessfully logged out")
    return redirect('home')
    return HttpResponse('handlelogout')
    
def upload_file(bucket,file_name, object_key=None):
        """Upload a file to an S3 bucket
        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param key: S3 object key. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """
        if object_key is None:
            object_key = file_name
        
        s3_client = boto3.client('s3')
        try:
            response = s3_client.upload_file(file_name, bucket, object_key)
            '''
            # an example of using the ExtraArgs optional parameter to set the ACL (access control list) value 'public-read' to the S3 object
            response = s3_client.upload_file(file_name, bucket, key,
            ExtraArgs={'ACL': 'public-read'})
            '''
        except ClientError as e:
            logging.error(e)
            return False
        return True
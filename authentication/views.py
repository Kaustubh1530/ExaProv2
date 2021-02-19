from django.http import HttpResponse
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from packages.DEM import dec, enc
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from main.decorators import unauthenticated_user, allowed_users, admin_only 
from django.views.decorators.csrf import csrf_protect
import random
import datetime

otp_global = 0
register = None
email = ''

##################################### ADMIN ######################################

# ADMIN LOGIN
@csrf_protect
@unauthenticated_user
def admin_login(request):
    if request.method == 'POST':
        globals()['email'] = request.POST['email']
        password = request.POST['password']
        try:
            admin = User.objects.get(email=globals()['email'])
            if admin is not None:
                if admin.check_password(password):
                    login(request,admin)
                    return redirect('admin-home')
                else:
                    err_msg = "Incorrect password"
                    return render(request, 'templates_authentication/admin_login.html', {'err_msg': err_msg})
        except ObjectDoesNotExist:
            err_msg = "Account doesn't exist"
            return render(request, 'templates_authentication/admin_login.html', {'err_msg': err_msg})
    else:
        return render(request, 'templates_authentication/admin_login.html')

def admin_logout(request):
    logout(request)
    return redirect('admin-login')

@csrf_protect
@login_required(login_url='admin-login')
@admin_only
def admin_home(request):
    return render(request,'templates_panels/admin_home.html')

##################################### USER #######################################

# USER SIGNUP
@unauthenticated_user
def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        globals()['email'] = request.POST['email']
        globals()['password'] = request.POST['password']
        conf = request.POST['conf_pass']
        try:
            globals()['register'] = User.objects.get(
                email=globals()['email'])
            err_message = "Account already exists"
            return render(request, 'templates_authentication/user_signup.html', {'err_message': err_message})
        except ObjectDoesNotExist:
            if len(globals()['password']) <= 4 or len(globals()['password']) > 16:
                err_pass = "Password must be more than 4 and less than 16 characters"
                return render(request, 'templates_authentication/user_signup.html', {'err_pass': err_pass})
            else:
                if globals()['password'] == conf:
                    globals()['register'] = User(
                        username=username, email=globals()['email'])
                    comm_otp_generation()
                    return render(request, 'templates_authentication/otp.html')
                else:
                    err_pass = "Passwords doesn't match"
                    return render(request, 'templates_authentication/user_signup.html', {'err_pass': err_pass})
    else:
        return render(request, 'templates_authentication/user_signup.html')

# USER LOGIN
@csrf_protect
@unauthenticated_user
def user_login(request):
    if request.method == 'POST':
        globals()['email'] = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=globals()['email'])
            if user is not None:
                if user.check_password(password):
                    login(request,user)
                    return redirect('user-home')
                else:
                    err_msg = "Incorrect password"
                    return render(request, 'templates_authentication/user_login.html', {'err_msg': err_msg})
        except ObjectDoesNotExist:
            err_msg = "Account doesn't exist"
            return render(request, 'templates_authentication/user_login.html', {'err_msg': err_msg})
    else:
        return render(request, 'templates_authentication/user_login.html')

# USER HOME
@login_required(login_url="user-login")
def user_home(request):
      return render(request,'templates_panels/user_home.html')
    

# USER LOGOUT
def user_logout(request):
    logout(request)
    return redirect("user-login")



##################################################################################

def verify(request):
    err_msg = ""
    try:
        if request.method == 'POST':
            try:
                otp = int(request.POST.get('otp', 0))
                if globals()['otp_global'] == otp:
                    globals()['register'].set_password(globals()['password'])
                    globals()['register'].save()
                    group = Group.objects.get(name='user')
                    globals()['register'].groups.add(group)
                    return render(request, 'templates_authentication/user_login.html')
                else:
                    err_msg = "Incorrect OTP"
                    return render(request, 'templates_authentication/otp.html', {'err_msg': err_msg})
            except ValueError:
                err_msg = "Only characters allowed"
                return render(request, 'templates_authentication/otp.html', {'err_msg': err_msg})

    except IntegrityError as e:
        err_msg = "Account already exists"
        return render(request, 'templates_authentication/otp.html', {'err_msg': err_msg})


def generate(request):
    comm_otp_generation()
    return render(request, 'templates_authentication/otp.html')

@login_required(login_url="user-login")
def change_pass(request):
    if request.method == 'POST':
        globals()['email'] = request.POST['email']
        globals()['password'] = request.POST['pass']
        conf_pass = request.POST['conf_pass']

        try:
            globals()['register'] = User.objects.get(
                email=globals()['email'])
            if globals()['password'] == conf_pass:
                if len(globals()['password']) <= 4 or len(globals()['password']) > 16:
                    err_msg = "Password must be more than 4 and less than 16 characters"
                    return render(request, 'templates_authentication/changepass.html', {'err_msg': err_msg})
                else:
                    globals()['register'].password = globals()['password']
                    comm_otp_generation()
                    return render(request, 'templates_authentication/otp.html')

            else:
                err_msg = "Passwords doesn't match"

                return render(request, 'templates_authentication/changepass.html', {'err_msg': err_msg})

        except ObjectDoesNotExist:
            err_msg = "Account doesn't exist"

            return render(request, 'templates_authentication/changepass.html', {'err_msg': err_msg})

    else:
        return render(request, 'templates_authentication/changepass.html')


def comm_otp_generation():
    otp_rand = random.randint(1000, 9999)
    globals()['otp_global'] = otp_rand
    otp_msg = f"Email-Verification OTP : {otp_rand}"
    send_mail(
        "Welcome to ExaPro",
        otp_msg,
        'ExaPro<exapro.official@gmail.com>',
        [(globals()['email'])],
        fail_silently=False
    )





# views.py
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from . import utils
from .models import VerificationCode
from datetime import timedelta
from django.utils import timezone


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')


        # check if the username is a valid phone number and with 8 digits
        if len(username) != 8:
            messages.error(request, 'Invalid Phone Number.')
            return redirect('register')
        if not username.isdigit():
            messages.error(request, 'Invalid Phone Number.')
            return redirect('register')


        username = '+216'+username

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Phone Number already exists.')
            return redirect('register')

        user = User.objects.create_user(username=username, password=password1, first_name=first_name, last_name=last_name)
        user.save()
        messages.success(request, 'Registration successful.')
        return redirect('login')

    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        username = "+216"+username
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_staff:
                return redirect('admin_index')
            else:
                return redirect('student_index')  # Redirect to the homepage after successful login
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('login')




def password_change_step1(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if len(username) != 8:
            messages.error(request, 'Invalid Phone Number.')
            return redirect('password_change_step1')
        if not username.isdigit():
            messages.error(request, 'Invalid Phone Number.')
            return redirect('password_change_step1')
        username = '+216'+username
        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Phone Number does not exist.')
            return redirect('password_change_step1')
        request.session['username'] = username

        
        user = User.objects.get(username=username)

        # Delete the old verification code if it was created more than 1 minute ago or if it doesn't exist
        try:
            old_verification_code = VerificationCode.objects.get(user=user)
            time_since_code_sent = timezone.now() - old_verification_code.created_at
            if time_since_code_sent > timedelta(minutes=1):
                old_verification_code.delete()
            else:
                time_left = timedelta(minutes=1) - time_since_code_sent
                messages.error(request, f'Please wait {time_left.seconds} seconds before requesting a new code.')
                return redirect('password_change_step1')
        except VerificationCode.DoesNotExist:
            pass
    
        # Generate and send the new verification code
        verification_code = VerificationCode.objects.create(user=user)
        verification_code.generate_code()

        utils.send_verification_code(username, verification_code.code,user.first_name)
        messages.success(request, 'Verification code sent successfully.')
        

        return redirect('password_change_step2')  
    # set step 3 completed 
    request.session['step1_completed'] = True   
    return render(request, 'password_change_step1.html')


def password_change_step2(request):
    if request.method == 'POST':
    #    get the code and verify it 
        code = request.POST.get('code')
        username = request.session.get('username')
        user = User.objects.get(username=username)
        try:
            verification_code = VerificationCode.objects.get(user=user)
        except VerificationCode.DoesNotExist:
            messages.error(request, 'Invalid verification code.')
            return redirect('password_change_step2')
        if not verification_code.is_valid(user):
            messages.error(request, 'Invalid Or Expired verification code.')
            return redirect('password_change_step2')
        if verification_code.code != code:
            messages.error(request, 'Invalid verification code.')
            return redirect('password_change_step2')
        verification_code.delete()
        messages.success(request, 'Code Verified !')
        return redirect('password_change_step3')
        
    
    username = request.session.get('username')
    # making the first 9 digits from the right as *
    username = username[:-9] + '*'*9 + username[-1]
    context = {'username': username}

    request.session['step2_completed'] = True

    return render(request, 'password_change_step2.html',context)


def password_change_step3(request):
    # Check if all previous steps have been completed
    if not request.session.get('step1_completed') or not request.session.get('step2_completed'):
        messages.error(request, 'You must complete all previous steps first.')
        return redirect('password_change_step1')

    if request.method == 'POST':
        password1 = request.POST.get('new_password1')
        password2 = request.POST.get('new_password2')
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('password_change_step3')
        username = request.session.get('username')
        user = User.objects.get(username=username)
        user.set_password(password1)
        user.save()
        messages.success(request, 'Password changed successfully.')
        del request.session['username']
        del request.session['step1_completed']
        del request.session['step2_completed']
        return redirect('login')
        
    return render(request, 'password_change_step3.html')
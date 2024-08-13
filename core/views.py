from courses.models import Course
from django.contrib import messages
from django.shortcuts import render
from django.core.mail import send_mail
from core.models import ContactUs, Comment
from .task import send_contact_email
from elearn.settings import EMAIL_HOST_USER
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from core.forms import SignUpForm, AuthenticateUserForm, CustomPasswordChangeForm, FormContactUs

def Home(request: HttpRequest) -> HttpResponse:
    context ={
        'sign_log': True,
    }
    
    courses_list = Course.objects.all().order_by('-id')
    per_page = 3
    paginator = Paginator(courses_list, per_page)
    page_number = request.GET.get('page')
    courses = paginator.get_page(page_number)
        
    context['courses'] = courses

    if request.user.is_authenticated:
        context['sign_log'] = False
        context['loged_in'] = True
        
        return render(request, 'core/home.html', context)
    return render(request, 'core/home.html', context)

def About(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        context = {
            'loged_in': True,
        }
        return render(request, 'core/about.html', context)
    context = {
        'sign_log': True
    }
    return render(request, 'core/about.html', context)

def Contact(request: HttpRequest) -> HttpResponse:
    context = {
        'sign_log': True,
        'form' : FormContactUs()
    }
    if request.user.is_authenticated: 
        context['sign_log'] = False 
        context['loged_in'] = True 
        context['form'] = FormContactUs()
        
        if request.method == "POST":
            form = FormContactUs(request.POST)
            if form.is_valid():
                f_name = form.cleaned_data['first_name'] 
                l_name = form.cleaned_data['last_name']
                name = f_name + " " + l_name
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                subject = form.cleaned_data['subject']
                footer = form.cleaned_data['footer']
                body = name + ", " + form.cleaned_data['body'] + "\n" + footer

                print(body)

                # Use the Celery task
                task = send_contact_email.delay(subject, body, email)

                # Check if the task was successful
                if task:
                    contact = ContactUs.objects.create(
                        first_name = f_name,
                        last_name = l_name,
                        username = username,
                        email = email,
                        subject = subject,
                        body = body,
                        footer = footer
                    )
                    contact.save()
                    messages.success(request, "Mail was successfuly sent!")
                else:
                    messages.error(request, "Mail was not Successfuly Sent!")

                return render(request, 'core/contact.html', context)

            messages.error(request, "Please Fill the From Correctly!")
            return render(request, 'core/contact.html', context)

        return render(request, 'core/contact.html', context)
    
    return render(request, 'core/contact.html', context)

def SignUp(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        form = SignUpForm()
        if request.method == "POST":
            try:
                form = SignUpForm(data=request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Sign Up Successful!")
                    return HttpResponseRedirect('/')
                messages.error(request, "Something Went Wrong!")
                form = SignUpForm()
                return render(request, 'core/signup.html', {'form' : form, 'sign_log' : False})
            except Exception as e:
                print(e.__str__())
                return render(request, 'core/signup.html', {'form' : form, 'sign_log' : False})
        else:
            return render(request, 'core/signup.html', {'form' : form, 'sign_log' : False})
    return HttpResponseRedirect('/user/')

def LogIn(request: HttpRequest) -> HttpResponse :
    form = AuthenticateUserForm()

    if not request.user.is_authenticated:
        if request.method == "POST":
            try:
                fm = AuthenticateUserForm(data=request.POST)
                if fm.is_valid():
                    username = fm.cleaned_data['username']
                    password = fm.cleaned_data['password']
                    user = authenticate(username=username, password=password)
                    
                    if user:
                        if user.is_superuser:
                            messages.error(request, "Super Not Allowed")
                            return render(request, 'core/login.html', {'form': form, 'sign_log' : False})
                        login(request=request, user=user)
                        messages.success(request, "Log In Successful")
                        return HttpResponseRedirect('/')
                    else:
                        form.add_error(None, 'Invalid username or password')
                        messages.error(request, "User Not Found!")
                        return render(request, 'core/login.html', {'form': form, 'sign_log' : False})
                messages.error(request, "Please Enter Correct Credientials!")
                return render(request, 'core/login.html', {'form': form, 'sign_log' : False})
            except Exception as e:
                print(e.__str__())
                return render(request, 'core/login.html', {'form': form, 'sign_log' : False})
        else:
            return render(request, 'core/login.html', {'form': form, 'sign_log' : False})
    return HttpResponseRedirect('/')

def ChangePassword(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        form = CustomPasswordChangeForm(user=request.user)
        if request.method == "POST":
            try:
                form = CustomPasswordChangeForm(user=request.user, data=request.POST)
                if form.is_valid():
                    form.save() 
                    update_session_auth_hash(request, form.user)
                    print('Password Changes Successfuly!')
                    messages.success(request, "Password changed successfully")
                    return HttpResponseRedirect('/')
                else:
                    messages.error(request, "Please Select an Strong Password")
                    return render(request, 'core/passwordChange.html', {'form': form})
            except Exception as e:
                print(e.__str__())
        return render(request, 'core/passwordChange.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')

def LogOut(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        try:
            logout(request)
            messages.success(request, "Log Out Successful")
        except Exception as e:
            print(e.__str__())
    return HttpResponseRedirect('/')


def SendMail(request : HttpRequest) -> HttpResponse:
    try:
        subject = "Internship Offer, E-Learn"
        message = '''Hey Aniket Jagdish Kushwaha,

                    Did you do the AI internship?

                    Congratulations! You've received a prize of Rs. 550 from the Maharashtra Government. Additionally, you have been recommended for a full-time job at Artemis Tecno with a salary as per your skill. To claim the prize, upload your resume at

                    [https://drive.google.com/drive/folders/1YPFfQrIiZIbbfexnn7nNH9QTmiHYwAZT]

                    Your name will be moved to the second round based on your resume. This opportunity is only for candidates who completed the AI internship between 2023-24.
                '''
        email = EMAIL_HOST_USER
        sent_not = send_mail(
            subject,
            message,
            email,
            recipient_list= ["aniketkushwaha816@gmail.com"],
            fail_silently= False
        )

        if sent_not:
            messages.success(request, "Mail Sent!")
            return HttpResponseRedirect('/contact/')
    
        messages.error(request, "Error, Something Went Wrong!")
        return HttpResponseRedirect('/contact/')
        
    except Exception as e:
        print(e.__str__())
        return HttpResponseRedirect('/')
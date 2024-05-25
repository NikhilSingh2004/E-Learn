from courses.models import Course
from django.shortcuts import render
from django.contrib import messages
from django.core.paginator import Paginator
from users.forms  import EditProfileForm
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

def UserHome(request : HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        context = {
            'user' : request.user.username,
            'loged_in' : True,
        }

        courses_list = Course.objects.all()
        per_page = 3
        paginator = Paginator(courses_list, per_page)
        page_number = request.GET.get('page')
        courses = paginator.get_page(page_number)

        context['courses'] = courses
        return render(request, 'users/userHome.html', context)
    return HttpResponseRedirect('/login/')

def EditUser(request: HttpRequest, username: str) -> HttpResponse:
    if request.user.is_authenticated:
        form = EditProfileForm(instance= request.user)
        if request.method == "POST":
            form = EditProfileForm(request.POST)
            user = User.objects.filter(username = username).first()
            if user:
                user.username = request.POST['username']
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                user.email = request.POST['email']
                user.save()
                messages.success(request, "Profile Edited Successfuly!")
                return HttpResponseRedirect('/user/')
            messages.error(request, "Please Enter Valid Data")
            return render(request, 'users/editUser.html', {'form' : form})
        return render(request, 'users/editUser.html', {'form' : form})
    else:
        return HttpResponseRedirect('/login/')

def DeleteUser(request: HttpRequest ) -> HttpResponse:
    if request.user.is_authenticated:
        context = {
            'user' : request.user.username,
            'loged_in' : True,
        }
        try:
            user = User.objects.get(id=request.user.id)
            if user:
                if user.is_superuser:
                    messages.error(request, "Not Allowed!")
                    return render(request, 'users/userHome.html', context)
                user.delete()
                messages.warning(request, "User Deleted!")
                return HttpResponseRedirect('/')
            messages.error(request, "Something Went Wrong!")
            return render(request, 'users/userHome.html', context)
        except Exception as e:
            print(e.__str__())
            messages.error(request, "User Not Found!")
            return render(request, 'users/userHome.html', context)
    return HttpResponseRedirect('/login/')
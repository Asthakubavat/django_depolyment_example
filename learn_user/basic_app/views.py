from django.shortcuts import render
from basic_app.forms import ProfileInfo,basicUserInfo
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse

def index(req):
    return render(req,'basic_app/index.html')



@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))



def register(request):
    registered = False

    if  request.method=="POST":
        user_form =  basicUserInfo(data=request.POST)
        profile_form = ProfileInfo(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic=request.FILES['profile_pic']

            profile.save()


            registered  = True
        else:
            print(user_form.errors,profile_form.errors)


    else:
        user_form = basicUserInfo()
        profile_form = ProfileInfo()

    return render(request,'basic_app/register.html',{'user':user_form,'profile':profile_form,'registered':registered})



# Create your views here.
def user_login(request):
    auth=False
    if request.method=='POST':
        username= request.POST.get('username')
        password= request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse(req,"your account is not active ")

        else:
            print("someone tried to login and failed")

            return HttpResponse("invalid login details supplied")

    else:

        return render(request,'basic_app/user_login.html')

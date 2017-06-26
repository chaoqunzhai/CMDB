from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page



@cache_page(100)
def error(request):
    return render(request,'error.html')

@login_required
@cache_page(60)
def category(request,category_id):
    if category_id == 'all':
        return render(request,'index.html')

def acc_login(request):
    errors ={}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username,password=password)
        if user:
            login(request,user)
            print('yes')
            # return redirect(request.GET.get("next") or "/")
            return redirect('/category/all/')
        else:
            errors = {"error":"用户名或者密码错误"}
            print(errors)
    return render(request,"login.html",errors)


def acc_logout(request):

    logout(request)

    return redirect("/")


from django.shortcuts import render
from django.contrib import messages
import random
import requests
from django.http import HttpResponse, HttpResponseForbidden
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth import logout

from .models import CustomUser
from .forms import CustomUserCreationForm

# Create your views here.


def welcomePage(request):
    return render(
        request=request,
        template_name='homepage.html',
        context={}
    )


def companyPage(request):
    return render(
        request=request,
        template_name='company.html',
        context={}
    )


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        print("in_post")
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            print("saved")
            return redirect('account/login')
    form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {"form": form})


def log_out(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('/account/login')


def userPage(request):
    if request.user.is_authenticated:
        user = CustomUser.objects.get(email=request.user.email)
        return render(
            request=request,
            template_name='userDetail.html',
            context={
                "email_id": str(user),
            }
        )
    return HttpResponseForbidden('<h1>Access Denied</h1>')


def send_testGraphData(request):

    url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&interval=5min&apikey=demo"

    temp = requests.get(url).json()
    # print(temp.get("Meta Data"))
    stockData = temp.get("Time Series (5min)")
    # print(stockData)
    countLim = 10
    xData = list(stockData.keys())

    xTime = []
    for i in xData:
        xTime.append(i.split()[1])

    # print(xData[:countLim])
    yData = []
    for i in xData:
        yData.append(float(stockData.get(i).get("1. open")))
    print(yData[:10])

    # l = random.randint(1,30)
    # x = []
    # y = []
    # for i in range(l):
    # 	x.append(random.randint(1,5))
    # 	y.append(x[-1]**2)

    return JsonResponse({
        "x_axis": xTime[:10],
        "y_axis": yData[:10]
    })

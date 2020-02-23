from django.shortcuts import render
from django.contrib import messages
import random
import requests
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views import generic

from .models import CustomUser, Company, Shares
from .forms import CustomUserCreationForm, CompanyRegistrationForm, CompanySharesUpdateForm, SharesSaleUpdateForm


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


@login_required
def newCompany(request):
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.owner = request.user
            company.save()
            create_share = Shares(
                company=company, user=request.user, shares_count=0)
            create_share.save()
            return redirect(myCompanies)

    form = CompanyRegistrationForm()
    return render(request, 'registration/company.html', {"form": form})


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('accounts/login')
    form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {"form": form})


def log_out(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged out successfully!")
    else:
        messages.warning(request, "You Are not Logged in")
    return redirect('/accounts/login')


@login_required
def market(request):
    return MarketView.as_view()(request)


class MarketView(generic.ListView):
    model = Shares
    context_object_name = 'market_list'
    template_name = "market.html"

    def get_queryset(self):
        shr = Shares.objects.exclude(
            user=self.request.user).filter(shares_sale__gte=1)
        return shr


@login_required
def userPage(request):
    user = CustomUser.objects.get(email=request.user.email)
    return render(
        request=request,
        template_name='userDetail.html',
        context={
            "email_id": str(user),
        }
    )


@login_required
def editCompanyShares(request, id):
    obj = get_object_or_404(Shares, id=id)
    form = CompanySharesUpdateForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save(commit=True)
        return redirect(myCompanies)
    return render(request, 'registration/gen_form.html', {"form": form, "head": 'Edit Company Shares', "redirect": 'edit_shares'})


@login_required
def sellMyShares(request, id):
    obj = get_object_or_404(Shares, id=id)
    form = SharesSaleUpdateForm(request.POST or None, instance=obj)
    print("dssfa")
    print(form.is_valid())
    if form.is_valid():
        form.save(commit=True)
        return redirect(myShares)
    return render(request, 'registration/gen_form.html', {"form": form, "head": 'Sell My Shares', "redirect": 'sell_shares', "id": id})


@login_required
def myCompanies(request):
    return myCompaniesView.as_view()(request)


class myCompaniesView(generic.ListView):
    model = Shares
    context_object_name = 'my_companies_list'
    template_name = "my_company.html"

    def get_queryset(self):
        cp = Company.objects.filter(owner=self.request.user)
        shr = Shares.objects.filter(user=self.request.user, company__in=cp)
        return shr


@login_required
def myShares(request):
    return mySharesView.as_view()(request)


class mySharesView(generic.ListView):
    model = Shares
    context_object_name = 'my_shares_list'
    template_name = "my_shares.html"

    def get_queryset(self):
        shr = Shares.objects.filter(user=self.request.user)
        return shr


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
    y2Data = []
    y3Data = []

    for i in xData:
        yData.append(float(stockData.get(i).get("1. open")))
        y2Data.append(float(stockData.get(i).get("2. high")))
        y3Data.append(float(stockData.get(i).get("3. low")))

    print(yData[:10])

    # l = random.randint(1,30)
    # x = []
    # y = []
    # for i in range(l):
    # 	x.append(random.randint(1,5))
    # 	y.append(x[-1]**2)

    return JsonResponse({
        "x_axis": xTime[:10],
        "y_axis": yData[:10],
        "y2_axis": y2Data[:10],
        "y3_axis": y3Data[:10],
    })

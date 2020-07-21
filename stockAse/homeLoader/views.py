from django.shortcuts import render
from django.contrib import messages
import random
import requests
from datetime import datetime
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.db import transaction
from django.utils import timezone

from .models import *
from .forms import CustomUserCreationForm, CompanyRegistrationForm, CompanySharesUpdateForm, SharesSaleUpdateForm, BuySharesUpdateForm
from .filters import SharesFilter


def welcomePage(request):
    company_list = Company.objects.all()
    return render(
        request=request,
        template_name='homepage.html',
        context={"company_list": company_list}
    )


def companyPage(request, id):
    obj = get_object_or_404(Company, id=id)
    return render(
        request=request,
        template_name='company.html',
        context={"company": obj}
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
        else:
            print("not valid")
            return render(request, 'registration/company.html', {"form": form})

    form = CompanyRegistrationForm()
    return render(request, 'registration/company.html', {"form": form})


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(
                request, "Account Created Successfully. Login and start earning!")
            return redirect('accounts/login')
        else:
            print("not valid")
            return render(request, 'registration/signup.html', {"form": form})
    form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {"form": form})


def log_out(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged out successfully!")
    else:
        messages.error(request, "You Are not Logged in")
    return redirect('/accounts/login')


def friendPage(request, id):
    friend = get_object_or_404(CustomUser, id=id)
    shr = Shares.objects.filter(user=friend, shares_sale__gte=1)
    return render(
        request=request,
        template_name='friendDetail.html',
        context={
            "friend": friend,
            "friend_sell_list": shr
        }
    )


@login_required
def market(request):
    shares_list = Shares.objects.filter(shares_sale__gte=1)
    shares_filter = SharesFilter(request.GET, queryset=shares_list)
    context = {
        'filter': shares_filter,
        'companies': Company.objects.all(),
    }
    return render(request, 'market.html', context=context)


@login_required
def userPage(request):
    user = CustomUser.objects.get(email=request.user.email)
    # cp = Company.objects.filter(owner=request.user)
    shr = Shares.objects.filter(user=request.user)
    get_as_seller = Transaction.objects.filter(seller=request.user)
    get_as_buyer = Transaction.objects.filter(buyer=request.user)
    get_transactions = get_as_buyer | get_as_seller
    return render(
        request=request,
        template_name='userDetail.html',
        context={
            "email_id": str(user),
            "balance": user.balance,
            "my_shares_list": shr,
            "my_transactions_list": get_transactions
        }
    )


@login_required
def startTransaction(request, id):
    obj = get_object_or_404(Transaction, id=id)
    shr = get_object_or_404(Shares, user=obj.seller, company=obj.company)
    form = BuySharesUpdateForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid() and form.save(commit=False).shares_count <= shr.shares_count:
        var = form.save(commit=False)
        var.total_amount = var.shares_count * var.cost_price
        var.save()
        return render(request, 'payment_page.html', {"transaction": obj})
    elif form.is_valid() and form.save(commit=False).shares_count > shr.shares_count:
        print(shr.shares_count)
        messages.error(request, "You cannot buy more than available")
    return render(request, 'buy_share.html', {"form": form, "head": 'Sell My Shares', "transaction": obj, "share": shr})


@login_required
@transaction.atomic
def makepayment(request, id):
    obj = get_object_or_404(Transaction, id=id)
    buyer_balance = obj.buyer.balance
    if buyer_balance < obj.total_amount:
        raise Exception("Payment Failed due to Low Balance!")

    # start payment
    buyer = obj.buyer
    seller = obj.seller
    buyer.balance -= obj.total_amount
    seller.balance += obj.total_amount
    seller_share = Shares.objects.filter(user=seller, company=obj.company)[0]
    seller_share.shares_sale -= obj.shares_count
    seller_share.shares_count -= obj.shares_count
    buyer_share = None
    if not not Shares.objects.filter(user=buyer, company=obj.company):
        buyer_share = Shares.objects.filter(user=buyer, company=obj.company)
        buyer_share = buyer_share[0]
        buyer_share.shares_count += obj.shares_count
    else:
        buyer_share = Shares(company=obj.company, user=buyer,
                             shares_count=obj.shares_count)
    try:
        obj.status = "Success"
        obj.save()
        buyer.save()
        seller.save()
        seller_share.save()
        buyer_share.save()
    except Exception as e:
        raise e


@login_required
def simulateTransaction(request, id):
    obj = get_object_or_404(Transaction, id=id)
    try:
        makepayment(request, id)
        messages.success(request, "Payment Successfully Completed")
    except Exception as e:
        obj.status = "Failed"
        obj.total_amount = 0
        obj.save()
        messages.error(request, "Error: " + str(e))
    return myShares(request)


@login_required
def myTransactions(request):
    return myTransactionsView.as_view()(request)


class myTransactionsView(generic.ListView):
    model = Transaction
    context_object_name = 'my_transactions_list'
    template_name = "my_transactions.html"

    def get_queryset(self):
        get_as_seller = Transaction.objects.filter(seller=self.request.user)
        get_as_buyer = Transaction.objects.filter(buyer=self.request.user)
        get_transactions = get_as_buyer | get_as_seller
        get_transactions = get_transactions.order_by('-time')
        return get_transactions

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


@login_required
def buyShares(request, id):
    obj = get_object_or_404(Shares, id=id)
    new_transaction = Transaction(seller=obj.user, buyer=request.user,
                                  status='Pending', company=obj.company, cost_price=obj.company.selling_price)
    curr_balance = request.user.balance
    if curr_balance < obj.company.selling_price:
        messages.error(
            request, "You Don't Have Enough Balance!")
        return MarketView.as_view()(request)
    new_transaction.save()
    return startTransaction(request, new_transaction.id)


@login_required
def editCompanyShares(request, id):
    obj = get_object_or_404(Shares, id=id)
    form = CompanySharesUpdateForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save(commit=True)
        return redirect(myCompanies)
    form = CompanySharesUpdateForm(
        initial={'shares_count': obj.shares_count, 'price': obj.company.selling_price})
    return render(request, 'registration/gen_form.html', {"form": form, "head": 'Edit Company Shares', "redirect": 'edit_shares', "id": id})


@login_required
def sellMyShares(request, id):
    obj = get_object_or_404(Shares, id=id)
    form = SharesSaleUpdateForm(request.POST or None, instance=obj)
    if form.is_valid() and obj.shares_count >= obj.shares_sale:
        form.save(commit=True)
        return redirect(myShares)
    form = SharesSaleUpdateForm(initial={'shares_sale': obj.shares_sale})
    if obj.shares_count < obj.shares_sale:
        messages.error(request, "Your currently own {0} shares. The sale value cannot exceed it".format(
            obj.shares_count))
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


class myWishListView(generic.ListView):
    model = WishList
    context_object_name = 'my_wish_list'
    template_name = 'my_wishlist.html'

    def get_queryset(self):
        obj = WishList.objects.filter(buyer=self.request.user)
        return obj


@login_required
def myWishList(request):
    return myWishListView.as_view()(request)


@login_required
def addToWishList(request, id):
    shares_obj = Shares.objects.get(id=id)
    queryset = WishList.objects.filter(buyer=request.user, share=shares_obj)
    if len(queryset) > 0:
        messages.error(request, "This share already exists in your wishlist")
    else:
        wish = WishList(share=shares_obj, buyer=request.user)
        wish.save()
        messages.success(request, "Successfully added share to your WishList")
    # This redirects it to the same page
    return redirect(request.META['HTTP_REFERER'])


@login_required
def removeFromWishList(request, id):
    shares_obj = Shares.objects.get(id=id)
    queryset = WishList.objects.filter(buyer=request.user, share=shares_obj)
    if len(queryset) == 0:
        messages.error(request, "No such wish found in your wishlist")
    else:
        instance = WishList.objects.get(buyer=request.user, share=shares_obj)
        instance.delete()
    # This redirects it to the same page
    return redirect(request.META['HTTP_REFERER'])


def send_testGraphData(request):
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&interval=5min&apikey=demo"

    temp = requests.get(url).json()
    # print(temp.get("Meta Data"))
    stockData = temp.get("Time Series (5min)")
    # print(stockData)
    countLim = 50
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

    print(yData[:countLim])

    # l = random.randint(1,30)
    # x = []
    # y = []
    # for i in range(l):
    # 	x.append(random.randint(1,5))
    # 	y.append(x[-1]**2)

    return JsonResponse({
        "x_axis": xTime[:countLim],
        "y_axis": yData[:countLim],
        "y2_axis": y2Data[:countLim],
        "y3_axis": y3Data[:countLim],
    })


def getCompLiveData(request, compCode, compKey):
    print(compCode, compKey)
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=" + \
        compCode + "&interval=5min&apikey=" + compKey
    print(url)
    temp = requests.get(url).json()
    # print(temp.get("Meta Data"))
    stockData = temp.get("Time Series (5min)")
    # print(stockData)
    countLim = 50
    xData = list(stockData.keys())[:countLim]
    xData.reverse()

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

    # l = random.randint(1,30)
    # x = []
    # y = []
    # for i in range(l):
    # 	x.append(random.randint(1,5))
    # 	y.append(x[-1]**2)

    return JsonResponse({
        "x_axis": xTime[:countLim],
        "y_axis": yData[:countLim],
        "y2_axis": y2Data[:countLim],
        "y3_axis": y3Data[:countLim],
    })


def getCachedCompanyStockData(request, compCode, compKey):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={compCode}&interval=5min&apikey={compKey}"

    needNewLoad = False
    createNewObject = False
    # check data last data instance in db
    cachedResult = CachedStockData.objects.filter(companyCode=compCode)
    currentTime = timezone.now()
    print(currentTime)
    if ((cachedResult.count() == 0) or ((currentTime - cachedResult[0].cacheTime).seconds > 300)):
        needNewLoad = True
        if (cachedResult.count() == 0):
            createNewObject = True

    # if instance timeStamp > 300sec -> load new data
    if needNewLoad:
        print("loading new data")
        temp = requests.get(url).json()
        stockData = temp.get("Time Series (5min)")

        countLim = 50
        xData = list(stockData.keys())[:countLim]
        xData.reverse()

        marketTime = [i.split()[1] for i in xData]

        openPrice = [float(stockData.get(i).get("1. open")) for i in xData]
        highPrice = [float(stockData.get(i).get("2. high")) for i in xData]
        lowPrice = [float(stockData.get(i).get("3. low")) for i in xData]

        # openPrice = [0 for i in xData]
        # highPrice = [0 for i in xData]
        # lowPrice = [0 for i in xData]

        # save loaded data
        if (createNewObject == True):
            print("Printing New Response")
            for i in range(countLim):
                newStockVal = CachedStockData(
                    cacheTime=currentTime, companyCode=compCode, marketTime=marketTime[i],
                    openPrice=openPrice[i], highPrice=highPrice[i], lowPrice=lowPrice[i]
                )
                newStockVal.save()
        else:
            print("Printing newly Cached Response")
            for i in range(countLim):
                tempObj = cachedResult[i]
                tempObj.cacheTime = currentTime
                tempObj.companyCode = compCode
                tempObj.marketTime = marketTime[i]
                tempObj.openPrice = openPrice[i]
                tempObj.highPrice = highPrice[i]
                tempObj.lowPrice = lowPrice[i]
                tempObj.save()
                # print(marketTime[i],openPrice[i],highPrice[i],lowPrice[i])

    # return json response from models in db
    cachedResult = CachedStockData.objects.filter(companyCode=compCode)

    return JsonResponse({
        "x_axis": [item.marketTime for item in cachedResult],
        "y_axis": [item.openPrice for item in cachedResult],
        "y2_axis": [item.highPrice for item in cachedResult],
        "y3_axis": [item.lowPrice for item in cachedResult],
    })


def exploreCompany(request):
    allCompany = Company.objects.all()
    return render(
        request=request,
        template_name='exploreCompany.html',
        context={"company_list": allCompany}
    )

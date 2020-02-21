from django.shortcuts import render
import random, requests
from django.http import JsonResponse

# Create your views here.

def welcomePage(request):
	return render(
		request = request,
		template_name = 'homepage.html',
		context = {}
	)

def companyPage(request):
	return render(
		request = request,
		template_name = 'company.html',
		context = {}
	)

def userPage(request):
	return render(
		request = request,
		template_name = 'userDetail.html',
		context = {}
	)

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
		"x_axis" : xTime[:10],
		"y_axis" : yData[:10]
	})
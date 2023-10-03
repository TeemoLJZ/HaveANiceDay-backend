from django.shortcuts import render,HttpResponse
from common.models import Customer
from django.http import JsonResponse
import json

# Create your views here.
def Index(request):
    return HttpResponse('Hello World!')


def Index2(request):
    return HttpResponse('Hello World!33333')  

def listcustomers(request):
    qs = Customer.objects.values()
    retStr = ''
    for customer in qs:
        for name, value in customer.items():
            retStr += f'{name}:{value}|'
        retStr += '<br>'
    return HttpResponse(retStr)

def CustomersAdd(request):
    Customer.objects.create(name="杨丞琳",phone="12345688",address="ChinaTaiwan")
    return HttpResponse("Success")

def ShowCustomers(request):
    data= Customer.objects.values()
    jsonlist = list(data)
    # for customer in data:
    #     print(customer.id,customer.name,customer.phone,customer.address)
    # return HttpResponse("Success")
    return JsonResponse({'ret':0,'retlist':jsonlist})

def deleteCustomers(request):
    Customer.objects.filter(id=6).delete()
    # return HttpResponse("success")
    return JsonResponse({'ret':0,'msg':'success'})
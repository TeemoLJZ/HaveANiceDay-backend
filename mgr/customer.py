from django.shortcuts import render,HttpResponse
from common.models import Customer
from django.http import JsonResponse
from lib.handler import dispatcherBase
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage
import sys, traceback
import json

########dispathcer代码优化前###############
# def dispatcher(request):
#     #对用户调用接口的操作进行权限判断
#     if 'usertype' not in request.session:
#         return JsonResponse({
#             'ret':302,
#             'msg':'未登录'
#         },
#             status=302)

#     if request.session['usertype']!='mgr':
#         return JsonResponse({
#             'ret':302,
#             'msg':'未登录'
#         },
#             status = 302)
#     # 将请求参数统一放入request 的 params 属性中，方便后续处理

#     # GET请求 参数在url中，同过request 对象的 GET属性获取
#     if request.method == 'GET':
#         request.params = request.GET

#     # POST/PUT/DELETE 请求 参数 从 request 对象的 body 属性中获取
#     elif request.method in ['POST','PUT','DELETE']:
#         # 根据接口，POST/PUT/DELETE 请求的消息体都是 json格式
#         request.params = json.loads(request.body)


#     # 根据不同的action分派给不同的函数进行处理
#     action = request.params['action']
#     if action == 'list_customer':
#         return listcustomers(request)
#     elif action == 'add_customer':
#         return addcustomer(request)
#     elif action == 'modify_customer':
#         return modifycustomer(request)
#     elif action == 'del_customer':
#         return deletecustomer(request)

#     else:
#         return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})
################优化前结束#####################


def listcustomers(request):
      # 返回一个 QuerySet 对象 ，包含所有的表记录
    try:
        qs = Customer.objects.values().order_by('-id')
        keywords = request.params.get("keywords",None)
        if keywords:
            conditions = [Q(name__contains = one) for one in keywords if one]
            query = Q()
            for condition in conditions:
                query &= condition
            qs = qs.filter(query)
        pagesize = request.params["pagesize"]
        pagenum = request.params["pagenum"]
        pgne = Paginator(qs,pagesize)
        page = pgne.page(pagenum)
        retlist = list(page)
        return JsonResponse({'ret': 0, 'retlist': retlist,'total':pgne.count})
    except EmptyPage:
        return JsonResponse({'ret':0,'retlist':[],'total':0})
    except:
        return JsonResponse({'ret': 2,  'msg': f'未知错误\n{traceback.format_exc()}'})


def addcustomer(request):
  
    info    = request.params['data']
    ### 从请求消息中 获取要添加客户的信息
    ### 并且插入到数据库中
    #### 返回值 就是对应插入记录的对象 
    record = Customer.objects.create(name=info['name'],phone=info['phone'],address=info['address'])
    return JsonResponse({'ret': 0,'id':record.id})

def modifycustomer(request):
  
    # 从请求消息中 获取修改客户的信息
    # 找到该客户，并且进行修改操作
    
    customerid = request.params['id']
    newdata    = request.params['newdata']

    try:
        # 根据 id 从数据库中找到相应的客户记录
        customer = Customer.objects.get(id=customerid)
    except Customer.DoesNotExist:
        return  {
                'ret': 1,
                'msg': f'id 为`{customerid}`的客户不存在'
        }


    if 'name' in  newdata:
        customer.name = newdata['name']
    if 'phone' in  newdata:
        customer.phone = newdata['phone']
    if 'address' in  newdata:
        customer.address = newdata['address']

    # 注意，一定要执行save才能将修改信息保存到数据库
    customer.save()

    return JsonResponse({'ret': 0})

def deletecustomer(request):
  
    customerid = request.params['id']

    try:
        # 根据 id 从数据库中找到相应的客户记录
        customer = Customer.objects.get(id=customerid)
    except Customer.DoesNotExist:
        return  {
                'ret': 1,
                'msg': f'id 为`{customerid}`的客户不存在'
        }

    # delete 方法就将该记录从数据库中删除了
    customer.delete()

    return JsonResponse({'ret': 0})

################ dispatcher代码优化后 ############   
action2Handler ={
    'list_customer': listcustomers,
    'add_customer' : addcustomer,
    'modify_customer': modifycustomer,
    'del_customer': deletecustomer,
}
def dispatcher(request):
    return dispatcherBase(request,action2Handler)
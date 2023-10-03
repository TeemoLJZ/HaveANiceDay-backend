from common.models import Order,OrderMedicine
from django.http import JsonResponse
from django.db import transaction
from django.db.models import F
import json
from lib.handler import dispatcherBase

    
def listorder(request):
  qs = Order.objects.\
    annotate(
      customer_name = F('customer__name'),
      medicine_name = F('medicine__name')
  )\
    .values('id','name','createdate','customer_name','medicine_name')
  retlist = list(qs)
  
  newlist= []
  id2order = {}
  for one in retlist:
    orderid = one['id']
    if orderid not in id2order:
      newlist.append(one)
      id2order[orderid] = one
    else:
      id2order[orderid]['medicine_name'] += '|' + one['medicine_name']
    
  return JsonResponse({"ret":"0","retlist":newlist})


def addorder(request):
  
    info  = request.params['data']

    # 从请求消息中 获取要添加订单的信息
    # 并且插入到数据库中

    
    with transaction.atomic():
        new_order = Order.objects.create(name=info['name'] ,
                                         customer_id=info['customerid'])

        batch = [OrderMedicine(order_id=new_order.id,medicine_id=mid,amount=1)  
                    for mid in info['medicineids']]

        #  在多对多关系表中 添加了 多条关联记录
        OrderMedicine.objects.bulk_create(batch)


    return JsonResponse({'ret': 0,'id':new_order.id})

action2Handler ={
    'list_order': listorder,
    'add_order' : addorder,
}
def dispatcher(request):
    return dispatcherBase(request,action2Handler)
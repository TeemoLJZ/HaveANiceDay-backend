from common.models import Medicine
from django.http import JsonResponse
from lib.handler import dispatcherBase
from django.core.paginator import Paginator
from django.db.models import Q
from django_redis import get_redis_connection
from BKHelloWorld import settings
import json

rconn = get_redis_connection("default")

def listmedicine(request):
      # 返回一个 QuerySet 对象 ，包含所有的表记录
    qs = Medicine.objects.values().order_by('-id')
    keywords = request.params.get('keywords',None)
    pagesize = request.params['pagesize']
    pagenumber = request.params['pagenum']

    # 定义cachefield作为redis中存储搜索结果的key
    cacheField = f'{pagesize}|{pagenumber}|{keywords}'
    # 从redis的MedineList的cachefield中获取结果
    caheObj = rconn.hget(settings.CK.MedineList,cacheField)

    # 如果存在缓存结果，则将结果存在retobj中在后续的代码中直接返回
    if caheObj:
        print("cache stores")
        retObj = json.loads(caheObj)
    
    # 如果不存在缓存结果，就根据关键字在数据库中进行查询
    else:
        print("cache did not stored")
        if keywords:
            conditions = [Q(name__contains=one)for one in keywords.split(' ') if one]
            query =Q()
            for condition in conditions:
                query &= condition
            qs=qs.filter(query)
  
        pgnt = Paginator(qs,pagesize)
        page = pgnt.page(pagenumber)

        retlist =list(page)
        retObj = {'ret': 0, 'retlist': retlist, 'total':pgnt.count}

        # 把结果存到redis中，下次可以直接返回redis中的结果
        rconn.hset(settings.CK.MedineList,cacheField,json.dumps(retObj))
        # 将 QuerySet 对象 转化为 list 类型
        # 否则不能 被 转化为 JSON 字符串
    return JsonResponse(retObj)

def addmedicine(request):
  
    info    = request.params['data']
    ### 从请求消息中 获取要添加客户的信息
    ### 并且插入到数据库中
    #### 返回值 就是对应插入记录的对象 
    record = Medicine.objects.create(name=info['name'],sn=info['sn'],dec=info['dec'])
    rconn.delet(settings.CK.Medine)
    return JsonResponse({'ret': 0,'id':record.id})

def modifymedicine(request):
  
    # 从请求消息中 获取修改客户的信息
    # 找到该客户，并且进行修改操作
    
    medicineid = request.params['id']
    newdata    = request.params['newdata']

    try:
        # 根据 id 从数据库中找到相应的客户记录
        medicine = Medicine.objects.get(id=medicineid)
    except Medicine.DoesNotExist:
        return  {
                'ret': 1,
                'msg': f'id 为`{medicineid}`的客户不存在'
        }


    if 'name' in  newdata:
        medicine.name = newdata['name']
    if 'sn' in  newdata:
        medicine.sn = newdata['sn']
    if 'dec' in  newdata:
        medicine.dec = newdata['dec']

    # 注意，一定要执行save才能将修改信息保存到数据库
    medicine.save()
    rconn.delet(settings.CK.Medine)
    return JsonResponse({'ret': 0})

def deletemedicine(request):
  
    medicineid = request.params['id']

    try:
        # 根据 id 从数据库中找到相应的客户记录
        medicine = Medicine.objects.get(id=medicineid)
    except Medicine.DoesNotExist:
        return  {
                'ret': 1,
                'msg': f'id 为`{medicineid}`的客户不存在'
        }

    # delete 方法就将该记录从数据库中删除了
    medicine.delete()
    rconn.delet(settings.CK.Medine)
    return JsonResponse({'ret': 0})

action2Handler ={
    'list_medicine': listmedicine,
    'add_medicine' : addmedicine,
    'modify_medicine': modifymedicine,
    'del_medicine': deletemedicine,
}
def dispatcher(request):
    return dispatcherBase(request,action2Handler)
from common.models import IlluPic
from common.models import Illustration
from django.http import JsonResponse
from django.core.paginator import Paginator,EmptyPage
from django.db.models import Q

from lib.handler import dispatcherBase
from datetime import datetime
from random import randint

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from BKHelloWorld.local_settings import TENCENTCOS_STORAGE
# from django_cos_storage.storage import TencentCOSStorage
# from functools import wraps

# 腾讯云cos相关配置
secret_id = TENCENTCOS_STORAGE.get('CONFIG').get('SecretId')    # 用户的 SecretId，建议使用子账号密钥，授权遵循最小权限指引，降低使用风险。子账号密钥获取可参见 https://cloud.tencent.com/document/product/598/37140
secret_key = TENCENTCOS_STORAGE.get('CONFIG').get('SecretKey')  # 用户的 SecretKey，建议使用子账号密钥，授权遵循最小权限指引，降低使用风险。子账号密钥获取可参见 https://cloud.tencent.com/document/product/598/37140
region =  TENCENTCOS_STORAGE.get('CONFIG').get('Region')     # 替换为用户的 region，已创建桶归属的 region 可以在控制台查看，https://console.cloud.tencent.com/cos5/bucket
                           # COS 支持的所有 region 列表参见 https://cloud.tencent.com/document/product/436/6224
token = None               # 如果使用永久密钥不需要填入 token，如果使用临时密钥需要填入，临时密钥生成和使用指引参见 https://cloud.tencent.com/document/product/436/14048
scheme = 'https'  

config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
client = CosS3Client(config)

# 普通上传至本地文件，已弃用
def uploadhandler(request):
    if request.method == 'POST':
      uploadfile = request.FILES['upload1']
      filetype = uploadfile.name.split('.')[-1]
      if filetype not in ["jpeg",'png']:
         return JsonResponse({'ret':430, 'msg':'文件格式错误'},)
      if uploadfile.size > 10*1024*1024:
         return JsonResponse({'ret':431,'msg':'文件过大'})
      
      suffix = datetime.now().strftime('%y%m%d%h%m%s_')+str(randint(0,99999))
      filename = f'{suffix}.{filetype}'

      record = IlluPic.objects.create(
      picname=filename,
      illu=uploadfile,
      )

      return JsonResponse({'ret': 0,'recordid':record.picid})

# 腾讯云对象存储的图片上传，暂时不采用这种方案
def uploadIllu(request):
      if request.method == 'POST':
         uploadfile = request.FILES['upload1']
         filetype = uploadfile.name.split('.')[-1]
         if filetype not in ["jpeg",'png']:
            return JsonResponse({'ret':430, 'msg':'文件格式错误'},)
         if uploadfile.size > 10*1024*1024:
            return JsonResponse({'ret':431,'msg':'文件过大'})
      
      suffix = datetime.now().strftime('%y%m%d%h%m%s_')+str(randint(0,99999))
      filename = f'{suffix}.{filetype}'

      client.upload_file_from_buffer(
         Bucket='illustration-1305693432',
         Body=uploadfile,
         Key=f'{filename}',
         PartSize=1,
         MAXThread=10,
         EnableMD5=False
      )

      record = IlluPic.objects.create(
      picname=filename,
      illu=f'https://illustration-1305693432.cos.ap-chengdu.myqcloud.com/{filename}'
      )

      return JsonResponse({'ret': 0,'recordid':record.picid,'recordillu':record.illu})
      

def listillu(request):
   try:
      qs = Illustration.objects.values()
      keywords = request.GET['keywords']
      source = request.GET['source']
      feature = request.GET['feature']
      type = request.GET['type']

      # 根据类型筛选
      if type:
         qs = qs.filter(Q(type__contains=type))

      # 关键字搜索
      if keywords:
         conditions = [Q(name__icontains=one)
                     for one in keywords.split(' ') if one
                     ]
         query =Q()
         for condition in conditions:
            query &= condition
         qs=qs.filter(query)
      
      # 根据来源搜索（多选）
      if source:
         conditions = [Q(source__contains=one)
                     for one in source.split(',') if one]
         query = Q()
         for condition in conditions:
            query |= condition
         qs = qs.filter(query)

      # 根据特点搜索
      if feature:
         qs = qs.filter(Q(feature__contains=feature))
      
      #进行分页
      pagesize = request.GET['pagesize']
      pagenumber = request.GET['pagenum']
      pgnt = Paginator(qs,pagesize)
      page = pgnt.page(pagenumber)
      retlist = list(page)
      return JsonResponse({'ret':0,'retlist':retlist,'total':pgnt.count})
   except EmptyPage:
      return JsonResponse({'ret': 0, 'retlist': [], 'total': 0})

def getilludetail(request):
   id = request.GET['id']
   # targlist = Illustration.objects.values()
   # print(targlist)
   targetlist = Illustration.objects.filter(id=id).values()
   if targetlist.exists():
      retlist = list(targetlist)
      print(retlist)
      return JsonResponse({'ret':0,'retlist':retlist})
   else:
      return JsonResponse({'ret':401,'msg':'id dose not exsits'})

action2Handler = {
   'list_illu':listillu,
   'get_illu_detail':getilludetail
}

def dispatcher(request):
    return dispatcherBase(request,action2Handler)
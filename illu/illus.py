from common.models import IlluPic
from common.models import Illustration
from django.http import JsonResponse
import json
from lib.handler import dispatcherBase
from datetime import datetime
from random import randint


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
    

def listillu(request):
   qs = Illustration.objects.values()
   retlist = list(qs)
   return JsonResponse({'ret':0,'retlist':retlist})

action2Handler = {
   'list_illu':listillu
}

def dispatcher(request):
    return dispatcherBase(request,action2Handler)
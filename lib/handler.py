from django.http import JsonResponse
import json

def dispatcherBase(request,action2Table):
  if 'usertype' not in request.session:
        return JsonResponse({
            'ret':302,
            'msg':'未登录'
        },
            status=302)

  if request.session['usertype']!='mgr':
      return JsonResponse({
            'ret':302,
            'msg':'未登录'
        },
            status = 302)
    # 将请求参数统一放入request 的 params 属性中，方便后续处理

    # GET请求 参数在url中，同过request 对象的 GET属性获取
  if request.method == 'GET':
        request.params = request.GET

    # POST/PUT/DELETE 请求 参数 从 request 对象的 body 属性中获取
  elif request.method in ['POST','PUT','DELETE']:
        # 根据接口，POST/PUT/DELETE 请求的消息体都是 json格式
        request.params = json.loads(request.body)
  
  action = request.params['action']
  if action in action2Table:
    handlerfunc = action2Table[action]
    return handlerfunc(request)
  
  else:
    return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})


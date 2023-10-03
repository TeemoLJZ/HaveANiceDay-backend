import  requests,pprint

response = requests.get('http://127.0.0.1:8000/api/mgr/customers?action=list_customer')

pprint.pprint(response.json())

payload = {
    "action":"add_customer",
    "data":{
        "name":"武汉市桥西医院",
        "phone":"13345679934",
        "address":"武汉市桥西医院北路"
    }
}
# 发送请求给web服务
response = requests.post('http://127.0.0.1:8000/api/mgr/customers/',
              json=payload)
pprint.pprint(response.json())    

# 构建查看 客户信息的消息体
response = requests.get('http://127.0.0.1:8000/api/mgr/customers?action=list_customer')

# 发送请求给web服务
pprint.pprint(response.json())
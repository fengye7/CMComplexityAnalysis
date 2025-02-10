import requests
import json

# 设置中转服务的基本URL和API密钥
Baseurl = "https://api.claudeshop.top"
Skey = "sk-Ypf4WUIqVKt8tFbglB4YASiIuo0vYWuLPY5Dx6bpZm7esOio"

# 构建请求的有效载荷
payload = json.dumps({
   "model": "gpt-4o",
   "messages": [
      {
         "role": "system",
         "content": "You are a helpful assistant."
      },
      {
         "role": "user",
         "content": '''
         {
         "AI系统": [
           {
             "system": "AI数字人形象系统",
             "services": [
               {
                 "id": "service_1",
                 "name": "Service_1",
                 "interfaces": [
                   {
                     "id": "interface_1",
                     "name": "Interface_1"
                   },
                   {
                     "id": "interface_2",
                     "name": "Interface_2"
                   }
                 ]
               },
               {
                 "id": "service_2",
                 "name": "Service_2",
                 "interfaces": [
                   {
                     "id": "interface_3",
                     "name": "Interface_3"
                   },
                   {
                     "id": "interface_4",
                     "name": "Interface_4"
                   },
                   {
                     "id": "interface_5",
                     "name": "Interface_5"
                   }
                 ]
               }
             ]
           },
           {
             "system": "AI数字分身形象系统",
             "services": [
               {
                 "id": "service_3",
                 "name": "Service_3",
                 "interfaces": [
                   {
                     "id": "interface_6",
                     "name": "Interface_6"
                   }
                 ]
               },
               {
                 "id": "service_4",
                 "name": "Service_4",
                 "interfaces": [
                   {
                     "id": "interface_7",
                     "name": "Interface_7"
                   },
                   {
                     "id": "interface_8",
                     "name": "Interface_8"
                   }
                 ]
               }
             ]
           },
           {
             "system": "AI马良智能绘图系统",
             "services": [
               {
                 "id": "service_5",
                 "name": "Service_5",
                 "interfaces": [
                   {
                     "id": "interface_9",
                     "name": "Interface_9"
                   },
                   {
                     "id": "interface_10",
                     "name": "Interface_10"
                   },
                   {
                     "id": "interface_11",
                     "name": "Interface_11"
                   },
                   {
                     "id": "interface_12",
                     "name": "Interface_12"
                   },
                   {
                     "id": "interface_13",
                     "name": "Interface_13"
                   }
                 ]
               }
             ]
           }
         ],

         根据上面的系统结构的mock数据，接下来我要给出变更工单mock数据的条件，请你配合我完成我的mock数据工作：

         变更历史数据应该符合以下条件：（相关描述信息都是中文）
         1. 有变更id，变更标题（这个标题是有意义的描述性信息）
         2.  变更事由/变更目标 
         3. 变更系统（和上面给出的系统结构mock数据对应关联）
         4. 变更分类（eg:应用系统软件变更）
         5. 需求/story编号（变更和需求、story对应相关）（这部分也需要mock数据）
         6. 变更需求类型（对应需求的类别）
         7. 影响到的其它系统（不一定有）
         8. 变更文件（可能为空）

         你可以看到上面信息还是挺多的，我们一步一步来，先生成需要的需求-story mock数据：
         需求1对多个story，（变更一对1到多个story）
         eg:
         需求-Story Mock 数据
         requirement_id	requirement_name	story_id	story_name	是否重大需求	所属系统
         R20231001	AI数字人形象系统的图像处理优化	S202310011	图像上传接口优化	是	AI数字人形象系统
         R20231001	AI数字人形象系统的图像处理优化	S202310012	图像渲染性能提升	否	AI数字人形象系统
         R20231002	CMDB系统的资源监控增强	S202310021	资源使用查询接口增加实时监控	是	CMDB系统
         R20231002	CMDB系统的资源监控增强	S202310022	资源告警系统优化	否	CMDB系统
         R20231003	DMP营销管理系统的数据分析模块扩展	S202310031	用户画像分析功能拓展	是	DMP营销管理系统
         R20231004	DataStage数据交换系统的安全性提升	S202310041	数据导入接口增加安全验证	是	DataStage数据交换系统
         R20231004	DataStage数据交换系统的安全性提升	S202310042	数据导出接口添加审计日志	否	DataStage数据交换系统
         R20231005	ETF奖利平台的奖励计算规则优化	S202310051	奖励规则配置界面优化	是	ETF奖利平台
         R20231005	ETF奖利平台的奖励计算规则优化	S202310052	奖励计算接口提升计算性能	否	ETF奖利平台
         R20231006	股票市场动态系统的动态监测功能增强	S202310061	动态监测接口增加异常波动检测	是	股票市场动态系统

         给出参照上面例子的500条mock，可使用csv格式'''
      }
   ]
})

# 构建完整的URL和请求头
url = Baseurl + "/v1/chat/completions"
headers = {
   'Accept': 'application/json',
   'Authorization': f'Bearer {Skey}',
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
   'Content-Type': 'application/json'
}

# 发起 POST 请求
response = requests.post(url, headers=headers, data=payload)

# 解析返回的 JSON 数据
data = response.json()

# 获取 content 字段的值并打印
content = data.get('choices', [{}])[0].get('message', {}).get('content', '')
print("返回的结果：",content)

# import requests
# import json

# # 使用中转链接
# Baseurl = "https://api.claudeshop.top"
# Skey = "sk-Ypf4WUIqVKt8tFbglB4YASiIuo0vYWuLPY5Dx6bpZm7esOio"

# # 输入文本数据
# input_text = "Hello, world!"

# # 请求 payload 数据
# payload = json.dumps({
#    "model": "text-embedding-ada-002",  # 使用适当的模型名称
#    "input": input_text
# })

# # 构建请求的 URL
# url = Baseurl + "/v1/embeddings"

# # 设置请求头
# headers = {
#    'Accept': 'application/json',
#    'Authorization': f'Bearer {Skey}',
#    'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
#    'Content-Type': 'application/json'
# }

# # 发送 POST 请求
# response = requests.request("POST", url, headers=headers, data=payload)

# # 解析 JSON 数据为 Python 字典
# data = response.json()

# # 获取嵌入结果
# embedding = data.get('data', [])[0].get('embedding', [])

# print(embedding)
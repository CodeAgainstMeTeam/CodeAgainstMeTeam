'''
author:朱一凡
create time:2020-07-16
update time:2020-07-18
'''

# encoding:utf-8
import requests

#获取车辆检测access_token
# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=axVzDpA1g77MmslGiBOCAkIg&client_secret=EujHlAm7SDnphcGZX8DO4jU09e1tHTov'
response = requests.get(host)
if response:
    print(response.json())

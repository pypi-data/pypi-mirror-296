import argparse
from sj_util.helpers.utils import write_log

def create_admin_user(username):
    pass

def create_xog_user(username):
    pass

def create_user(username):
    request_body={
    {"lastName": "test",
"timezone":"Asia/Calcutta",
"description":"Test user created via REST API integration",
"language":"1",
"locale":"en_US",
"forcePwdChange":"false",
"email":"test@restapi.com",
"resourceName":"test02",
"userName":"test02",
"firstName":"test02",
"employmentType":"300",
"status":"200"
}
    }

# import requests
# import json

# url = "http://claritynam.aod.labs.broadcom.net:1622/ppm/rest/v1/users"

# payload = {}
# headers = {
#   'x-api-ppm-client': 'restclient',
#   'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiIsImlzcyI6Imh0dHBzOi8vcHBtLmNhLmNvbSIsImdlbngiOiI1OWI3N2RjYWE1ZmZjZTVhYjlkYTg1YTBmNjVmNGJjOCIsInRlbmFudF9jaGVjayI6InRydWUiLCJleHAiOjE3MzAyNzE2MDAsInVzZXIiOjEsImp0aSI6ImY2Nzc3MDE1LTljYmQtNDQwNS05NWMzLTZiMmVlMjhhZTgzMSIsInRlbmFudCI6ImNsYXJpdHkifQ.mUmYFhu9_3qYbt7L38KAbKmyLGP26OWPvilqZExqdbk',
#   'Content-Type': 'application/json',
#   'Cookie': 'sessionId=5601074__3D03922D-2ACC-4950-8773-699A67336DDA'
# }

# response = requests.request("GET", url, headers=headers, data=payload)

# print(response.text)


import requests
import json
import os
##  环境变量需要 SCKEY   EMAIL_PASSWORD 账号格式为email&password ，多账号为email&password#email&password#email&password   BASE_URL这个是机场地址 比如：https://78cloud.pro，sckey是pushplus的推送token。
requests.packages.urllib3.disable_warnings()
SCKEY = os.environ['JCSCKEY']
EMAIL_PASSWORD = os.environ['JCEMAIL_PASSWORD'] # 用#分隔多个账号密码
BASE_URL = os.environ['JCBASE_URL']

def checkin(email, password, base_url, account_num):
    email = email.split('@')
    email = email[0] + '%40' + email[1]
    session = requests.session()
    session.get(base_url, verify=False)
    login_url = base_url + '/auth/login'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/56.0.2924.87 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }
    post_data = 'email=' + email + '&passwd=' + password + '&code='
    post_data = post_data.encode()
    response = session.post(login_url, post_data, headers=headers, verify=False)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/56.0.2924.87 Safari/537.36',
        'Referer': base_url + '/user'
    }
    response = session.post(base_url + '/user/checkin', headers=headers,
                            verify=False)
    response = json.loads(response.text)
    print(f'账号{account_num}: {response["msg"]}')
    return response['msg']


if __name__ == "__main__":
    account_list = EMAIL_PASSWORD.split('#')  # 多账号用#做分割
    num_accounts = len(account_list)  # 获取账号数量
    result = []
    for i, account in enumerate(account_list):
        email, password = account.split('&')  # 账号格式为 email&password
        result.append(checkin(email, password, BASE_URL, i + 1))
    if SCKEY != '':
        sendurl = 'http://www.pushplus.plus/send?token=' + SCKEY + '&title=机场签到&content=' + '\n'.join(result)
        r = requests.get(url=sendurl)

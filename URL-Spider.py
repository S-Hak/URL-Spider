# /usr/bin/env python3
# _*_ coding:utf-8 _*_

import time
import re
import sys

print("""

      _________.__    .__.____    .____              .____     
     /   _____/|  |__ |__|    |   |    |             |    |    
     \_____  \ |  |  \|  |    |   |    |      ______ |    |    
     /        \|   Y  \  |    |___|    |___  /_____/ |    |___ 
    /_______  /|___|  /__|_______ \_______ \         |_______ \\
            \/      \/           \/       \/                 \/
		    	Url-Spider
		From:https://github.com/ShiLL-L
""")

try:
    import requests
except:
    print("""
[?] not found modle:requests.   
[?] Please： pip install requests
    """)
    sys.exit()


UA = {'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
SCANURL = input("[>] Please enter will scan-url : ")
FRQ_tmp = input("[>] please enter deep(defalt:3): ")

try:
    FRQ = int(FRQ_tmp)
except:
    FRQ = 3

ALL_LIST = []
C40x_LIST = []
C403_LIST = []
OTHER_LIST = []
REPEAT_LIST = []


def scan_url(url):
    """
    1.对传入的URL进行完整化
    2.对传入的URL进行测试是否可用
    :param url:传入用户输入的URL
    :return: 1）url可用将返回完整URL。2）url不可用将返回-1
    """
    # 将url进行完整化
    urls = ''
    if 'http://' in url:
        urls = url
    elif 'https://' in url:
        urls = url
    else:
        urls = 'http://' + url
    # 验证传入的URL是否可用
    try:
        time.sleep(0.2)
        response = requests.get(urls, headers=UA)
        print("[+] Call URL [" + urls + "] >> status: " + str(response.status_code))
        return urls
    except:
        print("[?] [" + urls + "]the URL is not found ---")
        return -1


def cat_url(in_url):
    """
    1.访问传入URL，获取返回包，从中提取可能为URL的字段
    2.对提取的字段进行筛选：
        1）替换字段 &amp; 为 &
        2）将存在 " ' 的字段去除 ' "，其他的直接添加
    获取所有标签的值，输出列表
    :param in_url: 完整的URL
    :return: 网页内全部标签链接的列表
    """
    # 获取所有标签的值，输出列表 out_url
    response = ""
    try:
        time.sleep(0.2)
        response = requests.get(in_url, headers=UA)
    except:
        print("[?] Get the URL out error . url: " + in_url)

    re_sp = r'(?<=.=).*?(?=[\s+|\>])'
    page_tab = re.findall(re_sp, response.text)
    out_url = []
    for i in page_tab:
        if '/' in i:
            aaa = str(i).replace("&amp;", "&")
            out_url.append(aaa)
    # 对out_url 进行整理，去除 " ' 输出到next_outurl
    next_outurl = []
    for i in out_url:
        re_text = r'(?<=[\'|\"]).*?(?=[\'|\"|\s+|\?])'          # 逻辑不完整1)---暂时先去掉所有参数
        page_tab = re.findall(re_text, i)
        def is_url():
            try:
                next_outurl.append(page_tab[0])
            except:
                pass
        if i.startswith("\""):
            is_url()
        elif i.startswith("\'"):
            is_url()
        elif i.startswith("\{"):
            pass
        elif i.startswith("\}"):
            pass
        else:
            next_outurl.append(i)
    return next_outurl


def del_other(url_list):
    '''
    清除干扰项
        1）删除值为 / 的字段
    :param url_list:存储URL列表
    :return:处理后的结果（列表）
    '''
    out_url = []
    for i in url_list:
        if "/" == i:
            continue
        elif i.startswith("/"):
            re_txt = r'(^/[a-z]|\.)'
            url_test1 = re.findall(re_txt, i)
            if url_test1:
                if re.findall(r'(^/[a-z]*[\}|\)])', i):
                    continue
                out_url.append(i)
        else:
            out_url.append(i)
    return out_url


def over_url(url_list, url):
    """
    整理输出的URL，留下可以访问的
    :param url_list: url列表
    :return: 完整的URL列表
    """
    repeat_url = []
    for i in url_list:
        if i.startswith("/"):
            over_url_a = url + i
        else:
            over_url_a = i
        # 判断外链
        if SCANURL in over_url_a:
            pass
        else:
            continue
        # 判断重复和状态，并输入到ALL_LIST
        # ==========================================================================================
        try:
            if over_url_a in repeat_url:
                print("[-] test URL:" + over_url_a + " >> the URL It already exists.")
            elif over_url_a in REPEAT_LIST:
                print("[-] test URL:" + over_url_a + " >> the URL It already exists.")

            else:
                time.sleep(0.2)
                resp = requests.get(over_url_a, headers=UA)
                if str(resp.status_code) == '403':
                    print("[-] test URL:" + over_url_a + " >> status: 403 page not found")
                    C403_LIST.append(over_url_a)
                    REPEAT_LIST.append(over_url_a)
                elif '20' in str(resp.status_code):
                    print("[-] test URL:" + over_url_a + " >> status:" + str(resp.status_code))
                    ALL_LIST.append(over_url_a)
                    REPEAT_LIST.append(over_url_a)
                elif '40' in str(resp.status_code):
                    print("[-] test URL:" + over_url_a + " >> status: 40x page not found")
                    C40x_LIST.append(over_url_a)
                    REPEAT_LIST.append(over_url_a)
                else:
                    print("[+] test URL:" + over_url_a + " >> status:" + str(resp.status_code))
                    OTHER_LIST.append(over_url_a)
                    REPEAT_LIST.append(over_url_a)
        except:
            print("[-] test URL:" + over_url_a + " >> status: URL not found")
            continue
        #==============================================================================================
        repeat_url.append(over_url_a)
    return ALL_LIST


# ---------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------下面是主方法----------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------

def main():
    # url = "39.106.53.56"
    # 完整化URL
    scans = scan_url(SCANURL)
    ALL_LIST.append(scans)
    # 测试URL是否可用
    try:
        time.sleep(0.2)
        requests.get(scans, headers=UA)
    except:
        print("[?] you enter URL >>> ERROR")
        sys.exit()


    ci_next = 0
    k = 0
    # tmp_list = []
    while(k<FRQ):
        k = k + 1
        print("\n" + "-" * 99 + "\n[>] spider " + str(k) + " frequency")
        for i in range(ci_next, len(ALL_LIST)):
            print("[>] Spider URL : " + ALL_LIST[i])
            #------------------------------------
            # 获取网页内所有可能是链接的字段并整理 》》 列表prs_s
            prs_s = cat_url(scans)
            # 删除干扰项
            del_others = del_other(prs_s)
            # 整理输出的URL
            over_url(del_others, scans)



    # 打印
    print("\n\n" + "=" * 99 +"\n[+] ALL status:20x print >>>>")
    for i in ALL_LIST:
        print(i)


if __name__ == '__main__':
    main()

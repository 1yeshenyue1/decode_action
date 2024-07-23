#2024-07-23 16:46:41
"""
* 仅供学习交流，请在下载后的24小时内完全删除 请勿将任何内容用于商业或非法目的，否则后果自负。
* 小阅阅阅读 V2.31

* 活动入口,微信打开：
* 如果连接过期了运行一下就出来了最新的入口！
* http://dcc222334.y43a1.3gn8m.cn/jxybyy/2639bb95daba1d99e5338a8c2e21e2f0?upuid=91
* 打开活动入口，抓包的任意接口cookies中的ysm_uid参数
* 
* 变量格式：
* 新建同名环境变量
* 变量名：xyyyd
* 变量值：
* # 3000 代表 3毛，后面两个推送参数可不填，那就必须配置全局推送！
* 账号备注#ysm_uid参数#提现金额如3000#wxpushApptoken#wxpushTopicId
* 
* 其他参数说明（脚本最下方填写参数）
* wxpusher全局参数：wxpusherAppToken、wxpusherTopicId
* 具体使用方法请看文档地址：https://wxpusher.zjiecode.com/docs/#/
* 
* 也可使用 微信机器人：wechatBussinessKey
* 
* 支持支付宝提现：账号备注#ysm_uid参数#提现金额如3000#wxpushApptoken#wxpushTopicId#支付宝姓名#支付宝账号
* 只想提现支付宝，不想填写其他参数，最少的参数就是：账号备注#ysm_uid参数####支付宝姓名#支付宝账号
*
* 增加 自定义检测文章等待时间：xyyydReadPostDelay，默认值是 15-20秒
* 增加 精简日志：xyyydReadPureLog，默认值是 true（也就是精简日志，如果需要显示完整的，请设置为 false）
* 
* 定时运行每半小时一次
* 达到标准自动提现
* 达到标准，自动提现
"""
onlyDoInviteRewardJob = False
onlyWithdraw = False
withdrawAlipay = False
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import hashlib
import json
import math
import os
import string
import time
import requests
import random
import re
from urllib.parse import quote, urlparse, parse_qs
import urllib3
from urllib.parse import parse_qs, urlsplit
from fake_useragent import UserAgent

urllib3.disable_warnings()

# 填wxpusher的appToken，配置在环境变量里这样没配置的账号会自动使用这个推送
wxpusherAppToken = os.getenv("wxpusherAppToken") or ""
wxpusherTopicId = os.getenv("wxpusherTopicId") or ""
wechatBussinessKey = os.getenv("wechatBussinessKey") or ""
globalHelpAccountUrl = os.getenv("xyyydGlobalHelpAccountUrl") or ""
globalHelpAccountUrlTemplate = os.getenv("xyyydGlobalHelpAccountUrlTemplate") or ""
readPostDelay = 0
if os.getenv("xyyydReadPostDelay") and os.getenv("xyyydReadPostDelay").isdecimal():
    readPostDelay = int(os.getenv("xyyydReadPostDelay"))
readTimeRangeStr = os.getenv("xyyydReadTimeRange") or "[0,23]"
if readTimeRangeStr:
    readTimeRange = json.loads(readTimeRangeStr)
xyyydReadPureLog = True
if os.getenv("xyyydReadPureLog"):
    xyyydReadPureLog = os.getenv("xyyydReadPureLog") == "true"
totalWithdrawAmount = 0
gloablAlipayAccounts = os.getenv("xyyydGloablAlipayAccounts") or ""
# 变量名：xyyydGloablAlipayWithdrawTimeForAccount  变量值：一个全局支付宝对应几个提现账户，比如 2 的话，就是 1-2个账户属于 第一个支付宝，3-4属于第二个
gloablAlipayWithdrawTimeForAccount = os.getenv(
    "xyyydGloablAlipayWithdrawTimeForAccount"
)
if gloablAlipayWithdrawTimeForAccount == None:
    gloablAlipayWithdrawTimeForAccount = 1
else:
    gloablAlipayWithdrawTimeForAccount = int(gloablAlipayWithdrawTimeForAccount)
# 变量名：xyyydGloablAlipayAccounts  变量值：支付宝姓名#支付宝账号，多个全局支付宝提现配置用 , 分割
if gloablAlipayAccounts and "," in gloablAlipayAccounts:
    gloablAlipayAccounts = gloablAlipayAccounts.split(",") or []
else:
    gloablAlipayAccounts = [gloablAlipayAccounts]


def get_random_int(min, max):
    return random.randint(min, max)


def check_file_md5(url, expected_md5):
    # 获取文件内容
    response = requests.get(url)
    data = response.content

    # 计算MD5
    md5 = hashlib.md5()
    md5.update(data)
    calculated_md5 = md5.hexdigest()
    # print("当前文件的MD5值为：", calculated_md5)
    # 比较MD5
    return calculated_md5 == expected_md5


def check_str_md5(str, expected_md5):
    # 计算MD5
    md5 = hashlib.md5()
    md5.update(str.encode("utf-8"))
    calculated_md5 = md5.hexdigest()
    # print("当前内容的MD5值为：", calculated_md5)
    # 比较MD5
    return calculated_md5 == expected_md5


def extract_middle_text(source, before_text, after_text, all_matches=False):
    results = []
    start_index = source.find(before_text)

    while start_index != -1:
        source_after_before_text = source[start_index + len(before_text) :]
        end_index = source_after_before_text.find(after_text)

        if end_index == -1:
            break

        results.append(source_after_before_text[:end_index])
        if not all_matches:
            break

        source = source_after_before_text[end_index + len(after_text) :]
        start_index = source.find(before_text)

    return results if all_matches else results[0] if results else ""


def safe_request(method, url, retries=3, **kwargs):
    for i in range(retries):
        try:
            if method.upper() == "GET":
                response = requests.get(url, **kwargs)
            elif method.upper() == "POST":
                response = requests.post(url, **kwargs)
            else:
                print(f"不支持的请求类型: {method}")
                return None
            return response
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            if i < retries - 1:  # 如果不是最后一次尝试，就等待一段时间再重试
                wait = random.randint(1, 5)  # 随机等待时间
                print(f"等待 {wait} 秒后重试...")
                time.sleep(wait)
            else:
                print("尝试请求失败，已达到最大尝试次数")
                return None  # 或者你可以返回一个特定的值或对象来表示请求失败


def push(appToken, topicIds, title, link, text):
    datapust = {
        "appToken": appToken,
        "content": f"""<body onload="window.location.href='{link}'">出现检测文章！！！\n<a style='padding:10px;color:red;font-size:20px;' href='{link}'>点击我打开待检测文章</a>\n请尽快点击链接完成阅读\n备注：{text}</body>""",
        "summary": title or "小阅阅阅读",
        "contentType": 2,
        "topicIds": [topicIds or "11686"],
        "url": link,
    }
    # print(datapust)
    urlpust = "http://wxpusher.zjiecode.com/api/send/message"
    try:
        p = safe_request("POST", url=urlpust, json=datapust, verify=False)
        # print(p)
        if p.json()["code"] == 1000:
            print("✅ 推送文章到微信成功，请尽快前往点击文章，不然就黑号啦！")
            return True
        else:
            print("❌ 推送文章到微信失败，完犊子，要黑号了！")
            return False
    except Exception as e:
        print("❌ 推送文章到微信失败，完犊子，要黑号了！")
        raise e
        return False


def pushWechatBussiness(robotKey, link):
    datapust = {"msgtype": "text", "text": {"content": link}}
    # print(datapust)
    urlpust = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=" + robotKey
    try:
        p = safe_request("POST", url=urlpust, json=datapust, verify=False)
        # print(p)
        if p.json()["errcode"] == 0:
            print("✅ 推送文章到企业微信成功！")
            return True
        else:
            print("❌ 推送文章到企业微信失败！")
            return False
    except:
        print("❌ 推送文章到企业微信失败！")
        return False


def getPostWechatInfo(link):
    try:
        r = safe_request("GET", link, verify=False)
        # print(link, r.text)
        html = re.sub("\s", "", r.text)
        biz = re.findall('varbiz="(.*?)"\|\|', html)
        if biz != []:
            biz = biz[0]
        if biz == "" or biz == []:
            if "__biz" in link:
                biz = re.findall("__biz=(.*?)&", link)
                if biz != []:
                    biz = biz[0]
        nickname = re.findall('varnickname=htmlDecode\("(.*?)"\);', html)
        if nickname != []:
            nickname = nickname[0]
        user_name = re.findall('varuser_name="(.*?)";', html)
        if user_name != []:
            user_name = user_name[0]
        msg_title = re.findall("varmsg_title='(.*?)'\.html\(", html)
        if msg_title != []:
            msg_title = msg_title[0]
        text = f"公众号唯一标识：{biz}|文章:{msg_title}|作者:{nickname}|账号:{user_name}"
        print(text)
        return nickname, user_name, msg_title, text, biz
    except Exception:
        # print(e)
        print("❌ 提取文章信息失败")
        return False


def trimSpaceCharacters(text):
    return "".join(text.split())


class LinkCache:
    def __init__(self, file_path):
        self.file_path = file_path
        self.cache = self.load_cache()

    def load_cache(self):
        try:
            with open(self.file_path, "r") as f:
                data = json.load(f)
            return data
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_cache(self):
        try:
            with open(self.file_path, "w") as f:
                json.dump(self.cache, f, indent=2)
        except Exception as e:
            print("无法保存链接到本地缓存文件：", e)

    def add_link(self, link, date):
        if link not in self.cache:
            self.cache[link] = {"publishDate": date, "count": 1}
        else:
            self.cache[link]["count"] += 1
        self.save_cache()

    def get_link_info(self, link):
        return self.cache.get(link, None)

    def get_all_links(self):
        return list(self.cache.keys())


link_cache = LinkCache("huansheng_xyy_link_cache.json")


def fetch_wx_time_and_record(url, link_cache):
    max_retries = 3
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; RMX1971 Build/QKQ1.190918.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 XWEB/1160083 MMWEBSDK/20231202 MMWEBID/8342 MicroMessenger/8.0.47.2560(0x28002F51) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64"
    }
    for i in range(max_retries):
        try:
            response = requests.get(url, headers=headers)
            wx = response.text
            wz_time_regex = r"var createTime = '(.*?)';"
            match = re.search(wz_time_regex, wx)
            if match:
                article_time = match.group(1)
                print(f"微信文章发布时间: {article_time}")
                link_info = link_cache.get_link_info(url)
                print(f"该检测文章，已记录了 {link_info['count'] if link_info else 0 + 1} 次")
                link_cache.add_link(url, article_time)
                return True
        except Exception as e:
            print(f"检测微信文章时间发生错误: {e}")
            return True


def ts():
    return str(int(time.time())) + "000"


checkDict = {
    "MzkxNTE3MzQ4MQ==": ["香姐爱旅行", "gh_54a65dc60039"],
    "Mzg5MjM0MDEwNw==": ["我本非凡", "gh_46b076903473"],
    "MzUzODY4NzE2OQ==": ["多肉葡萄2020", "gh_b3d79cd1e1b5"],
    "MzkyMjE3MzYxMg==": ["Youhful", "gh_b3d79cd1e1b5"],
    "MzkxNjMwNDIzOA==": ["少年没有乌托邦3", "gh_b3d79cd1e1b5"],
    "Mzg3NzUxMjc5Mg==": ["星星诺言", "gh_b3d79cd1e1b5"],
    "Mzg4NTcwODE1NA==": ["斑马还没睡123", "gh_b3d79cd1e1b5"],
    "Mzk0ODIxODE4OQ==": ["持家妙招宝典", "gh_b3d79cd1e1b5"],
    "Mzg2NjUyMjI1NA==": ["Lilinng", "gh_b3d79cd1e1b5"],
    "MzIzMDczODg4Mw==": ["有故事的同学Y", "gh_b3d79cd1e1b5"],
    "Mzg5ODUyMzYzMQ==": ["789也不行", "gh_b3d79cd1e1b5"],
    "MzU0NzI5Mjc4OQ==": ["皮蛋瘦肉猪", "gh_58d7ee593b86"],
    "Mzg5MDgxODAzMg==": ["北北小助手", "gh_58d7ee593b86"],
    "MzIzMDczODg4Mw==": ["有故事的同学Y", "gh_b8b92934da5f"],
    "MzkxNDU1NDEzNw==": ["小阅阅服务", "gh_e50cfefef9e5"],
    "MzkxNDYzOTEyMw==": ["蓝莓可乐", "gh_73ca238add97"],
    "MzkzNTYxOTgyMA==": ["韭菜炒鱿鱼", "gh_c131c3ee1187"],
    "MzkxNDYzOTEyMw==": ["蓝莓可乐", "gh_73ca238add97"],
    "MzkwMTYwNzcwMw==": ["艾克里鸭", "gh_77acafd552da"],
    "MzU5MzgzMzE4Ng==": ["未知", "没记录"],
    "MzUzODY4NzE2OQ==": ["未知", "没记录"],
    "MzkxNDYzOTEyMw==": ["未知", "没记录"],
    "MzkyNjY0MTExOA==": ["未知", "没记录"],
    "MzkwNzYwNDYyMQ==": ["未知", "没记录"],
    "MzkxNjMwNDIzOA==": ["未知", "没记录"],
    "Mzg4NTcwODE1NA==": ["未知", "没记录"],
    "MzkzMTYyMDU0OQ==": ["未知", "没记录"],
    "MzkyMjE3MzYxMg==": ["未知", "没记录"],
    "MzkwMTYwNzcwMw==": ["未知", "没记录"],
    "MzkwNDUwMTk3NA==": ["未知", "没记录"],
    "MzkyMjYxNzQ2NA==": ["九点准时睡9点", "gh_48fda2f8936c"],
    "MzkyNjY0MTExOA==": ["未知", "没记录"],
    "MzkzNDYxODY5OA==": ["没有星期8", "gh_9143bf676245"],
    "Mzg5MDgxODAzMg==": ["未知", "没记录"],
    "MzkxNDU1NDEzNw==": ["未知", "没记录"],
    "MzkzNTYxOTgyMA==": ["未知", "没记录"],
}


def follow_redirect(url, max_redirects=None, stop_on=None, **kwargs):
    redirects = 0
    response = None
    try:
        response = requests.get(url, **kwargs)
        # print("返回：", url, response.text, response.headers)
        if max_redirects is not None and redirects >= max_redirects:
            return response.headers, response.content
        if stop_on is not None and stop_on in url:
            return response.headers, response.content
        if not 300 <= response.status_code < 400:
            return response.headers, response.content
        url = response.headers.get("Location", url)
        # if stop_on is not None and stop_on in url:
        #     return response.headers, response.content
        redirects += 1
        return follow_redirect(url, max_redirects, stop_on, **kwargs)
    except (requests.exceptions.RequestException, KeyError):
        return response.headers, response.content


# 设置代理地址和端口
proxies = None
if os.getenv("xyyHttpProxyUrl"):
    proxies = {
        "http": os.getenv("xyyHttpProxyUrl"),
        "https": os.getenv("xyyHttpProxyUrl"),
    }


class HHYD:
    def __init__(self, cg):
        self.isBindAliAccount = False
        self.balance = 0
        self.unionId = cg.get("unionId", None)
        self.ysm_uid = cg["ysm_uid"].replace("ysm_uid=", "").replace("ysmuid=", "")
        # print("cg", cg, self.unionId, self.ysm_uid)
        self.txbz = cg["txbz"]
        self.topicIds = cg["topicIds"]
        self.appToken = cg["appToken"]
        global wechatBussinessKey
        self.wechatBussinessKey = wechatBussinessKey or ""
        self.aliAccount = cg["aliAccount"] or ""
        self.aliName = cg["aliName"] or ""
        self.name = cg["name"]
        self.domnainHost = "1698855139.hxiong.top"
        self.exchangeParams = ""
        wechat_ua_list = [
            " MicroMessenger/8.0.{随机小版本号}.25{随机补丁版本号}({随机标识}) WeChat/arm64 Weixin NetType/5G Language/zh_CN ABI/arm64 MiniProgramEnv/android",
            " MicroMessenger/8.0.{随机小版本号}.25{随机补丁版本号}({随机标识}) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android",
        ]
        self.signModule = False
        random_wechat_after_sign_str = (
            random.choice(wechat_ua_list)
            .replace("{随机标识}", format(get_random_int(0x00000000, 0xFFFFFFFF), "08x"))
            .replace("{随机小版本号}", str(random.randint(41, 48)))
            .replace("{随机补丁版本号}", str(random.randint(60, 80)))
        )

        user_agent = UserAgent().random + random_wechat_after_sign_str
        self.headers = {
            "Connection": "keep-alive",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "User-Agent": user_agent
            or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090621) XWEB/8351 Flue",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": f"http://{self.domnainHost}/",
            "Origin": f"http://{self.domnainHost}",
            # "Host": f"{self.domnainHost}",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": f"ysm_uid={self.ysm_uid}; ysmuid={self.ysm_uid};",
        }
        self.readJumpPath = ""
        self.helpAccountUrl = cg["helpAccountUrl"] or ""
        if self.helpAccountUrl:
            if self.helpAccountUrl.startswith("http://") == False:
                if globalHelpAccountUrlTemplate:
                    self.helpAccountUrl = globalHelpAccountUrlTemplate.replace(
                        "$helpCode", self.helpAccountUrl
                    )
                else:
                    self.helpAccountUrl = f"http://api.3ulbs.shop/yunonline/v1/auth/{self.helpAccountUrl}?cate=1&codeurl=%24domain"
        self.helpAccountCode = extract_middle_text(self.helpAccountUrl, "auth/", "?")
        self.helpAccountUrlBak = self.helpAccountUrl
        if self.helpAccountCode:
            self.helpAccountUrlBak = (
                f"http://{self.domnainHost}?cate=1&cid={self.helpAccountCode}"
            )
        self.getHelpCode = ""
        self.readApiVersion = "8.0"
        self.addGoldPath = ""
        self.getReadUrlPath = ""
        # print(self.helpAccountUrl, self.helpAccountUrlBak, self.helpAccountCode)

    def user_info(self):
        u = f"http://{self.domnainHost}/yunonline/v1/sign_info?time={ts()}&unionid={self.unionId}"
        r = ""
        try:
            r = safe_request("GET", u)
            rj = r.json()
            if rj.get("errcode") == 0:
                print(
                    f"账号[{self.name}]获取信息成功，当前阅读文章每篇奖励 {r.json()['data']['award']}个金币"
                )
                return True
            else:
                print(f"账号[{self.name}]获取用户信息失败，账号异常 或者 ysm_uid无效，请检测ysm_uid是否正确")
                return False
        except Exception:
            print(r.text)
            print(f"账号[{self.name}]获取用户信息失败,ysm_uid无效，请检测ysm_uid是否正确")
            return False

    def hasWechat(self):
        r = ""
        try:
            u = f"http://{self.domnainHost}/yunonline/v1/hasWechat?unionid={self.unionId}"
            r = safe_request("GET", u)
            print(f"账号[{self.name}]判断公众号任务数量：{r.json()['data']['has']}")
        except Exception:
            print(f"账号[{self.name}]判断是否有公众号任务失败：{r.text}")
            return False

    def sign_in(self):
        r = ""
        try:
            u = f"http://{self.domnainHost}/yunonline/v1/sign_in"
            data = f"unionid={self.unionId}"
            r = safe_request("POST", u, headers=self.headers, data=data)
            print(f"账号[{self.name}]签到成功，获得：{r.json()['data']['award'] or 0}金币")
        except Exception:
            print(f"账号[{self.name}]签到失败：{r.text}")
            return False

    def sign_info(self):
        r = ""
        try:
            u = f"http://{self.domnainHost}/yunonline/v1/sign_info?time={ts()}&unionid={self.unionId}"
            r = safe_request("GET", u)
            signStatus = r.json()["data"]["signIn"]
            signMessage = "未签到"
            if signStatus:
                signMessage = "已签到"
            print(f"账号[{self.name}]今日{signMessage}")
            if signStatus == False:
                self.sign_in()
        except Exception:
            print(f"账号[{self.name}]判断签到状态失败：{r.text}")
            return False

    def gold(self):
        r = ""
        try:
            u = f"http://{self.domnainHost}/yunonline/v1/gold?unionid={self.unionId}&time={ts()}"
            r = safe_request("GET", u)
            # print(r.json())
            rj = r.json()
            self.remain = math.floor(int(rj.get("data").get("last_gold")))
            if onlyDoInviteRewardJob and int(self.remain) > 3000:
                print("✅ 账号[{self.name}]金币超过3000，停止阅读")
                return False
            print(
                f'账号[{self.name}]今日已经阅读了{rj.get("data").get("day_read")}篇文章,剩余{rj.get("data").get("remain_read")}未阅读，今日获取金币{rj.get("data").get("day_gold")}，剩余{self.remain}'
            )
        except Exception as e:
            print(f"账号[{self.name}]获取金币失败：", e)
            # raise e
            return False

    def getKey(self):
        uk = ""
        ukRes = None
        u = f"http://{self.domnainHost}/{self.readJumpPath}"
        # print("提示 getKey：", u)
        p = f"unionid={self.unionId}"
        r = safe_request("POST", u, headers=self.headers, data=p, verify=False)
        # print("getKey：", r.text)
        rj = r.json()
        domain = rj.get("data").get("domain")
        # print("请求中转页：", r.text)
        pp = parse_qs(urlparse(domain).query)
        hn = urlparse(domain).netloc
        uk = pp.get("uk")[0]
        ukRes = r.text
        if uk == "":
            print(f"账号[{self.name}]获取uk失败，返回错误：{ukRes}")
            return
        time.sleep(8)
        # print(domain)
        r = safe_request(
            "GET",
            domain,
            headers={
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Connection": "keep-alive",
                "Host": f"{hn}",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309071d) XWEB/8461 Flue",
            },
            verify=False,
        )
        # <script src="https://image.hzysmyy.cn/yunsaoma/js/article.js?v16.0"></script>
        readJsVersion = extract_middle_text(r.text, "js/article.js?", '"')
        # print(readJsVersion)
        if readJsVersion:
            checkJsCodeChanged = (
                check_file_md5(
                    extract_middle_text(r.text, '<script src="', '"></scrip'),
                    "7c014a989ea39c4fd65aebddd0f22d3c",
                )
                == False
            )
            if (readJsVersion != "v16.0") or checkJsCodeChanged:
                print(
                    f"账号[{self.name}] 检测到接口版本发生变化，当前接口版本为：{readJsVersion}，拉响警报，台子搞事，要抓人了，开始撤退，退出程序 >> "
                )
                os._exit(0)
            else:
                # print(f"账号[{self.name}] 阅读准备完成：{uk}，提取到的地址：{domain}")
                if xyyydReadPureLog == False:
                    print(
                        f"账号[{self.name}] 阅读准备成功，当前接口版本为：{readJsVersion} 即将开始阅读 ✅ ，阅读参数为：{uk}"
                    )
        else:
            resText = trimSpaceCharacters(r.text)
            getReadUrlStr = extract_middle_text(
                resText,
                trimSpaceCharacters("function read_jump_read() {"),
                trimSpaceCharacters(
                    "localStorage.setItem('art_start_time', art_start_time);"
                ),
            )
            self.getReadUrlPath = extract_middle_text(
                getReadUrlStr,
                trimSpaceCharacters('url: domain + "'),
                trimSpaceCharacters("?uk="),
            )
            addGoldStr = extract_middle_text(
                resText,
                trimSpaceCharacters("function getGold(time) {"),
                trimSpaceCharacters('$(".goldNum").html(res.data.gold);'),
            )
            self.addGoldPath = extract_middle_text(
                addGoldStr,
                trimSpaceCharacters('url: domain + "'),
                trimSpaceCharacters("?uk="),
            )
            # http://cc67d48b82.t1713583661s.ek9e8.shop/rdf.html?uk=bbc57b9a7106cfa4388d9ca6e56aabe5&t=1713583669
            readApiVersion = extract_middle_text(
                resText,
                trimSpaceCharacters(
                    f'url: domain + "{self.getReadUrlPath}?uk=" + uk + "&time="+ time +"&psgn=168&vs='
                ),
                '"',
            )
            if readApiVersion:
                self.readApiVersion = readApiVersion
            if (
                trimSpaceCharacters(
                    f"""url: domain + "{self.addGoldPath}?uk=" + uk + "&time=" + time +
				"&timestamp=" + timestamp,"""
                )
                in resText
                and trimSpaceCharacters(
                    f'url: domain + "{self.getReadUrlPath}?uk=" + uk + "&time="+ time +"&psgn=168&vs={self.readApiVersion}",'
                )
                in resText
                # and check_str_md5(
                #     extract_middle_text(
                #         r.text, '<script type="text/javascript">', "</script>"
                #     ).replace(
                #         f'url: domain + "dyuedus?uk=" + uk + "&time="+ time +"&psgn=168&vs=abc",',
                #         f'url: domain + "dyuedus?uk=" + uk + "&time="+ time +"&psgn=168&v={self.readApiVersion}",',
                #     ),
                #     "6d66ea6279b870ec961c96d460547475",
                # )
            ):
                print(f"账号[{self.name}] 阅读准备完成，当前 加密代码hash值 与 预设值一致，加密内容未修改，可继续阅读 ✅ ")
            else:
                print(f"账号[{self.name}] 检测到加密代码内容发生变化，拉响警报，台子搞事，要抓人了，开始撤退，退出程序 >> ")
                os._exit(0)
        reqHeader = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Host": hn,
            "Origin": f"https://{hn}",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309071d) XWEB/8461 Flue",
        }
        return uk, reqHeader

    def read(self):
        self.sign_info()
        info = self.getKey()
        if len(info) == 0:
            print(f"账号[{self.name}]获取阅读参数失败，停止往后阅读！⚠️ ")
            return
        # print(info)
        time.sleep(2)
        arctileTime = 1
        wechatPostLink = ""
        while True:
            res = {"errcode": -1}
            refreshTime = 0
            while res["errcode"] != 0:
                timeStamp = str(ts())
                psgn = hashlib.md5(
                    (
                        info[1]["Host"].replace("https://", "")[0:11]
                        + info[0]
                        + timeStamp
                        + "A&I25LILIYDS$"
                    ).encode()
                ).hexdigest()
                # print(info, timeStamp)
                self.params = {
                    "uk": info[0],
                    "time": timeStamp,
                    "psgn": "168",
                    "vs": self.readApiVersion,
                }
                u = f"http://{info[1]['Host']}/{self.getReadUrlPath}"
                r = safe_request(
                    "GET",
                    u,
                    headers=info[1],
                    params=self.params,
                    verify=False,
                    timeout=60,
                )
                print("-" * 50)
                # print(
                #     f"账号[{self.name}]第[{refreshTime+1}]次获取阅读文章[{info[0]}]目的页：{r.text}"
                # )
                # print("阅读文章参数查看：", u, self.params, r.text, info[1])
                try:
                    if r.text and r.json()["errcode"] == 0:
                        res = r.json()
                        print(
                            f"账号[{self.name}]第[{refreshTime+1}]次获取第[{arctileTime}]篇阅读文章[{info[0]}]跳转链接成功"
                        )
                    else:
                        decoded_str = json.loads(r.text)
                        if decoded_str["errcode"] == 409:
                            if decoded_str["msg"] and int(decoded_str["msg"]) > 0:
                                decoded_str["msg"] = (
                                    str(round(int(decoded_str["msg"]) / 60, 2))
                                    + " 分钟后再来阅读吧~"
                                )
                        if decoded_str["msg"]:
                            tipText = decoded_str["msg"]
                            if "您的阅读暂时失效" in decoded_str["msg"]:
                                tipText = (
                                    decoded_str["msg"]
                                    + " 🚨 检测未通过的文章为："
                                    + wechatPostLink
                                )
                            print(
                                f"账号[{self.name}]第[{refreshTime+1}]次获取第[{arctileTime}]篇阅读文章[{info[0]}]跳转链接失败：{tipText}"
                            )
                            return False
                        else:
                            tipText = r.json()["msg"]
                            if "您的阅读暂时失效" in r.text:
                                tipText = r.text + " 🚨 检测未通过的文章为：" + wechatPostLink
                            print(
                                f"账号[{self.name}]第[{refreshTime+1}]次获取第[{arctileTime}]篇阅读文章[{info[0]}]跳转链接异常：{tipText}"
                            )
                except Exception:
                    print(
                        f"账号[{self.name}]第[{refreshTime+1}]次获取第[{arctileTime}]篇阅读文章[{info[0]}]跳转链接异常：{r.text}"
                    )
                time.sleep(1.5)
                refreshTime = refreshTime + 1
                if refreshTime >= 5:
                    print(f"⚠️ 账号[{self.name}]获取阅读第[{arctileTime}]篇文章[{info[0]}]超时……")
                    return
            print("获取文章数据：", res)
            if res.get("errcode") == 0:
                returnLink = ""
                try:
                    returnLink = res.get("data").get("link")
                except Exception:
                    print(
                        f"⚠️ 账号[{self.name}]获取阅读第[{arctileTime}]篇文章[{info[0]}]链接失败，疑似台子接口太垃圾，崩了，返回数据为：",
                        res.get("data"),
                    )
                    continue
                if "mp.weixin.qq.com" in returnLink:
                    if xyyydReadPureLog == False:
                        print(f"账号[{self.name}] 阅读第[{arctileTime}]篇微信文章：{returnLink}")
                    wechatPostLink = returnLink
                else:
                    # print(f"账号[{self.name}] 阅读第[{arctileTime}]篇文章准备跳转：{link}")
                    wechatPostLink = self.jump(returnLink)
                    if xyyydReadPureLog == False:
                        print(
                            f"账号[{self.name}] 阅读第[{arctileTime}]篇微信文章：{wechatPostLink}"
                        )
                if xyyydReadPureLog == False:
                    print(f"账号[{self.name}] 阅读第[{arctileTime}]篇文章：{wechatPostLink}")
                sleepTime = random.randint(7, 10)
                if "mp.weixin.qq.com" in wechatPostLink:
                    postWechatInfo = getPostWechatInfo(wechatPostLink)
                    if postWechatInfo == False:
                        print(
                            f"⚠️ 账号[{self.name}]因 获取公众号文章信息不成功，导致阅读第[{arctileTime}]篇文章[{info[0]}] 失败……"
                        )
                        return False
                    # 如果是检测特征到的文章 或者 后一篇文章与前一篇相似
                    if (
                        checkDict.get(postWechatInfo[4]) != None
                        # or ("&idx=1" not in wechatPostLink)
                        # or ("&idx=7" in wechatPostLink)
                        # or ("&idx=5" in wechatPostLink)
                        # or ("&idx=8" in wechatPostLink)
                        # or (res.get("data").get("a") == 2)
                        or ("&chksm=" in wechatPostLink)
                        # or ("__biz" not in wechatPostLink)
                    ):
                        sleepTime = readPostDelay or random.randint(15, 20)
                        print(
                            f"⚠️ 账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}] 检测到疑似检测文章，正在推送，等待过检测，等待时间：{sleepTime}秒。。。"
                        )
                        global link_cache
                        fetch_wx_time_and_record(wechatPostLink, link_cache)
                        if self.wechatBussinessKey:
                            pushWechatBussiness(self.wechatBussinessKey, wechatPostLink)
                        elif self.appToken:
                            push(
                                self.appToken,
                                self.topicIds,
                                "小阅阅阅读过检测",
                                wechatPostLink,
                                f"账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}] 正在等待过检测，等待时间：{sleepTime}秒\n幻生提示：快点，别耽搁时间了！",
                            )
                        else:
                            print(
                                f"⚠️ 账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}] 需要过检测，但是未配置推送token，为了避免黑号，停止阅读。。。"
                            )
                            return False
                    else:
                        print(
                            f"✅ 账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}] 非检测文章，模拟读{sleepTime}秒"
                        )
                else:
                    print(
                        f"✅ 账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}] 非检测文章，模拟读{sleepTime}秒"
                    )
                time.sleep(sleepTime)
                u1 = f"http://{info[1]['Host']}/{self.addGoldPath}?uk={info[0]}&time={sleepTime}&timestamp={ts()}"
                r1 = safe_request("GET", u1, headers=info[1], verify=False)
                if r1.text and r1.json():
                    try:
                        print(
                            f"✅ 账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}]所得金币：{r1.json()['data']['gold']}个，账户当前金币：{r1.json()['data']['last_gold']}个，今日已读：{r1.json()['data']['day_read']}次，今日未读 {r1.json()['data']['remain_read']}篇文章"
                        )
                        if (
                            onlyDoInviteRewardJob
                            and int(r1.json()["data"]["last_gold"]) > 3000
                        ):
                            print("✅ 账号[{self.name}]金币超过3000，停止阅读")
                            break
                    except Exception:
                        print(
                            f"❌ 账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}]异常：{r1.json().get('msg')}"
                        )
                        if "阅读无效" in r1.json().get("msg"):
                            continue
                        else:
                            break
                else:
                    print(
                        f"❌ 账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}]失败：{r1.text}"
                    )
                    break
            elif res.get("errcode") == 405:
                print(f"⚠️ 账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}]阅读重复")
                time.sleep(1.5)
            elif res.get("errcode") == 407:
                print(f"⚠️ 账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}]阅读结束")
                return True
            else:
                print(f"⚠️ 账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}]未知情况")
                time.sleep(1.5)
            arctileTime = arctileTime + 1

    def jump(self, link):
        print(f"账号[{self.name}]开始本次阅读……")
        hn = urlparse(link).netloc
        h = {
            "Host": hn,
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090621) XWEB/8351 Flue",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh",
            "Cookie": f"ysm_uid={self.ysm_uid}",
        }
        r = safe_request("GET", link, headers=h, allow_redirects=False, verify=False)
        # print(r.status_code)
        Location = r.headers.get("Location")
        print(f"账号[{self.name}]开始阅读文章 - {Location}")
        return Location

    def withdrawPost(self, exchangeParams, withdrawBalanceNum):
        global totalWithdrawAmount
        u = f"http://{self.domnainHost}/yunonline/v1/withdraw"
        p = f"unionid={exchangeParams['unionid']}&signid={exchangeParams['request_id']}&ua=0&ptype=0&paccount=&pname="
        if self.aliAccount and self.aliName:
            p = f"unionid={exchangeParams['unionid']}&signid={exchangeParams['request_id']}&ua=2&ptype=1&paccount={quote(self.aliAccount)}&pname={quote(self.aliName)}"
        r = safe_request(
            "POST",
            u,
            headers={
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Cookie": f"ysmuid={self.ysm_uid}; ejectCode=1",
                "Host": f"{self.domnainHost}",
                "Origin": f"http://{self.domnainHost}",
                "Proxy-Connection": "keep-alive",
                "Referer": f"http://{self.domnainHost}/yunonline/v1/exchange?unionid={exchangeParams['unionid']}&request_id={exchangeParams['request_id']}&qrcode_number=16607864358145588",
                "X-Requested-With": "XMLHttpRequest",
            },
            data=p,
            verify=False,
        )
        try:
            if r.json()["msg"] == "success":
                print(f"✅ 账号[{self.name}] 提现结果：", r.json()["msg"])
                totalWithdrawAmount += withdrawBalanceNum
                print(f"✅ 本轮累计提现了 ", totalWithdrawAmount, " 元")
            else:
                print(
                    f"账号[{self.name}] 提现失败：",
                    r.json()["msg"],
                    f" 支付宝账号{self.aliAccount} 姓名{self.aliName}",
                )
        except Exception as e:
            print(f"账号[{self.name}] 提现异常：", r.text)

    def withdraw(self):
        gold = int(int(self.remain) / 1000) * 1000
        print(f"账号[{self.name}] 本次提现金额 ", self.balance, "元 + ", gold, "金币")
        # print(self.exchangeParams)
        query = urlsplit(self.exchangeParams).query
        exchangeParams = parse_qs(query)
        # 将列表值转换为字符串
        for key, value in exchangeParams.items():
            exchangeParams[key] = value[0]
        withdrawBalance = round((int(self.txbz) / 10000), 3)
        # print(self.domnainHost)
        if gold or (self.balance >= withdrawBalance):
            if gold and ((float(self.balance) + gold / 10000) <= 30):
                # 开始提现
                u1 = f"http://{self.domnainHost}/yunonline/v1/user_gold"
                p1 = f"unionid={exchangeParams['unionid']}&request_id={exchangeParams['request_id']}&gold={gold}"
                r = safe_request(
                    "POST",
                    u1,
                    data=p1,
                    headers={
                        "Accept": "application/json, text/javascript, */*; q=0.01",
                        "Accept-Encoding": "gzip, deflate",
                        "Accept-Language": "zh-CN,zh;q=0.9",
                        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                        "Cookie": f"ysmuid={self.ysm_uid}; ejectCode=1",
                        "Host": f"{self.domnainHost}",
                        "Origin": f"http://{self.domnainHost}",
                        "Proxy-Connection": "keep-alive",
                        "Referer": f"http://{self.domnainHost}/yunonline/v1/exchange{self.exchangeParams}",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309071d) XWEB/8461 Flue",
                        "X-Requested-With": "XMLHttpRequest",
                    },
                    verify=False,
                )
                try:
                    # print(r.text)
                    res = r.json()
                    if res.get("errcode") == 0:
                        withdrawBalanceNum = self.balance + float(res["data"]["money"])
                        print(
                            f"✅ 账号[{self.name}] 金币兑换为现金成功，开始提现，预计到账 {withdrawBalanceNum} 元 >>> "
                        )
                        if withdrawBalanceNum < withdrawBalance:
                            print(f"账号[{self.name}]没有达到提现标准 {withdrawBalance} 元")
                            return False
                        self.withdrawPost(exchangeParams, withdrawBalanceNum)
                        return
                    else:
                        print(
                            f"账号[{self.name}] 金币兑换为现金失败：",
                            r.text,
                            " 提现地址：",
                            u1,
                            " 提现参数：",
                            p1,
                        )
                except Exception as e:
                    # raise e
                    # 处理异常
                    print(f"账号[{self.name}] 提现失败：", e)
            self.withdrawPost(exchangeParams, self.balance)

    def init(self):
        try:
            characters = string.ascii_letters + string.digits
            r = safe_request(
                "GET",
                f"https://nsr.zsf2023e458.cloud/yunonline/v1/getchatsite?t={time.time()}&cid={''.join(random.choices(characters, k=32))}&code=081ktRFa1TM60H0gr4Ga1U{''.join(random.choices(characters, k=10))}&state=1",
                verify=False,
            )
            self.domnainHost = r.json()["data"]["luodi"].split("/")[2]
            # print(r.text)
            if xyyydReadPureLog == False:
                print(f"账号[{self.name}]提取到的域名：{self.domnainHost}")
            self.headers = {
                "Connection": "keep-alive",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090621) XWEB/8351 Flue",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": f"http://{self.domnainHost}/",
                "Origin": f"http://{self.domnainHost}",
                # "Host": f"{self.domnainHost}",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Cookie": f"ysm_uid={self.ysm_uid}; ysmuid={self.ysm_uid};",
            }
            # 获取requestId
            self.signid = ""
            for i in range(3):
                r = safe_request(
                    "GET",
                    f"http://{self.domnainHost}/",
                    headers={
                        "Upgrade-Insecure-Requests": "1",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309071d) XWEB/8461 Flue",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                        "Accept-Encoding": "gzip, deflate",
                        "Accept-Language": "zh-CN,zh;q=0.9",
                        "Cookie": f"ysmuid={self.ysm_uid}",
                    },
                    verify=False,
                )
                htmltext = r.text
                if r.history:
                    for resp in r.history:
                        if "open.weixin.qq.com" in resp.headers["Location"]:
                            print(
                                f"账号[{self.name}] Cookie已过期，请重进一下网站，就会自动更新Cookie（目前不确定过期是因为自己手动进去过了还是什么其他原因）"
                            )
                            return False
                res1 = re.sub("\s", "", htmltext)
                signidl = re.findall('\)\|\|"(.*?)";', res1)
                unionId = extract_middle_text(htmltext, 'unionid="', '"')
                userId = extract_middle_text(htmltext, '">我的id:', "<")
                parentId = extract_middle_text(htmltext, 'var codeid = "', '"')
                if self.name == "":
                    self.name = f"[用户Id {userId}][父级Id {parentId}]"
                if unionId:
                    self.unionId = unionId
                    print(f"账号[{self.name}] unionId 为 {self.unionId}")

                if "该账号存在违规操作，已被封禁" in htmltext or "存在违规操作，已封" in htmltext:
                    if "直接提" not in self.name:
                        print(f"账号[{self.name}] 存在违规操作，已被封禁，凉凉，过两个月再看看解没解封吧~ ")
                        return False
                    else:
                        self.balance = 5
                        self.remain = 10000
                        self.exchangeParams = f"?unionid={self.ysm_uid}&request_id=d97c9564b9a1a819813139e7f910251d&qrcode_number=16607864358145588&addtime=1693293641"
                        break
                if "url: domain+'sign_info?time='+Date.parse(new Date())," in htmltext:
                    self.signModule = True
                else:
                    print(f"账号[{self.name}] 检测到签到接口已变更，不进行签到！")
                if signidl == []:
                    time.sleep(1)
                    continue
                else:
                    self.signid = signidl[0]
                    break
            # 获取提现页面地址
            r = safe_request(
                "GET",
                f"http://{self.domnainHost}/?cate=0",
                headers={
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309071d) XWEB/8461 Flue",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                    "Cookie": f"ysmuid={self.ysm_uid}",
                },
                verify=False,
            )
            htmltext = r.text
            read_jump_read_text = extract_middle_text(
                htmltext,
                "function read_jump_read(type,time){",
                "success: function(res) {",
            )
            # self.getHelpCode = extract_middle_text(
            #     htmltext, "/yunonline/v1/redirect/", "?unionid="
            # )
            if read_jump_read_text:
                readJumpPath = extract_middle_text(
                    read_jump_read_text, "url: nodomain+'", "',"
                )
                if readJumpPath:
                    self.readJumpPath = readJumpPath
                else:
                    print(
                        f"账号[{self.name}] 初始化失败，请手动访问下确认页面没崩溃 或者 稍后再试吧，一直不行，请前往TG群反馈~ "
                    )
                    return False
            else:
                hiddenTipText = extract_middle_text(
                    htmltext, '<!-- <p style="color:red">', "<br>"
                )
                # 移除掉注释的公告部分
                htmltext = htmltext.replace(
                    '<!-- <p style="color:red">' + hiddenTipText + "<br>", ""
                )
                tipText = extract_middle_text(htmltext, '<p style="color:red">', "<br>")
                if "直接提" not in self.name:
                    if "存在违规操作" in htmltext or "存在违规操作，已封" in htmltext:
                        print(f"账号[{self.name}] 被检测到了，已经被封，终止任务，快去提醒大家吧~ ")
                        # os._exit(0)
                        return False
                    elif "系统维护中" in tipText:
                        # <p style="color:red">系统维护中，预计周一恢复，与码无关！<br>
                        print(f"账号[{self.name}] 检测到系统维护中，公告内容为 [{tipText}] ，终止任务")
                        os._exit(0)
                    else:
                        print(
                            f"账号[{self.name}] 初始化失败，请手动访问下确认页面没崩溃 或者 稍后再试吧，一直不行，请前往TG群反馈~ "
                        )
                        return False
            res1 = re.sub("\s", "", htmltext)
            signidl = re.findall('/yunonline/v1/exchange(.*?)"', res1)
            # print("初始化 提现参数:", signidl[0])
            withdraw_page_text = extract_middle_text(
                htmltext,
                '">找回原账户</p></div>',
                ">提现</a></di",
            )
            withdraw_url = extract_middle_text(withdraw_page_text, 'href="', '"')
            # print(withdraw_url)
            if withdraw_url and withdrawAlipay:
                r = safe_request(
                    "GET",
                    withdraw_url,
                    headers={
                        "Upgrade-Insecure-Requests": "1",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309071d) XWEB/8461 Flue",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                        "Accept-Encoding": "gzip, deflate",
                        "Accept-Language": "zh-CN,zh;q=0.9",
                        "Cookie": f"ysmuid={self.ysm_uid}",
                    },
                    verify=False,
                )
                if r.text:
                    self.isBindAliAccount = (
                        extract_middle_text(r.text, 'var bindffli = "', '";') != "0"
                    )
                    if self.isBindAliAccount:
                        self.aliAccount = extract_middle_text(
                            r.text, 'var raccount = "', '";'
                        )
                        self.aliName = extract_middle_text(
                            r.text, 'var rname = "', '";'
                        )
                        print(
                            f"账号[{self.name}] 检测到已绑定支付宝：{self.aliName} - {self.aliAccount}"
                        )
                    else:
                        print(f"账号[{self.name}] 检测到未绑定支付宝，可自动提现绑定支付宝！")
            if signidl == []:
                print(f"账号[{self.name}]初始化 提现参数 失败,账号异常")
                return "直接提" in self.name
            else:
                self.exchangeParams = signidl[0]
            rewardNumResult = re.search(
                '<div class="num number rewardNum">(.*?)</', htmltext
            )
            # print("初始化 提现参数:", signidl[0])
            if rewardNumResult == []:
                print(f"账号[{self.name}]初始化 提现参数 失败,账号异常")
                return "直接提" in self.name
            else:
                self.balance = float(rewardNumResult[1])
            if self.signid == "":
                print(f"账号[{self.name}]初始化 requestId 失败,账号异常")
                return "直接提" in self.name

            return True
        except Exception:
            # raise e
            print(f"账号[{self.name}]初始化失败,请检查你的ck")
            return False

    def gethelpcode(self, secret):
        r = ""
        if secret == "" or secret == False:
            print(f"账号[{self.name}] secret为空：", secret)
            return False
        try:
            u = f"http://{self.domnainHost}/yunonline/v1/gethelpcode?secret={secret}"
            r = safe_request("GET", u)
            # print(r.json())
            rj = r.json()
            self.helpAccountUrl = rj.get("data").get("qrcodes")
            self.helpAccountCode = extract_middle_text(
                self.helpAccountUrl, "auth/", "?"
            )
            print(f"账号[{self.name}] 助力码为 {self.helpAccountCode}")
        except Exception as e:
            print(f"账号[{self.name}] 获取助力码失败：", e)
            # raise e
            return False

    def getSecret(self, retryTime=0):
        r = ""
        if retryTime > 5:
            print(f"账号[{self.name}] 多次获取secret失败")
            return ""
        try:
            u = f"http://{self.domnainHost}/yunonline/v1/helpcode/{self.getHelpCode}"
            r = safe_request("GET", u)
            # print(r.text)
            secret = extract_middle_text(r.text, 'var secret = "', '"')
            if secret == "":
                retryTime += 1
                print(f"账号[{self.name}] 获取 secret 失败")
                return self.getSecret(retryTime)
            else:
                print(f"账号[{self.name}] 获取 secret 成功")
                return secret
        except Exception as e:
            print(f"账号[{self.name}] 获取secret失败：", e)
            # raise e
            return False

    def helpeRead(self):
        followHeader = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090621) XWEB/8351 Flue",
            "Cookie": f"ysm_uid={self.ysm_uid}; ysmuid={self.ysm_uid};",
        }
        helpHeaders, helpContentBytes = follow_redirect(
            self.helpAccountUrl,
            max_redirects=3,
            stop_on="?cate=1&cid=",
            headers=followHeader,
            verify=False,
            timeout=60,
            allow_redirects=False,
        )
        helpContent = str(helpContentBytes.decode("utf-8"))
        # print(helpHeaders, helpContent)
        secret = extract_middle_text(helpContent, 'var secret="', '"')
        if secret == "":
            print(f"账号[{self.name}]获取助力阅读参数异常，尝试强制获取⚠️ ")
            helpHeaders, helpContentBytes = follow_redirect(
                self.helpAccountUrlBak,
                max_redirects=3,
                stop_on="?cate=1&cid=",
                headers=followHeader,
                verify=False,
                timeout=60,
                allow_redirects=False,
            )
            helpContent = str(helpContentBytes.decode("utf-8"))
            secret = extract_middle_text(helpContent, 'var secret="', '"')
        if len(helpContent) == 0:
            print(f"账号[{self.name}]获取助力阅读参数失败，停止往后阅读！⚠️ ")
            return
        if check_str_md5(
            extract_middle_text(
                helpContent,
                "function read_jump_wechat(type) {",
                "success: function (res) {",
            ),
            "26bfb95b476f83571c6ce567aff3d86a",
        ) and check_str_md5(
            extract_middle_text(
                helpContent, "function getGold(time){", "success: function(res) {"
            ),
            "88bd5a27c11fe36acfc2e1e7ac8165ad",
        ):
            print(f"账号[{self.name}] 助力阅读检测完成，当前 加密代码hash值 与 预设值一致，加密内容未修改，可继续阅读 ✅ ")
        else:
            # print(self.helpAccountUrl)
            print(f"账号[{self.name}] 检测到助力阅读代码内容发生变化，拉响警报，台子搞事，要抓人了，开始撤退，退出程序 >> ")
            os._exit(0)
        reqApi = extract_middle_text(helpContent, 'var domain="', '"')
        reqScheme = urlparse(reqApi).scheme
        reqHost = urlparse(reqApi).netloc
        header = {
            "Host": reqHost,
            "Connection": "keep-alive",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090621) XWEB/8351 Flue",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": reqScheme + "://" + reqHost,
            "Referer": reqScheme + "://" + reqHost,
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cookie": f"ysm_uid={self.ysm_uid}; ysmuid={self.ysm_uid};",
        }
        time.sleep(2)
        arctileTime = 1
        while True:
            res = {"errcode": -1}
            refreshTime = 0
            # var domain="http://1712565229.xxl860.top/yunonline/v1/";
            # var proto = window.location.protocol
            # var url_test = window.location.host;
            # domain = proto + "//"+url_test+"/yunonline/v1/";
            # get protocol
            wechatPostLink = ""
            while res["errcode"] != 0:
                u = f"{reqApi}task"
                body = {
                    "secret": secret,
                    "type": "read",
                }
                r = safe_request(
                    "POST",
                    u,
                    data=body,
                    headers=header,
                    verify=False,
                    timeout=60,
                )
                print("-" * 50)
                # print(
                #     f"账号[{self.name}]第[{refreshTime+1}]次获取阅读文章[{info[0]}]目的页：{r.text}"
                # )
                # print("阅读文章参数查看：", u, self.params, r.text, info[1])
                try:
                    if r.text and r.json()["errcode"] == 0:
                        res = r.json()
                        print(
                            f"账号[{self.name}]第[{refreshTime+1}]次获取第[{arctileTime}]篇助力阅读文章跳转链接成功"
                        )
                    else:
                        decoded_str = json.loads(r.text)
                        # {"errcode": 409, "msg": "3289"}
                        if decoded_str["errcode"] == 409:
                            if decoded_str["msg"] and int(decoded_str["msg"]) > 0:
                                decoded_str["msg"] = (
                                    str(round(int(decoded_str["msg"]) / 60, 2))
                                    + " 分钟后再来阅读吧~"
                                )
                        if decoded_str["msg"]:
                            tipText = decoded_str["msg"]
                            if "您的阅读暂时失效" in decoded_str["msg"]:
                                tipText = (
                                    decoded_str["msg"]
                                    + " 🚨 检测未通过的文章为："
                                    + wechatPostLink
                                )
                            print(
                                f"账号[{self.name}]第[{refreshTime+1}]次获取第[{arctileTime}]篇助力阅读文章跳转链接失败：{tipText}"
                            )
                            return False
                        else:
                            tipText = r.json()["msg"]
                            # print(r.json())
                            if "您的阅读暂时失效" in r.text:
                                tipText = r.text + " 🚨 检测未通过的文章为：" + wechatPostLink
                            print(
                                f"账号[{self.name}]第[{refreshTime+1}]次获取第[{arctileTime}]篇助力阅读文章跳转链接失败：{tipText}"
                            )
                except Exception as e:
                    print(
                        f"账号[{self.name}]第[{refreshTime+1}]次获取第[{arctileTime}]篇助力阅读文章跳转链接异常：{r.text}，错误发生于：",
                        e,
                    )
                time.sleep(1.5)
                refreshTime = refreshTime + 1
                if refreshTime >= 5:
                    print(f"⚠️ 账号[{self.name}]获取助力阅读第[{arctileTime}]篇文章超时……")
                    return
            print("获取文章数据：", res)
            if res.get("errcode") == 0:
                returnLink = ""
                try:
                    returnLink = res.get("data").get("link")
                except Exception:
                    print(
                        f"⚠️ 账号[{self.name}]获取助力阅读第[{arctileTime}]篇文章链接失败，疑似台子接口太垃圾，崩了，返回数据为：",
                        res.get("data"),
                    )
                    continue
                if "mp.weixin.qq.com" in returnLink:
                    if xyyydReadPureLog == False:
                        print(f"账号[{self.name}] 助力阅读第[{arctileTime}]篇微信文章：{returnLink}")
                    wechatPostLink = returnLink
                else:
                    # print(f"账号[{self.name}] 阅读第[{arctileTime}]篇文章准备跳转：{link}")
                    wechatPostLink = self.jump(returnLink)
                    if xyyydReadPureLog == False:
                        print(
                            f"账号[{self.name}] 助力阅读第[{arctileTime}]篇微信文章：{wechatPostLink}"
                        )
                if xyyydReadPureLog == False:
                    print(f"账号[{self.name}] 助力阅读第[{arctileTime}]篇文章：{wechatPostLink}")
                sleepTime = random.randint(7, 10)
                if "mp.weixin.qq.com" in wechatPostLink:
                    postWechatInfo = getPostWechatInfo(wechatPostLink)
                    if postWechatInfo == False:
                        print(
                            f"⚠️ 账号[{self.name}]因 获取公众号文章信息不成功，导致阅读第[{arctileTime}]篇文章 失败……"
                        )
                        return False
                    # 如果是检测特征到的文章 或者 后一篇文章与前一篇相似
                    if (
                        checkDict.get(postWechatInfo[4]) != None
                        # or ("&idx=1" not in wechatPostLink)
                        # or ("&idx=7" in wechatPostLink)
                        # or ("&idx=5" in wechatPostLink)
                        # or ("&idx=8" in wechatPostLink)
                        # or (res.get("data").get("a") == 2)
                        or ("&chksm=" in wechatPostLink)
                        # or ("__biz" not in wechatPostLink)
                    ):
                        sleepTime = readPostDelay or random.randint(15, 20)
                        print(
                            f"⚠️ 账号[{self.name}]助力阅读第[{arctileTime}]篇文章 检测到疑似检测文章，正在推送，等待过检测，等待时间：{sleepTime}秒。。。"
                        )
                        global link_cache
                        fetch_wx_time_and_record(wechatPostLink, link_cache)
                        if self.wechatBussinessKey:
                            pushWechatBussiness(self.wechatBussinessKey, wechatPostLink)
                        elif self.appToken:
                            push(
                                self.appToken,
                                self.topicIds,
                                "小阅阅阅读过检测",
                                wechatPostLink,
                                f"账号[{self.name}]助力阅读第[{arctileTime}]篇文章 正在等待过检测，等待时间：{sleepTime}秒\n幻生提示：快点，别耽搁时间了！",
                            )
                        else:
                            print(
                                f"⚠️ 账号[{self.name}]助力阅读第[{arctileTime}]篇文章 需要过检测，但是未配置推送token，为了避免黑号，停止阅读。。。"
                            )
                            return False
                    else:
                        print(
                            f"✅ 账号[{self.name}]助力阅读第[{arctileTime}]篇文章 非检测文章，模拟读{sleepTime}秒"
                        )
                else:
                    print(
                        f"✅ 账号[{self.name}]助力阅读第[{arctileTime}]篇文章 非检测文章，模拟读{sleepTime}秒"
                    )
                time.sleep(sleepTime)
                u1 = f"{reqApi}add_gold"
                data = {
                    "unionid": extract_middle_text(helpContent, 'unionid="', '"'),
                    "time": sleepTime,
                }
                r1 = safe_request("POST", u1, data=data, headers=header, verify=False)
                if r1.text and r1.json():
                    try:
                        print(
                            f"✅ 账号[{self.name}]助力阅读第[{arctileTime}]篇文章所得金币：{r1.json()['data']['gold']}个，账户当前金币：{r1.json()['data']['day_gold']}个，今日已读：{r1.json()['data']['day_read']}次"
                        )
                        if (
                            onlyDoInviteRewardJob
                            and int(r1.json()["data"]["day_gold"]) > 3000
                        ):
                            print("✅ 账号[{self.name}]金币超过3000，停止阅读")
                            break
                    except Exception:
                        print(
                            f"❌ 账号[{self.name}]助力阅读第[{arctileTime}]篇文章异常：{r1.json().get('msg')}"
                        )
                        if "阅读无效" in r1.json().get("msg"):
                            continue
                        else:
                            break
                else:
                    print(f"❌ 账号[{self.name}]助力阅读第[{arctileTime}]篇文章失败：{r1.text}")
                    break
            elif res.get("errcode") == 405:
                print(f"⚠️ 账号[{self.name}]助力阅读第[{arctileTime}]篇文章阅读重复")
                time.sleep(1.5)
            elif res.get("errcode") == 407:
                print(f"⚠️ 账号[{self.name}]助力阅读第[{arctileTime}]篇文章阅读结束")
                return True
            else:
                print(f"⚠️ 账号[{self.name}]助力阅读第[{arctileTime}]篇文章未知情况")
                time.sleep(1.5)
            arctileTime = arctileTime + 1

    def run(self):
        if self.init():
            self.user_info()
            if onlyWithdraw == False:
                if self.helpAccountUrl == "":
                    self.hasWechat()
                    if self.gold() == False:
                        return
                if "直接提" not in self.name:
                    currentHour = datetime.now().hour
                    if (currentHour < readTimeRange[0]) or (
                        currentHour > readTimeRange[1]
                    ):
                        print(
                            f"账号[{self.name}] 检测到当前时间不在设定的阅读时间范围 {readTimeRange[0]}-{readTimeRange[1]}小时 内，跳过阅读"
                        )
                    else:
                        self.read()
                        # if self.helpAccountUrl:
                        #     print(f"账号[{self.name}] 检测到配置了助力阅读链接，开始进行助力阅读 >>> ")
                        #     self.helpeRead()
                        # else:
                        #     if self.getHelpCode:
                        #         self.gethelpcode(self.getSecret())
                        #     time.sleep(3)
                        #     self.read()
            if self.helpAccountUrl == "":
                time.sleep(3)
                if self.gold() == False:
                    return
                if onlyDoInviteRewardJob == False:
                    time.sleep(3)
                    self.withdraw()


def getNewInviteUrl():
    r = safe_request(
        "GET", "https://www.filesmej.cn/waidomain.php", verify=False
    ).json()
    if r.get("code") == 0:
        newEntryUrl = r.get("data").get("luodi")
        parsed_url = urlparse(newEntryUrl)
        host = parsed_url.hostname
        return f"http://dcc222334.y43a1.3gn8m.cn/jxybyy/2639bb95daba1d99e5338a8c2e21e2f0?upuid=91".replace(
            "dcc222334.y43a1.3gn8m.cn", host or "dcc222334.y43a1.3gn8m.cn"
        )
    else:
        return "http://dcc222334.y43a1.3gn8m.cn/jxybyy/2639bb95daba1d99e5338a8c2e21e2f0?upuid=91"


def main(account, forceAlipayName="", forceAlipayAccount=""):
    # print("-" * 50)
    # print(f"账号[{account.split('#')[0]}]开始执行任务 >>>")
    # print("\n")
    # 按@符号分割当前账号的不同参数
    values = account.split("#")
    # print(values)
    cg = {}
    try:
        if len(values) == 3:
            cg = {
                "name": values[0],
                "ysm_uid": values[1],
                "unionId": values[2],
                "txbz": 3000,
                "aliAccount": forceAlipayAccount or "",
                "aliName": forceAlipayName or "",
                "helpAccountUrl": globalHelpAccountUrl,
            }
        elif len(values) == 2:
            cg = {
                "name": values[0],
                "ysm_uid": values[1],
                "unionId": "",
                "txbz": 3000,
                "aliAccount": forceAlipayAccount or "",
                "aliName": forceAlipayName or "",
                "helpAccountUrl": globalHelpAccountUrl,
            }
        elif len(values) == 1:
            cg = {
                "name": "",
                "ysm_uid": values[0],
                "unionId": "",
                "txbz": 3000,
                "aliAccount": forceAlipayAccount or "",
                "aliName": forceAlipayName or "",
                "helpAccountUrl": globalHelpAccountUrl,
            }
        else:
            cg = {
                "name": values[0],
                "ysm_uid": values[1],
                "unionId": "",
                "txbz": values[2] or 3000,
                "aliAccount": forceAlipayAccount or "",
                "aliName": forceAlipayName or "",
                "helpAccountUrl": globalHelpAccountUrl,
            }
    except Exception:
        # 处理异常
        print("幻生逼逼叨:", f"账号[{account.split('#')[0]}]配置的啥玩意，缺参数了憨批，看清脚本说明！")
    cg["appToken"] = wxpusherAppToken or ""
    cg["topicIds"] = wxpusherTopicId or ""
    if len(values) >= 4:
        if values[3]:
            cg["appToken"] = values[3]
    if len(values) >= 5:
        if values[4]:
            cg["topicIds"] = values[4]
    if len(values) >= 6:
        if values[5]:
            cg["aliName"] = values[5]
    if len(values) >= 7:
        if values[6]:
            cg["aliAccount"] = values[6]
    if len(values) >= 8:
        if values[8]:
            cg["helpAccountUrl"] = values[7]
    try:
        if onlyWithdraw == False:
            if wechatBussinessKey == "":
                if cg["appToken"].startswith("AT_") == False:
                    print(f"幻生提示，账号[{account.split('#')[0]}] wxpush 配置错误，快仔细看头部说明！")
                if (cg["appToken"].startswith("AT_") == False) or (
                    cg["topicIds"].isdigit() == False
                ):
                    print(f"幻生提示，账号[{account.split('#')[0]}] wxpush 配置错误，快仔细看头部说明！")
        api = HHYD(cg)
        if cg["aliName"] and cg["aliAccount"]:
            print(
                f"幻生提示，账号[{account.split('#')[0]}] 采用了 支付宝提现，姓名：{cg['aliName']}，账户：{cg['aliAccount']}"
            )
        else:
            print(f"幻生提示，账号[{account.split('#')[0]}] 采用了 微信提现")
        api.run()
    except Exception as e:
        print(f"幻生提示，账号[{account.split('#')[0]}] 出错啦，请将下面报错截图发到tg交流群:", e)
        raise e
    # print("\n")
    # print("-" * 50)
    # print(f"账号[{account.split('#')[0]}]执行任务完毕！")
    # print("\n")


if __name__ == "__main__":
    # appToken：这个是填wxpusher的appToken
    # topicIds：这个是wxpusher的topicIds改成你自己的
    # 示例: 幻生#oZdBp04psgoN8dN1ET_uo81NTC31#3000#AT_UyIlbj2222nynESbM2vJyA7DrmUmUXD#11686
    accounts = os.getenv("xyyyd")
    inviteUrl = getNewInviteUrl()
    if accounts is None:
        print(f"你没有填入xyyyd，咋运行？\n走下邀请呗：{inviteUrl}")
    else:
        # 获取环境变量的值，并按指定字符串分割成多个账号的参数组合
        accounts_list = os.environ.get("xyyyd").split("&")

        # 输出有几个账号
        num_of_accounts = len(accounts_list)
        moreTip = ""
        if readPostDelay > 0:
            moreTip = f"已设置的推送文章等待点击时间为 {readPostDelay}秒 "
        print(
            f"当前脚本版本：小阅阅阅读 V2.31 \n幻生提示：获取到 {num_of_accounts} 个账号 {moreTip}\n注册地址：{inviteUrl}"
        )
        USE_THREADS = 1
        if os.environ.get("xyyydConcurrency"):
            USE_THREADS = int(os.environ.get("xyyydConcurrency")) or 1

        # 支付宝姓名#支付宝账号#账号序号xx-xx（0为起点)，多个全局支付宝提现配置用 , 分割
        # 单个支付宝的提现次数，默认为 1：gloablAlipayWithdrawTimeForAccount
        needCheckGlobalAlipay = (
            gloablAlipayAccounts
            and len(gloablAlipayAccounts)
            and gloablAlipayWithdrawTimeForAccount
        )
        extendAlipayAccs = []
        if needCheckGlobalAlipay:

            def distribute_items(lst):
                result = []
                for i in range(0, len(lst), gloablAlipayWithdrawTimeForAccount):
                    result.extend([lst[i]] * gloablAlipayWithdrawTimeForAccount)
                return result

            extendAlipayAccs = distribute_items(gloablAlipayAccounts)
        # 遍历所有账号
        if USE_THREADS <= 1:
            for i, account in enumerate(accounts_list, start=1):
                # print(f"当前账户{i}  ---------- ")
                if needCheckGlobalAlipay:
                    if i <= gloablAlipayWithdrawTimeForAccount * len(
                        gloablAlipayAccounts
                    ):
                        selectAlipayStr = extendAlipayAccs[i - 1]
                        if "#" in selectAlipayStr:
                            main(
                                account,
                                selectAlipayStr.split("#")[0],
                                selectAlipayStr.split("#")[1],
                            )
                            continue
                main(account)
        else:
            with ThreadPoolExecutor(max_workers=USE_THREADS) as executor:
                for i, account in enumerate(accounts_list):
                    # 为每个账号创建一个线程，注意传递参数的方式需要是元组，即使只有一个参数
                    if needCheckGlobalAlipay:
                        if i <= gloablAlipayWithdrawTimeForAccount * len(
                            gloablAlipayAccounts
                        ):
                            selectAlipayStr = extendAlipayAccs[i - 1]
                            if "#" in selectAlipayStr:
                                executor.submit(
                                    main,
                                    (
                                        account,
                                        selectAlipayStr.split("#")[0],
                                        selectAlipayStr.split("#")[1],
                                    ),
                                )
                                continue
                    executor.submit(main, account)
        print(f"\n---------运行完毕，统计收益---------")
        print(f"🎉🎉🎉  本轮累计提现了 ", totalWithdrawAmount, " 元 🎉🎉🎉 ")
'''你想干MwqCi1w嘛？偷UYw_8ilFaIVgB0_SQ8偷RYYYs摸摸的！'''

import httpx
import requests
from html import unescape
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

def get_token(userid: str, password: str) -> str:
    auth_url = "https://slbsso.meijo-u.ac.jp/opensso/json/authenticate"
    headers = {
        "Content-Type": "application/json",
        "Accept-API-Version": "resource=2.0, protocol=1.0"
    }

    response = requests.post(auth_url, headers=headers)
    response.raise_for_status()

    json_data = response.json()
    json_data["callbacks"][0]["input"][0]["value"] = userid
    json_data["callbacks"][1]["input"][0]["value"] = password

    cookies = requests.cookies.RequestsCookieJar()
    for c in response.cookies:
        cookies.set_cookie(c)

    response = requests.post(auth_url, headers=headers, cookies=cookies, json=json_data)
    response.raise_for_status()

    for c in response.cookies:
        cookies.set_cookie(c)

    auth_result = response.json()
    cookies.set("iPlanetDirectoryPro", auth_result["tokenId"], domain="slbsso.meijo-u.ac.jp")

    return auth_result["tokenId"]

def decode_chunked(data: str) -> str:
    decoded = ""
    while data:
        length_end = data.find("\r\n")
        if length_end == -1:
            break
        length_str = data[:length_end]
        length = int(length_str, 16)
        if length == 0:
            break
        start = length_end + 2
        end = start + length
        decoded += data[start:end]
        data = data[end + 2:]
    return decoded

async def login_ssl_vpn(userid: str, password: str):
    token_id = get_token(userid, password)

    async with httpx.AsyncClient(follow_redirects=False) as client:
        r = await client.get('https://ccmoon2.meijo-u.ac.jp/')
        if r.status_code != 302:
            raise Exception("初期GET失敗")
        cookies = r.cookies
        cookies.set("iPlanetDirectoryPro", token_id, domain="slbsso.meijo-u.ac.jp")
        
        login_url = r.headers['location']

        full_login_url = f"https://ccmoon2.meijo-u.ac.jp{login_url}"
        headers = {
            "User-Agent": "Mozilla/5.0",
        }
        r2 = await client.get(full_login_url, headers=headers, cookies=cookies, follow_redirects=False)
        if r2.status_code != 302:
            raise Exception("トークンログイン失敗")

        for cookie in r2.cookies.jar:
            cookies.set(cookie.name, cookie.value, domain=cookie.domain, path=cookie.path)

        path = r2.headers['location']
        
        res3 = await client.get(f"{path}", headers={
            "User-Agent": "Mozilla/5.0",
            "Cookie": f"iPlanetDirectoryPro={token_id}"
        }, cookies=cookies, follow_redirects=False)

        html = res3.text
        for cookie in res3.cookies.jar:
            cookies.set(cookie.name, cookie.value, domain=cookie.domain, path=cookie.path)

        start_tag = '<input type="hidden" name="SAMLResponse" value="'
        start_index = html.find(start_tag) + len(start_tag)
        end_index = html.find('" />', start_index)
        saml_response = unescape(html[start_index:end_index])

        res4 = await client.post(
            'https://ccmoon2.meijo-u.ac.jp/saml/sp/profile/post/acs',
            data={'SAMLResponse': saml_response},
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            cookies=cookies,
            follow_redirects=False
        )
        if res4.status_code != 302:
            raise Exception("SAML POST失敗")

        for cookie in res4.cookies.jar:
            cookies.set(cookie.name, cookie.value, domain=cookie.domain, path=cookie.path)
    print("cookies:", cookies)
    return cookies


def generate_keys(id):
    public_key = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtcAin0WDr51RopyQ6CEHlyI+YE8sWalnY8NyXKOfCXxY/bOdmXOEOGy3v/uDVYhAf6lyyLcjt2W6Q9wQjd01JxV5fcsnU3yPHcHJAw32FJ5u1LKbOtopG5u3OvrGgjjm/3w6Fw9Yfqr4s25+lod7qWh4rJ6BQECbrM7hF+oLoCsPG2q/O7b7unMK//8SC+BCcBijn+O03Y7VmRxcyQq/38mZaG1ZIowfs935M5gQvX0l5Ea/PN19dlMI2a/3AcQRmYmvlOoEsi3zNEyRMcl3b9+xJDkzye5heSxN+Q2DrWbrPpmjhiTH9bMLmVvoTxHq44KeR4X43mN33dL//lClywIDAQAB\n-----END PUBLIC KEY-----"
    pubkey = RSA.import_key(public_key)
    cipher = PKCS1_v1_5.new(pubkey)
    encrypted = cipher.encrypt(bytes(id, 'utf-8'))
    encrypted = encrypted.hex()
    encrypted = encrypted.upper()
    bytes.fromhex(encrypted)
    encrypted = base64_encode(encrypted)
    return encrypted

def base64_encode(hex_string):
    charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    binary_str = bin(int(hex_string, 16))[2:].zfill(len(hex_string) * 4)

    result = ""
    i = 0
    while i + 12 <= len(binary_str):
        block = binary_str[i:i+12]
        first6 = int(block[:6], 2)
        second6 = int(block[6:], 2)
        result += charset[first6] + charset[second6]
        i += 12

    remaining = len(binary_str) - i
    if remaining == 4:
        last4 = binary_str[i:] + '00'
        result += charset[int(last4, 2)]
    elif remaining == 8:
        first6 = binary_str[i:i+6]
        last2 = binary_str[i+6:] + '0000' 
        result += charset[int(first6, 2)] + charset[int(last2, 2)]

    while len(result) % 4 != 0:
        result += "="

    return result



def get_print_quota(key, cookies, id):
        url = f"https://ccmoon2.meijo-u.ac.jp/f5-w-68747470733a2f2f63636470737276312e6d65696a6f2d752e61632e6a70$$/api/user/users/{id}?type=1"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/",
            "Authorization":key,
        }
        return requests.get(url, headers=headers, cookies=convert_httpx_cookies_to_requests_jar(cookies)).content.decode("utf-8")

def convert_httpx_cookies_to_requests_jar(httpx_cookies: httpx.Cookies):
    jar = requests.cookies.RequestsCookieJar()
    for cookie in httpx_cookies.jar:
        jar.set(cookie.name, cookie.value, domain=cookie.domain, path=cookie.path)
    return jar

def login(id, password):
    return asyncio.run(login_ssl_vpn(id,password))

import json, asyncio
def web_print(key, cookies, file, id, job_id, settings):
    print(settings)
    url = r"https://ccmoon2.meijo-u.ac.jp/f5-w-68747470733a2f2f63636470737276312e6d65696a6f2d752e61632e6a70$$/api/spool01/files/webprint"
    json_data = {
        "user_id" : id,
        "queue_id":"web-ondemand",
        "ip":"192.168.230.231",
        "paper_type":"06" if settings["paper"] == "A4" else "05",
        "duplex_type":"1" if settings["sides"] == "片面" else "2",
        "color_mode_type":"1",
        "copies":"1",
        "number_up":"1" if settings["n_in_one"] == "1 in 1" else "2" if settings["n_in_one"] == "2 in 1" else "4" if settings["n_in_one"] == "4 in 1" else "1",
        "orientation_edge":"1" if settings["binding"] == "長辺" else "2",
        "print_orientation":"2" if settings["direction"] == "縦" else "1",
        "page_sort":"1"
    }
    files = {
        "data": ("blob", json.dumps(json_data), "application/json"),
        "files": (f"{job_id}.pdf", open(file, "rb"), "application/pdf")
    }
    print(files)
    headers = {
        "Authorization":key,
    }
    print(key)
    return requests.post(url, headers=headers, cookies=cookies, files=files) # getとpost間違えてて20分くらい悩んだ, methods not allowed出して...

def get_print_queue(key, cookies, id):
    headers = {
        "Authorization":key,
    }
    url = f"https://ccmoon2.meijo-u.ac.jp/f5-w-68747470733a2f2f63636470737276312e6d65696a6f2d752e61632e6a70$$/user/f5-h-$$/api/job/prints/search?user_id={id}&accepting=true&order_wait=true&output_wait=true&outputting=true&end=true&accepting_web=true"
    return requests.get(url, cookies=cookies, headers=headers).content.decode("utf-8")

async def do_print_icp(job_id, userid, password, file_name, settings):   
    cookies = await login_ssl_vpn(userid, password)
    web_print(generate_keys(userid), cookies, file_name, userid, job_id, settings).content.decode("utf-8")
    return get_print_queue(key=generate_keys(userid), cookies=cookies, id=userid)

async def print_queue(userid, password):
    cookies = await login_ssl_vpn(userid, password)
    quota = get_print_quota(generate_keys(userid), cookies)
    queue = get_print_queue(key=generate_keys(userid), cookies=cookies, id=userid)
    queue = json.loads(queue)
    quota = json.loads(quota)
    return [queue, quota]
# https://ccmoon2.meijo-u.ac.jp/f5-w-68747470733a2f2f63636470737276312e6d65696a6f2d752e61632e6a70$$/user/f5-h-$$/api/job/prints/search?user_id={user_id}&accepting=true&order_wait=true&output_wait=true&outputting=true&end=true&accepting_web=true
# ここにアクセスすればjob-queue見れるので確認用に...
# この辺の処理時間かかるのでjsであとから取得したほうがいいかもしれない(どっちでもいいけど)

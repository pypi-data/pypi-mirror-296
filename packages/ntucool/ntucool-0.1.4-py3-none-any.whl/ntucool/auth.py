import os
import pickle
import time
from dataclasses import dataclass
from urllib.parse import parse_qs, urlparse

import bs4
import httpx
import requests

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"

DEBUG = True and not os.getenv("PROD")


def get_saml() -> str:
    cookies = {}
    headers = {
        "Connection": "keep-alive",
        "Referer": "https://cool.ntu.edu.tw/login/portal",
        "User-Agent": USER_AGENT,
    }

    response = requests.get(
        "https://cool.ntu.edu.tw/login/saml",
        cookies=cookies,
        headers=headers,
        allow_redirects=False,
    )
    url = response.headers["Location"]
    return url


@dataclass
class SAMLRequest:
    params: dict[str, list[str]]

    _form_fields: dict[str, str]
    _acc_name: str
    _pass_name: str

    def get_data(self, account: str, password: str) -> dict[str, str]:
        return self._form_fields | {self._acc_name: account, self._pass_name: password}


def parse_saml_req(text: str) -> SAMLRequest:
    soup = bs4.BeautifulSoup(text, "html.parser")
    form: bs4.Tag = soup.select("form#MainForm")[0]

    params = parse_qs(urlparse(form.attrs["action"]).query)

    fields = {}
    acc_name = ""
    pass_name = ""
    fields = {}
    for field in form.select("input"):
        match field.attrs["type"]:
            case "text":
                acc_name = field.attrs["name"]
            case "password":
                pass_name = field.attrs["name"]
            case _:
                fields[field.attrs["name"]] = field.attrs["value"]

    saml = SAMLRequest(params, fields, acc_name, pass_name)
    return saml


def post_saml(saml_req: SAMLRequest, account: str, password: str) -> str:
    headers = {
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://adfs.ntu.edu.tw",
        "User-Agent": USER_AGENT,
    }

    response = requests.post(
        "https://adfs.ntu.edu.tw/adfs/ls/",
        params=saml_req.params,
        headers=headers,
        data=saml_req.get_data(account, password),
    )
    return response.text


def get_cookies(saml_res_page: str) -> dict[str, str]:
    soup = bs4.BeautifulSoup(saml_res_page, "html.parser")

    form = soup.select("form")[0]
    input_ele = form.select("input")[0]
    data = {input_ele.attrs["name"]: input_ele.attrs["value"]}
    url = form.attrs["action"]

    res = requests.post(url, headers={"User-Agent": USER_AGENT}, data=data)
    cookie_raw = res.headers["set-cookie"]
    c = dict([c.split(";")[0].split("=") for c in cookie_raw.split(", ")])
    return c


def cache_if_debug(filename: str, expire: int):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if DEBUG and os.path.exists(filename):
                if os.path.getmtime(filename) + expire > time.time():
                    return pickle.loads(open(filename, "rb").read())

            res = func(*args, **kwargs)
            pickle.dump(res, open(filename, "bw"))
            return res

        return wrapper

    return decorator


@cache_if_debug("cookies", 3600)
def get_auth_cookies(client: httpx.Client, account: str, password: str):
    # if DEBUG and os.path.exists("cookies"):
    # return pickle.loads(open("cookies", "rb").read())

    url = get_saml()
    res = client.get(url, headers={"User-Agent": USER_AGENT})
    saml = parse_saml_req(res.text)
    saml_res_page = post_saml(saml, account, password)
    cookies = get_cookies(saml_res_page)

    # pickle.dump(cookies, open("cookies", "bw"))
    return cookies


@cache_if_debug("cookies", 3600)
async def async_get_auth_cookies(
    client: httpx.AsyncClient, account: str, password: str
):
    # if DEBUG and os.path.exists("cookies"):
    #     return pickle.loads(open("cookies", "rb").read())

    url = get_saml()
    res = await client.get(url, headers={"User-Agent": USER_AGENT})
    saml = parse_saml_req(res.text)
    saml_res_page = post_saml(saml, account, password)
    cookies = get_cookies(saml_res_page)

    # pickle.dump(cookies, open("cookies", "bw"))
    return cookies

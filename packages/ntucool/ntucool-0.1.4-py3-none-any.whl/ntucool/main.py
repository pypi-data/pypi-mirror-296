from typing import Literal

from bs4 import BeautifulSoup
import pydantic

from ntucool.base import NTUCoolBase
from ntucool.requestor import Requestor
from pages.profile.profile import ProfilePage

from .course import Course, get_courses, get_courses_async
from .descriptor import NTUCoolDescriptor

pydantic.AfterValidator


class _NTUCool[Async: bool](NTUCoolBase[Async]):
    __URL__ = "/"

    account: str
    password: str

    # cookies: dict[str, str]
    # user_id: int = remote_property()
    # files_page: FilesPage = remote_property()

    courses = NTUCoolDescriptor(get_courses, get_courses_async)

    def __init__(self, account: str, password: str):
        # self.account = account
        # self.password = password
        self.requestor = Requestor(account, password, is_async=self._is_async)

    # @property
    # def soup(self) -> BeautifulSoup:
    #     text = await_(self.requestor.async_get(self.__URL__, is_xhr=True)).text
    #     return BeautifulSoup(text, "html.parser")

    @property
    def profile(self):
        return ProfilePage(parent=self)

    # async def async_update(self, url: str):
    #     url = "https://cool.ntu.edu.tw/"
    #     if env := get_env(url, BeautifulSoup(text, "html.parser")):
    #         self.user_id = env.current_user_id


# print(get_ntucool("https://cool.ntu.edu.tw/courses/34494/assignments/219719").text)
# print(ntucool._get_endpoint("/").text)
# print(ntucool.cookies)
# print(get_modules(35448, ntucool.cookies))


class NTUCool(_NTUCool[Literal[False]]):
    _is_async = False


class NTUCoolAsync(_NTUCool[Literal[True]]):
    _is_async = True
